from http import HTTPStatus

from django.http import JsonResponse

from productManagement.const import ResponseTitle


def exceptionResponse(exception):
    return JsonResponse({ResponseTitle.error: str(exception)}, safe=False, status=HTTPStatus.BAD_REQUEST)


def successResponse(data, header=None):
    return JsonResponse(data, safe=False, status=HTTPStatus.OK, headers=header)


def errorResponse(title, message, status):
    return JsonResponse({title: message},
                        safe=False, status=status)
