from datetime import datetime, timedelta

from google.cloud.firestore_v1 import FieldFilter

from .const import String
from .firebaseConfig import *

DESCENDING = "DESCENDING"


def upload_data_to_database(table_name, data, _id):
    db.collection(table_name).document(_id).set(data)


def delete_data_from_database(table_name, _id):
    db.collection(table_name).document(_id).delete()


def get_data_by_id_from_database(table_name, _id):
    return db.collection(table_name).document(_id).get().to_dict()


def get_date_by_other_field_from_database(table_name, field_name, value):
    return db.collection(table_name).where(filter=FieldFilter(field_name, "==", value)).stream()


def get_all_data_from_database(table_name):
    return db.collection(table_name).order_by(String.createAt, direction=DESCENDING)


def update_data_by_id_from_database(table_name, data):
    db.collection(table_name).document(data[String.id]).update(data)


def upload_file_to_database(file_path, temp_file_path):
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    blob.upload_from_filename(temp_file_path)
    expiration_time = datetime.utcnow() + timedelta(days=365 * 100)
    return blob.generate_signed_url(expiration=expiration_time)
