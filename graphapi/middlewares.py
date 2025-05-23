import json
from error import errors
from django.utils.translation import gettext, activate


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        process_exception(request, response)
        return response

def process_exception(request, response):
    try:
        user = request.user
        lang = user.language if not user.is_anonymous else 'en'
        activate(lang)
        response_str = response.content.decode('utf-8')
        response_dict = json.loads(response_str)
        error = response_dict['errors'][0]['message']
        error_code = json.loads(error).get('code', None)
        if error_code:
            message = {"code": error_code, "message": gettext(errors[error_code])}
            response_dict['errors'][0]['message'] = message
            response.content = json.dumps(response_dict).encode('utf-8')
    except:
        pass