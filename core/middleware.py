from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils import timezone

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            if hasattr(request.user, 'profile') and request.user.profile.company:
                company = request.user.profile.company
                
                # Check expiration date
                if company.valid_until and company.valid_until < timezone.now().date():
                    if company.is_active:
                        company.is_active = False
                        company.save()

                if not company.is_active:
                    logout(request)
                    return redirect('/login/?error=subscription')
        
        return self.get_response(request)
