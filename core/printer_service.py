import socket
import threading
import logging
from datetime import datetime
from decimal import Decimal

logger = logging.getLogger(__name__)

# ESC/POS Constants
ESC = b'\x1b'
GS = b'\x1d'

CMD_INIT = ESC + b'@'
CMD_ALIGN_LEFT = ESC + b'a\x00'
CMD_ALIGN_CENTER = ESC + b'a\x01'
CMD_ALIGN_RIGHT = ESC + b'a\x02'
CMD_BOLD_ON = ESC + b'E\x01'
CMD_BOLD_OFF = ESC + b'E\x00'
CMD_DOUBLE_SIZE = GS + b'!\x11'     # 2x Width + 2x Height
CMD_DOUBLE_HEIGHT = GS + b'!\x01'   # 2x Height
CMD_DOUBLE_WIDTH = GS + b'!\x10'    # 2x Width
CMD_NORMAL_SIZE = GS + b'!\x00'     # Normal 1x
CMD_CUT_FULL = GS + b'V\x00'        # Full Cut
CMD_CUT_PARTIAL = GS + b'V\x01'     # Partial Cut
CMD_CUT_FEED = GS + b'V\x41\x03'    # Feed 3 lines & cut
CMD_LINE_FEED = b'\n'

def format_row(left_text: str, right_text: str, total_width: int = 40) -> str:
    """Format two columns with left and right alignment."""
    left_text = str(left_text)
    right_text = str(right_text)
    space_needed = total_width - len(left_text) - len(right_text)
    if space_needed < 1:
        max_left = max(1, total_width - len(right_text) - 1)
        left_text = left_text[:max_left]
        space_needed = 1
    return left_text + (' ' * space_needed) + right_text

def format_item_row(name: str, qty: int, amount: str = '', total_width: int = 40) -> str:
    """Format 3-column or 2-column item row."""
    qty_str = f"{qty:>3}x"
    if amount:
        right = f"{qty_str}  {amount:>8}"
        space_needed = total_width - len(name) - len(right)
        if space_needed < 1:
            max_name = max(1, total_width - len(right) - 1)
            name = name[:max_name]
            space_needed = 1
        return name + (' ' * space_needed) + right
    else:
        return format_row(name, qty_str, total_width)

def send_to_socket(ip: str, port: int, payload: bytes, timeout: float = 3.0) -> tuple[bool, str]:
    """
    Direct TCP socket communication to thermal network printer (port 9100).
    Returns (success: bool, message: str)
    """
    if not ip:
        return False, "No IP address specified"
    
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, int(port)))
        sock.sendall(payload)
        return True, f"Printed successfully to {ip}:{port}"
    except socket.timeout:
        err = f"Connection timeout to {ip}:{port}"
        logger.warning(err)
        return False, err
    except ConnectionRefusedError:
        err = f"Connection refused by {ip}:{port} (printer may be off or busy)"
        logger.warning(err)
        return False, err
    except Exception as e:
        err = f"Socket error to {ip}:{port}: {str(e)}"
        logger.warning(err)
        return False, err
    finally:
        if sock:
            try:
                sock.close()
            except Exception:
                pass

def send_async(ip: str, port: int, payload: bytes):
    """Fire and forget printing in background thread so POS UI is never blocked."""
    t = threading.Thread(target=send_to_socket, args=(ip, port, payload), daemon=True)
    t.start()


# =========================================================================
# ESC/POS Payload Builders
# =========================================================================

