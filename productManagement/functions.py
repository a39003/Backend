import os
import uuid
import math as mt

from django.core.handlers.wsgi import WSGIRequest

from .const import TableName, ResponseMessage
from .models import Users
from .databaseManagement import *

from .firebaseConfig import *

last_document = None


def upload_file(listFile):
    listUrl = []
    for index, file in enumerate(listFile):
        
        # Process each file as needed
        file_extension = str(file.name).split(".")[1]
        file_name = str(uuid.uuid4()) + "." + file_extension
        file_path = f"images/{file_name}"
        if not os.path.exists('/tmp'):
            os.makedirs('/tmp')
        temp_file_path = os.path.join('/tmp', file_name)

        # Save the uploaded file to a temporary location
        with open(temp_file_path, 'wb') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)

        download_url = upload_file_to_database(file_path=file_path, temp_file_path=temp_file_path)
        listUrl.append(download_url)
        os.remove(temp_file_path)
    return listUrl


def set_data_to_dict(request: WSGIRequest, fields, required_field, is_update_method=False, table_name=None, _id=None):
    data = {}
    if is_update_method:
        data = get_data_by_id(table_name, _id)
        if data is None:
            raise Exception(ResponseMessage.element_not_found)
    for field in fields:
        _data = None
        if field in request.POST:
            _data = request.POST[field]
        if field in request.FILES:
            _data = upload_file(request.FILES.getlist(field))
        if is_update_method:
            if _data is None:
                continue
        if _data is None and field in required_field and is_update_method is False:
            raise Exception(f"required field {field}")
        data[field] = _data

    if is_update_method is False:
        data[String.id] = str(uuid.uuid4())
        data[String.createAt] = datetime.now()
    data[String.updateAt] = datetime.now()

    return data


def post_data(table_name, data, meta_field):
    upload_data_to_database(table_name=table_name, _id=data[String.id], data=data)
    set_meta_data(meta_field)


def skip_element(table_name, page_number, items_per_page, total_pages):
    ref = get_all_data_from_database(table_name)

    if page_number == 1:
        ref = ref.limit(items_per_page)
    else:
        global last_document
        ref = ref.limit(items_per_page * (page_number - 1))
        data = ref.get()
        data_length = len(data)
        last_document = data[data_length - 1]
        ref = ref.start_after(last_document).limit(items_per_page)

    data = ref.get()
    result = [doc.to_dict() for doc in data]
    return {
        String.data: result,
        String.currentPage: page_number,
        String.totalPages: total_pages
    }


def get_list_data(table_name, page_number, meta_field, items_per_page):
    if items_per_page <= 0:
        raise Exception(ResponseMessage.item_per_page_not_valid)
    if page_number <= 0:
        raise Exception(ResponseMessage.less_than_0)

    meta_data = get_data_by_id(TableName.metaData, meta_field)

    if meta_data is None or meta_data[String.totalItems] is 0:
        raise Exception(ResponseMessage.list_is_empty)

    total_pages = mt.ceil(meta_data[String.totalItems] / items_per_page)

    if page_number > total_pages:
        raise Exception(ResponseMessage.greater_than_total_page)

    return skip_element(
        table_name=table_name,
        page_number=page_number,
        total_pages=total_pages,
        items_per_page=items_per_page
    )


def check_distinct(table_name, field_distinct, value_distinct):
    data = get_all_data_from_database(table_name).stream()
    for doc in data:
        _data = doc.get(field_distinct)
        if _data == value_distinct:
            raise Exception(ResponseMessage.element_exists)


def get_data_by_id(table_name, _id):
    return get_data_by_id_from_database(table_name, _id)


def get_data_by_other_field(table_name, field_name, value):
    data = get_date_by_other_field_from_database(table_name=table_name, field_name=field_name, value=value)
    list_doc = []
    for doc in data:
        list_doc.append(doc.to_dict())
    return list_doc


def update_data(table_name, data):
    upload_data_to_database(table_name=table_name, _id=data[String.id], data=data)


def delete_data_by_id(table_name, _id, meta_field):
    data = get_data_by_id_from_database(table_name, _id)
    if data is None:
        raise Exception(ResponseMessage.element_not_found)
    set_meta_data(meta_field, True)
    delete_data_from_database(table_name, _id)


def sign_in_with_email_and_password(email, password):
    user = pyre_auth.sign_in_with_email_and_password(email, password)
    return user[String.token]


def sign_up_with_email_and_password(request: WSGIRequest):
    email = None
    password = None
    try:
        if String.email in request.POST:
            email = request.POST[String.email]
        if String.password in request.POST:
            password = request.POST[String.password]

        user = auth.get_user_by_email(email)
        if user.email is not None:
            raise Exception(ResponseMessage.email_exists)
    except Exception as e:
        if String.no_user_found in str(e):
            is_admin = False
            if String.is_admin in request.POST:
                is_admin = bool(request.POST[String.is_admin])

            data = {
                String.id: str(uuid.uuid4()),
                String.email: email,
                String.is_admin: is_admin,
            }
            _user = Users(data).to_dict()
            pyre_auth.create_user_with_email_and_password(email, password)
            upload_data_to_database(table_name=TableName.users, _id=_user[String.id], data=_user)

        else:
            raise Exception(ResponseMessage.email_exists)


def sign_out():
    # Todo something
    pass


def check_if_user_exist(token):
    _token = split_token(token)
    return auth.verify_id_token(_token)


def split_token(token):
    return str(token).split("Bearer ")[1]


def set_meta_data(meta_field, is_delete_method=False):
    meta_data = get_data_by_id(TableName.metaData, meta_field)
    if is_delete_method:
        if meta_data is None or meta_data[String.totalItems] is 0:
            raise Exception(ResponseMessage.element_not_found)
        total_items = meta_data[String.totalItems] - 1
    else:
        if meta_data is not None:
            total_items = meta_data[String.totalItems] + 1
        else:
            total_items = 1

    meta_dict = {
        String.totalItems: total_items,
    }
    upload_data_to_database(
        table_name=TableName.metaData,
        _id=meta_field,
        data=meta_dict,
    )
