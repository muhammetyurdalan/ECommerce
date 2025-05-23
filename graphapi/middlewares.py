
class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(response.content.decode('utf-8'))
        print(response.content.decode('utf-8')['errors'][0]['message'])
        return response