def build_kot_payload(order, printer_name: str, items: list, line_width: int = 40) -> bytes:
    """Build ESC/POS byte sequence for a KOT ticket."""
    p = bytearray()
    p.extend(CMD_INIT)
    
    # Check if parcel / takeaway
    is_parcel = getattr(order, 'order_type', None) == 'parcel' or order.table is None
    
    # Header - Print PARCEL in Bold Double-Size at the top
    p.extend(CMD_ALIGN_CENTER)
    p.extend(CMD_BOLD_ON)
    p.extend(CMD_DOUBLE_SIZE)
    if is_parcel:
        p.extend(b"*** PARCEL ***\n")
    else:
        p.extend(b"*** KOT ***\n")
    p.extend(CMD_NORMAL_SIZE)
    
    p.extend(CMD_BOLD_ON)
    p.extend(f"[{printer_name.upper()} STATION]\n".encode('ascii', errors='ignore'))
    if is_parcel:
        p.extend(CMD_DOUBLE_WIDTH)
        p.extend(b">> PARCEL ORDER <<\n")
        p.extend(CMD_NORMAL_SIZE)
    p.extend(CMD_BOLD_OFF)
    
    if order.company and order.company.name:
        p.extend(f"{order.company.name}\n".encode('ascii', errors='ignore'))
    
    p.extend(b"-" * line_width + b"\n")
    
    # Metadata
    p.extend(CMD_ALIGN_LEFT)
    p.extend(CMD_BOLD_ON)
    p.extend(CMD_DOUBLE_WIDTH)
    p.extend(f"ORDER: #{order.order_number}\n".encode('ascii', errors='ignore'))
    p.extend(CMD_NORMAL_SIZE)
    date_str = datetime.now().strftime('%d/%m/%Y  %I:%M %p')
    p.extend(f"Date: {date_str}\n".encode('ascii', errors='ignore'))
    
    if is_parcel:
        p.extend(CMD_BOLD_ON)
        p.extend(CMD_DOUBLE_WIDTH)
        p.extend(b"TYPE:  PARCEL\n")
        p.extend(CMD_NORMAL_SIZE)
        p.extend(CMD_BOLD_OFF)
    else:
        table_label = f"Table {order.table.table_number}" if order.table else "Direct Sale"
        p.extend(CMD_DOUBLE_WIDTH)
        p.extend(f"{table_label}\n".encode('ascii', errors='ignore'))
        p.extend(CMD_NORMAL_SIZE)
        p.extend(CMD_BOLD_OFF)
    
    p.extend(b"=" * line_width + b"\n")
    
    # Items Header
    header_row = format_row("ITEM NAME", "QTY", line_width)
    p.extend(CMD_BOLD_ON)
    p.extend(header_row.encode('ascii', errors='ignore') + b"\n")
    p.extend(CMD_BOLD_OFF)
    p.extend(b"-" * line_width + b"\n")
    
    # Items
    total_qty = 0
    p.extend(CMD_BOLD_ON)
    for item in items:
        item_name = item.item_name or (item.menu_item.name if item.menu_item else 'Item')
        qty = item.quantity
        total_qty += qty
        row = format_item_row(item_name, qty, '', line_width)
        p.extend(row.encode('ascii', errors='ignore') + b"\n")
        if getattr(item, 'special_instructions', None):
            p.extend(CMD_BOLD_OFF)
            p.extend(f"  * Note: {item.special_instructions}\n".encode('ascii', errors='ignore'))
            p.extend(CMD_BOLD_ON)
    
    p.extend(CMD_BOLD_OFF)
    p.extend(b"=" * line_width + b"\n")
    
    # Footer
    p.extend(CMD_ALIGN_LEFT)
    summary_row = format_row(f"Total Items: {len(items)}", f"Total Qty: {total_qty}", line_width)
    p.extend(summary_row.encode('ascii', errors='ignore') + b"\n")
    
    p.extend(b"\n\n\n")
    p.extend(CMD_CUT_FEED)
    return bytes(p)


