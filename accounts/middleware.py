class PermissionMiddleware:
    """Middleware to check user permissions and add to context"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add is_admin flag to request
        if request.user.is_authenticated:
            request.is_admin = request.user.is_staff or request.user.groups.filter(name='Administrators').exists()
        else:
            request.is_admin = False

        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        # Add is_admin to template context
        if hasattr(response, 'context_data'):
            response.context_data['is_admin'] = request.is_admin
        return response