class TableName:
    product = "Products"
    metaData = "MetaData"
    category = "Category"
    users = "Users"


class Method:
    post = "POST"
    get = "GET"
    put = "PUT"
    delete = "DELETE"


class ResponseTitle:
    error = "error"
    message = "message"


class ResponseMessage:
    method_not_allowed = "Method_not_allowed"
    delete_success = "Delete success"
    element_not_found = "Element not found"
    not_correct_email_or_password = "Not correct email or password"
    login_success = "Login success"
    not_authenticated = "Not authenticated"
    logout_success = "Logout success"
    signup_success = "Signup success"
    greater_than_total_page = "The page number must be less or equal than the total"
    less_than_0 = "The page number must be greater than 0"
    list_is_empty = "List data is empty"
    item_per_page_not_valid = "The page number must be greater than 0"
    element_exists = "Element already exists"
    email_exists = "Email already exists"
    no_data_provided = "No data provided"


class String:
    token = "idToken"
    email = "email"
    password = "password"
    authorization = "Authorization"
    data = "data"
    no_user_found = "No user record found"
    is_admin = "is_admin"
    table_fields = "tableFields"
    table_name = "tableName"
    meta_data = "metaData"
    class_type = "classType"
    required_fields = "requiredFields"
    check_distinct = "check_distinct"
    distinct_fields = "distinct_fields"

    # Product
    id = "id"
    name = "name"
    description = "description"
    unitPrice = "unitPrice"
    quantity = "quantity"
    code = "code"
    image = "image"
    category = "category"
    createAt = "createAt"
    productOrigin = "productOrigin"
    provider = "provider"
    rating = "rating"
    updateAt = "updateAt"

    # MetaData
    totalItems = "totalItems"
    itemsPerPage = "itemsPerPage"
    currentPage = "currentPage"
    totalPages = "totalPages"


class TableField:
    productsMetaData = "productsMetaData"
    categoryMetaData = "categoryMetaData"
    products = [
        String.id,
        String.name,
        String.description,
        String.image,
        String.unitPrice,
        String.quantity,
        String.category,
        String.productOrigin,
        String.provider,
        String.rating,
        String.createAt,
        String.updateAt,
    ]
    categories = [
        String.id,
        String.name,
        String.createAt,
        String.updateAt,
    ]


class RequiredField:
    products = [
        String.name,
        String.image,
        String.unitPrice,
        String.quantity,
        String.productOrigin,
        String.provider,
        String.category,
    ]
    categories = [
        String.name,
    ]


class RouteName:
    products = "products"
    login = "login"
    logout = "logout"
    category = "category"
    signup = "signup"
    users = "users"


class VariableName:
    class_param = "class_params"
    class_type = "class_type"
    item_per_page = "item_per_page"


class Param:
    products = {
        String.table_fields: TableField.products,
        String.table_name: TableName.product,
        String.meta_data: TableField.productsMetaData,
        String.required_fields: RequiredField.products,
        String.check_distinct: False,
        String.distinct_fields: None,
    }
    category = {
        String.table_fields: TableField.categories,
        String.table_name: TableName.category,
        String.meta_data: TableField.categoryMetaData,
        String.required_fields: RequiredField.categories,
        String.check_distinct: True,
        String.distinct_fields: String.name,
    }
