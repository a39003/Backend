from django.core.handlers.wsgi import WSGIRequest

from .functions import *
from .models import *
from .response import *


def generate_create_response(request: WSGIRequest, fields,
                             table_name, meta_field, class_type,
                             required_field, _check_distinct=False,
                             field_distinct=None):
    # try:
        # check_if_user_exist(request.headers.get(String.authorization))
        try:
            data = set_data_to_dict(request, fields, required_field)
            instance = class_type(data).to_dict()
            if _check_distinct:
                check_distinct(table_name, field_distinct, instance[field_distinct])

            post_data(table_name, instance, meta_field)

            return successResponse(instance)
        except Exception as e:
            return exceptionResponse(e)
    # except Exception as e:
        # return errorResponse(ResponseTitle.message, ResponseMessage.not_authenticated,
        #                      HTTPStatus.BAD_REQUEST)


def generate_get_list_data_response(request: WSGIRequest, page_number, items_per_page, table_name, meta_field):
    # try:
    #     check_if_user_exist(request.headers.get(String.authorization))
        try:
            result = get_list_data(table_name, page_number, meta_field, items_per_page)
            return successResponse(result)
        except Exception as e:
            return exceptionResponse(e)
    # except Exception as e:
    #     return errorResponse(ResponseTitle.message, ResponseMessage.not_authenticated, HTTPStatus.BAD_REQUEST)


def generate_delete_data_response(table_name, meta_field, _id):
    try:
        delete_data_by_id(table_name, _id, meta_field)
        return successResponse({ResponseTitle.message: ResponseMessage.delete_success})
    except Exception as e:
        return exceptionResponse(e)


def generate_get_data_by_id_response(table_name, _id):
    try:
        data = get_data_by_id(table_name, _id)
        if data is None:
            return errorResponse(ResponseTitle.message, ResponseMessage.element_not_found, HTTPStatus.NOT_FOUND)
        return successResponse(data)
    except Exception as e:
        return exceptionResponse(e)


def generate_get_data_by_other_field(table_name, field_name, value):
    try:
        data = get_data_by_other_field(table_name, field_name, value)
        if not data:
            return errorResponse(ResponseTitle.message, ResponseMessage.element_not_found, HTTPStatus.NOT_FOUND)
        return successResponse(data)
    except Exception as e:
        return exceptionResponse(e)


def generate_update_data(request: WSGIRequest, table_name, _id, fields, class_type, required_field,
                         _check_distinct=False,
                         field_distinct=None):
    # try:
        # check_if_user_exist(request.headers.get(String.authorization))
        try:
            if request.POST == {} and request.FILES == {}:
                raise Exception(ResponseMessage.no_data_provided)
            data = set_data_to_dict(
                request=request,
                table_name=table_name,
                required_field=required_field,
                _id=_id,
                is_update_method=True,
                fields=fields,
            )
            print(data)
            instance = class_type(data).to_dict()
            if _check_distinct:
                check_distinct(table_name, field_distinct, instance[field_distinct])
            update_data(table_name, instance)
            return successResponse(instance)
        except Exception as e:
            return exceptionResponse(e)
    # except Exception as e:
    #     return errorResponse(ResponseTitle.message, ResponseMessage.not_authenticated,
    #                          HTTPStatus.BAD_REQUEST)


def generate_login_response(request: WSGIRequest):
    try:
        email = request.POST[String.email]
        password = request.POST[String.password]
        token = sign_in_with_email_and_password(email, password)
        header = {String.authorization: token}
        return successResponse({ResponseTitle.message: ResponseMessage.login_success}, header)
    except Exception as e:
        return errorResponse(ResponseTitle.message, ResponseMessage.not_correct_email_or_password,
                             HTTPStatus.NOT_FOUND)


def generate_signup_response(request: WSGIRequest):
    try:
        sign_up_with_email_and_password(request)
        return successResponse({ResponseTitle.message: ResponseMessage.signup_success})
    except Exception as e:
        return exceptionResponse(e)
