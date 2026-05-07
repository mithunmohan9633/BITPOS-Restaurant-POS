from django.shortcuts import redirect
from django.contrib.auth import logout

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            if hasattr(request.user, 'profile') and request.user.profile.company:
                if not request.user.profile.company.is_active:
                    logout(request)
                    return redirect('/login/?error=subscription')
        
        return self.get_response(request)
