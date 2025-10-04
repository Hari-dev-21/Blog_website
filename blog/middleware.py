# accounts/middleware.py

from django.shortcuts import redirect
from django.urls import reverse


class BlockAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define the paths you want to block for logged-in users
        unauthenticated_only_paths = [
            reverse('login'),
            reverse('register'),
            reverse('password_reset')

        ]

        authenticated_path = [
            reverse('dashboard'),
            
        ]


        if request.user.is_authenticated and request.path in unauthenticated_only_paths:
            return redirect('dashboard')  # Redirect to home/dashboard if already logged in
        
        if not request.user.is_authenticated and request.path in authenticated_path:
            return redirect('login') 

        return self.get_response(request)