def build_bill_payload(order, line_width: int = 40) -> bytes:
    """Build ESC/POS byte sequence for a Customer Tax Invoice / Bill."""
    p = bytearray()
    p.extend(CMD_INIT)
    
    # Company Header
    p.extend(CMD_ALIGN_CENTER)
    p.extend(CMD_BOLD_ON)
    p.extend(CMD_DOUBLE_SIZE)
    company_name = order.company.name if order.company else "BITPOS RESTAURANT"
    p.extend(f"{company_name}\n".encode('ascii', errors='ignore'))
    p.extend(CMD_NORMAL_SIZE)
    p.extend(CMD_BOLD_OFF)
    
    if order.company and order.company.address:
        p.extend(f"{order.company.address}\n".encode('ascii', errors='ignore'))
    
    p.extend(CMD_BOLD_ON)
    p.extend(b"TAX INVOICE\n")
    p.extend(CMD_BOLD_OFF)
    p.extend(b"=" * line_width + b"\n")
    
    # Meta Info
    p.extend(CMD_ALIGN_LEFT)
    p.extend(CMD_BOLD_ON)
    p.extend(format_row(f"Bill No: {order.order_number}", f"Date: {order.created_at.strftime('%d/%m/%Y')}", line_width).encode('ascii', errors='ignore') + b"\n")
    p.extend(CMD_BOLD_OFF)
    
    table_str = f"Table: {order.table.table_number}" if order.table else "Type: Direct Sale"
    time_str = f"Time: {order.created_at.strftime('%I:%M %p')}"
    p.extend(format_row(table_str, time_str, line_width).encode('ascii', errors='ignore') + b"\n")
    
    billed_by = order.billed_by.username if order.billed_by else "Staff"
    p.extend(format_row(f"Billed By: {billed_by}", "", line_width).encode('ascii', errors='ignore') + b"\n")
    
    p.extend(b"-" * line_width + b"\n")
    
    # Table Header
    header = format_item_row("ITEM", 1, "AMOUNT", line_width).replace("  1x", " QTY")
    p.extend(CMD_BOLD_ON)
    p.extend(header.encode('ascii', errors='ignore') + b"\n")
    p.extend(CMD_BOLD_OFF)
    p.extend(b"-" * line_width + b"\n")
    
    # Items
    items = order.items.all()
    for item in items:
        item_name = item.item_name or (item.menu_item.name if item.menu_item else 'Item')
        item_total = f"{(item.price * item.quantity):.2f}"
        row = format_item_row(item_name, item.quantity, item_total, line_width)
        p.extend(row.encode('ascii', errors='ignore') + b"\n")
    
    p.extend(b"=" * line_width + b"\n")
    
    # Total
    p.extend(CMD_BOLD_ON)
    p.extend(CMD_DOUBLE_WIDTH)
    tot_row = format_row("TOTAL:", f"{order.total_amount:.2f}", int(line_width * 0.75))
    p.extend(f"{tot_row}\n".encode('ascii', errors='ignore'))
    p.extend(CMD_NORMAL_SIZE)
    p.extend(CMD_BOLD_OFF)
    p.extend(b"-" * line_width + b"\n")
    
    # Payment Details
    if order.status == 'paid':
        p.extend(CMD_ALIGN_LEFT)
        p.extend(f"Payment Method: {order.get_payment_method_display().upper()}\n".encode('ascii', errors='ignore'))
        if order.cash_amount > 0:
            p.extend(format_row("Cash Paid:", f"{order.cash_amount:.2f}", line_width).encode('ascii', errors='ignore') + b"\n")
        if order.upi_amount > 0:
            p.extend(format_row("UPI Paid:", f"{order.upi_amount:.2f}", line_width).encode('ascii', errors='ignore') + b"\n")
        p.extend(b"-" * line_width + b"\n")
        
    # Footer
    p.extend(CMD_ALIGN_CENTER)
    p.extend(b"\nThank you for visiting us!\n")
    p.extend(b"Powered by BITPOS\n")
    
    p.extend(b"\n\n\n")
    p.extend(CMD_CUT_FEED)
    return bytes(p)


