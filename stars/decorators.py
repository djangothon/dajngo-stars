import json

from functools import wraps
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseNotAllowed, Http404
from django.http import HttpResponseForbidden, HttpResponseBadRequest


def ajax_view(only_POST=False, only_authenticated=False, **jsonargs):
    """
    Decorator that does the following for an ajax view
     - checks if the request is an ajax request
     - if only_POST is set to True then validates
       if its a POST request
     - if only_authenticated is set to True then validates
       if the user is authenticated
     - wraps the view response to json, only pass a dictionary
       in the view
    """
    def decorator(f):
        @wraps(f)
        def _ajax_view(request, *args, **kwargs):

            # check for ajax request
            if not request.is_ajax() and not settings.DEBUG:
                return HttpResponseForbidden(
                        mark_safe(_403_ERROR % 'Request must be set via AJAX.'))

            # check for POST request
            if only_POST:
                if request.method != 'POST' and request.method != 'REQUEST':
                    return HttpResponseNotAllowed(
                        mark_safe(_405_ERROR % (
                            'Request mehtod must be POST or REQUEST.')))

            # check if the user is authenticated or not
            if only_authenticated:
                user = request.user
                # check if the user is authenticated
                if not user.is_authenticated():
                    return HttpResponseForbidden(
                            mark_safe(_403_ERROR % 'User must be authenticated!'))

            # get the result
            result = f(request, *args, **kwargs)

            # if there is no result then send AJAX_ERROR
            # in the response
            if not result:
                result = { 'status': AJAX_ERROR }

            # determine the intendation of json
            indent = jsonargs.pop('indent', 4)

            # Dump as json
            return HttpResponse(json.dumps(result, indent=indent, **jsonargs))
        return _ajax_view
    return decorator