"""
Custom postprocessing hooks for drf-spectacular to customize API documentation.
"""

def custom_postprocessing_hook(result, generator, request, public):
    """
    Customize the OpenAPI schema by modifying tags for auth endpoints.
    This hook runs after the schema is generated.
    """
    # Update tags for auth endpoints
    if 'paths' in result:
        for path, methods in result['paths'].items():
            # Check if this is an auth endpoint (djoser endpoints)
            if path.startswith('/api/auth/'):
                for method, operation in methods.items():
                    if method.lower() in ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']:
                        # Replace the default tags with 'Auth'
                        operation['tags'] = ['Auth']
    
    return result
