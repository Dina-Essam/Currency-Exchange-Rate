from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        'ValidationError': _handler_generic_error,
        'HTTP404': _handler_generic_error,
        'PermissionDenied': _handler_generic_error,
        'NotFound': _handler_generic_error,
        'CustomValidation': _handler_generic_error,

    }
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    exception_name = exc.__class__.__name__
    if exception_name in handlers:
        return handlers[exception_name](exc, context, response)
    return response


def _handler_generic_error(exc, context, response):
    return response