def build_test_payload(printer, line_width: int = 40) -> bytes:
    """Build diagnostic test print slip."""
    p = bytearray()
    p.extend(CMD_INIT)
    p.extend(CMD_ALIGN_CENTER)
    p.extend(CMD_BOLD_ON)
    p.extend(CMD_DOUBLE_SIZE)
    p.extend(b"BITPOS TEST PRINT\n")
    p.extend(CMD_NORMAL_SIZE)
    p.extend(b"=" * line_width + b"\n")
    
    p.extend(CMD_ALIGN_LEFT)
    p.extend(format_row("Printer Name:", printer.name, line_width).encode('ascii', errors='ignore') + b"\n")
    p.extend(format_row("Role / Type:", printer.get_printer_type_display(), line_width).encode('ascii', errors='ignore') + b"\n")
    p.extend(format_row("IP Address:", printer.ip_address, line_width).encode('ascii', errors='ignore') + b"\n")
    p.extend(format_row("Port:", str(printer.port), line_width).encode('ascii', errors='ignore') + b"\n")
    p.extend(format_row("Store:", printer.company.name if printer.company else "--", line_width).encode('ascii', errors='ignore') + b"\n")
    p.extend(format_row("Time:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), line_width).encode('ascii', errors='ignore') + b"\n")
    
    p.extend(b"-" * line_width + b"\n")
    p.extend(CMD_ALIGN_CENTER)
    p.extend(CMD_BOLD_ON)
    p.extend(b"*** PRINTER IS ONLINE & READY ***\n")
    p.extend(CMD_BOLD_OFF)
    
    p.extend(b"\n\n\n")
    p.extend(CMD_CUT_FEED)
    return bytes(p)


# =========================================================================
# High-Level Routing Services
# =========================================================================

def print_kot_for_order(order, items=None, synchronous: bool = False) -> dict:
    """
    Route items in the order to their assigned KOT printers based on category.
    E.g. Non_veg -> KITCHEN Printer (192.168.1.20)
         Drinks  -> JUICE Printer (192.168.1.30)
    """
    company = order.company
    if items is None:
        items = list(order.items.all())
    
    if not items:
        return {'status': 'empty', 'message': 'No items to print'}
    
    from .models import Printer
    kot_printers = {p.id: p for p in Printer.objects.filter(company=company, printer_type='kot', is_active=True)}
    
    # Map items to printer: printer_id -> list of OrderItems
    printer_item_map = {}
    unassigned_items = []
    
    for item in items:
        printer = None
        if item.menu_item and item.menu_item.category and item.menu_item.category.printer:
            printer = item.menu_item.category.printer
        elif item.menu_item and item.menu_item.category:
            cat_name = item.menu_item.category.name.strip().lower()
            for p in kot_printers.values():
                p_name = p.name.strip().lower()
                if ('kitchen' in p_name and ('non' in cat_name or 'veg' in cat_name or 'biriyani' in cat_name or 'rice' in cat_name or 'food' in cat_name)) or \
                   ('juice' in p_name and ('drink' in cat_name or 'juice' in cat_name or 'tea' in cat_name or 'beverage' in cat_name)):
                    printer = p
                    break
        
        if printer and printer.is_active:
            if printer.id not in printer_item_map:
                printer_item_map[printer.id] = []
            printer_item_map[printer.id].append(item)
        else:
            unassigned_items.append(item)
            
    if unassigned_items and kot_printers:
        default_printer_id = list(kot_printers.keys())[0]
        if default_printer_id not in printer_item_map:
            printer_item_map[default_printer_id] = []
        printer_item_map[default_printer_id].extend(unassigned_items)
        
    results = {}
    for p_id, p_items in printer_item_map.items():
        printer = kot_printers.get(p_id)
        if not printer:
            continue
        payload = build_kot_payload(order, printer.name, p_items)
        if synchronous:
            success, msg = send_to_socket(printer.ip_address, printer.port, payload)
            results[printer.name] = {'success': success, 'ip': printer.ip_address, 'message': msg, 'item_count': len(p_items)}
        else:
            send_async(printer.ip_address, printer.port, payload)
            results[printer.name] = {'success': True, 'ip': printer.ip_address, 'message': f'Dispatched to {printer.ip_address}:{printer.port}', 'item_count': len(p_items)}

    return results


def print_bill_for_order(order, synchronous: bool = False) -> dict:
    """
    Send the full tax invoice / receipt to the CASH / Bill printer.
    E.g. CASH Printer (192.168.1.10)
    """
    company = order.company
    from .models import Printer
    cash_printer = Printer.objects.filter(company=company, printer_type__in=['cash_bill', 'bill'], is_active=True).first()
    
    if not cash_printer:
        return {'success': False, 'message': 'No Cash/Bill printer configured for this store'}
    
    payload = build_bill_payload(order)
    if synchronous:
        success, msg = send_to_socket(cash_printer.ip_address, cash_printer.port, payload)
        return {'success': success, 'printer': cash_printer.name, 'ip': cash_printer.ip_address, 'message': msg}
    else:
        send_async(cash_printer.ip_address, cash_printer.port, payload)
        return {'success': True, 'printer': cash_printer.name, 'ip': cash_printer.ip_address, 'message': f'Dispatched to {cash_printer.ip_address}:{cash_printer.port}'}


def build_table_transfer_payload(order, old_table_label: str, new_table_label: str, printer_name: str, line_width: int = 40) -> bytes:
    """Build ESC/POS byte sequence for Table Transfer / Shift Notice."""
    p = bytearray()
    p.extend(CMD_INIT)
    
    # Header
    p.extend(CMD_ALIGN_CENTER)
    p.extend(CMD_BOLD_ON)
    p.extend(CMD_DOUBLE_SIZE)
    p.extend(b"*** TABLE TRANSFER ***\n")
    p.extend(CMD_NORMAL_SIZE)
    p.extend(b"\n")
    
    p.extend(CMD_ALIGN_CENTER)
    p.extend(f"STATION: {printer_name.upper()}\n".encode('ascii', errors='replace'))
    p.extend(CMD_BOLD_OFF)
    p.extend(b"=" * line_width + b"\n")
    
    p.extend(CMD_ALIGN_LEFT)
    p.extend(CMD_BOLD_ON)
    p.extend(CMD_DOUBLE_WIDTH)
    p.extend(f"ORDER #: {order.order_number}\n".encode('ascii', errors='replace'))
    p.extend(CMD_NORMAL_SIZE)
    p.extend(CMD_BOLD_OFF)
    now_str = datetime.now().strftime('%d-%b-%Y  %I:%M %p')
    p.extend(f"Time:    {now_str}\n".encode('ascii', errors='replace'))
    p.extend(b"-" * line_width + b"\n")
    
    # Prominent FROM and TO block
    p.extend(CMD_BOLD_ON)
    p.extend(CMD_ALIGN_LEFT)
    p.extend(f"FROM:  {old_table_label.upper()}\n".encode('ascii', errors='replace'))
    p.extend(CMD_DOUBLE_SIZE)
    p.extend(f"TO:    {new_table_label.upper()}\n".encode('ascii', errors='replace'))
    p.extend(CMD_NORMAL_SIZE)
    p.extend(CMD_BOLD_OFF)
    p.extend(b"-" * line_width + b"\n")
    
    p.extend(CMD_ALIGN_CENTER)
    p.extend(CMD_BOLD_ON)
    p.extend(b">> PLEASE SERVE TO NEW TABLE <<\n")
    p.extend(CMD_BOLD_OFF)
    p.extend(b"=" * line_width + b"\n")
    
    # Items summary
    p.extend(CMD_ALIGN_LEFT)
    p.extend(b"CURRENT ORDER ITEMS:\n")
    for item in order.items.all():
        p.extend(f" - {item.quantity}x {item.item_name}\n".encode('ascii', errors='replace'))
        
    p.extend(b"-" * line_width + b"\n")
    p.extend(b"\n\n\n")
    p.extend(CMD_CUT_FEED)
    return bytes(p)


def print_table_transfer_notice(order, old_table_label: str, new_table_label: str, synchronous: bool = False) -> dict:
    """
    Sends table transfer / shift notice to all active station printers (KITCHEN, JUICE, etc.).
    """
    company = order.company
    from .models import Printer
    kot_printers = Printer.objects.filter(company=company, printer_type='kot', is_active=True)
    
    results = {}
    for printer in kot_printers:
        payload = build_table_transfer_payload(order, old_table_label, new_table_label, printer.name)
        if synchronous:
            success, msg = send_to_socket(printer.ip_address, printer.port, payload)
            results[printer.name] = {'success': success, 'ip': printer.ip_address, 'message': msg}
        else:
            send_async(printer.ip_address, printer.port, payload)
            results[printer.name] = {'success': True, 'ip': printer.ip_address, 'message': f'Dispatched to {printer.ip_address}:{printer.port}'}
            
    return results


def test_printer(printer, synchronous: bool = True) -> tuple[bool, str]:
    """Send a diagnostic test slip to the printer."""
    payload = build_test_payload(printer)
    return send_to_socket(printer.ip_address, printer.port, payload, timeout=3.0)