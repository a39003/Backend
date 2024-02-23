from django.views.decorators.csrf import csrf_exempt
from .const import *
from .generate import *


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == Method.post:
        return generate_login_response(request)
    return errorResponse(ResponseTitle.message, ResponseMessage.method_not_allowed, HTTPStatus.METHOD_NOT_ALLOWED)


@csrf_exempt
def logout(request):
    # todo something
    pass


@csrf_exempt
def signup(request):
    if request.method == Method.post:
        return generate_signup_response(request)
    return errorResponse(ResponseTitle.message, ResponseMessage.method_not_allowed, HTTPStatus.METHOD_NOT_ALLOWED)


@csrf_exempt
def create_items(request, class_params, class_type):
    if request.method == Method.post:
        return generate_create_response(
            request=request,
            fields=class_params[String.table_fields],
            table_name=class_params[String.table_name],
            meta_field=class_params[String.meta_data],
            class_type=class_type,
            required_field=class_params[String.required_fields],
            _check_distinct=class_params[String.check_distinct],
            field_distinct=class_params[String.distinct_fields],
        )
    return errorResponse(ResponseTitle.message, ResponseMessage.method_not_allowed, HTTPStatus.METHOD_NOT_ALLOWED)


@csrf_exempt
def get_list_item(request, page_number, items_per_page, class_params):
    if request.method == Method.get:
        return generate_get_list_data_response(
            request=request,
            page_number=page_number,
            items_per_page=items_per_page,
            table_name=class_params[String.table_name],
            meta_field=class_params[String.meta_data],
        )
    return errorResponse(ResponseTitle.message, ResponseMessage.method_not_allowed, HTTPStatus.METHOD_NOT_ALLOWED)


@csrf_exempt
def get_put_delete_item_by_id(request, id, class_params, class_type):
    match request.method:
        case Method.post:
            return generate_update_data(
                request=request,
                _id=id,
                fields=class_params[String.table_fields],
                class_type=class_type,
                table_name=class_params[String.table_name],
                required_field=class_params[String.required_fields],
            )
        case Method.get:
            return generate_get_data_by_id_response(
                table_name=class_params[String.table_name],
                _id=id
            )
        case Method.delete:
            return generate_delete_data_response(
                table_name=class_params[String.table_name],
                meta_field=class_params[String.meta_data],
                _id=id,
            )
        case default:
            return errorResponse(ResponseTitle.message,
                                 ResponseMessage.method_not_allowed, HTTPStatus.METHOD_NOT_ALLOWED)


@csrf_exempt
def get_user_by_email(request, email):
    if request.method == Method.get:
        return generate_get_data_by_other_field(
            table_name=TableName.users,
            field_name=String.email,
            value=email,
        )
    return errorResponse(ResponseTitle.message, ResponseMessage.method_not_allowed, HTTPStatus.METHOD_NOT_ALLOWED)
