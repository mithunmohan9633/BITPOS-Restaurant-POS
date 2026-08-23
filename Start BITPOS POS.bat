@echo off
:: Start Chrome with kiosk-printing mode enabled
:: This makes chrome print WITHOUT showing the print dialog
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --kiosk-printing http://localhost:8000/
