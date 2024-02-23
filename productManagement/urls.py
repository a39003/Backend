from django.urls import path
from . import views
from .const import RouteName, Param, VariableName
from .models import *

urlpatterns = [
    # Auth
    path(f'{RouteName.login}/', views.login),
    path(f'{RouteName.logout}/', views.logout),
    path(f'{RouteName.signup}/', views.signup),

    # Product
    path(f'{RouteName.products}/', views.create_items, {
        VariableName.class_param: Param.products,
        VariableName.class_type: Product
    }),
    path(f'{RouteName.products}/page=<int:page_number>/items=<int:items_per_page>', views.get_list_item, {
        VariableName.class_param: Param.products
    }),
    path(f'{RouteName.products}/page=<int:page_number>/', views.get_list_item, {
        VariableName.item_per_page: 5,
        VariableName.class_param: Param.products
    }),
    path(f'{RouteName.products}/id=<str:id>', views.get_put_delete_item_by_id, {
        VariableName.class_param: Param.products,
        VariableName.class_type: Product
    }),

    # Category
    path(f'{RouteName.category}/', views.create_items, {
        VariableName.class_param: Param.category,
        VariableName.class_type: Category
    }),
    path(f'{RouteName.category}/page=<int:page_number>/items=<int:items_per_page>', views.get_list_item, {
        VariableName.class_param: Param.category
    }),
    path(f'{RouteName.category}/page=<int:page_number>/', views.get_list_item, {
        VariableName.item_per_page: 5,
        VariableName.class_param: Param.category
    }),
    path(f'{RouteName.category}/id=<str:id>', views.get_put_delete_item_by_id, {
        VariableName.class_param: Param.category,
        VariableName.class_type: Category
    }),

    # User
    path(f'{RouteName.users}/email=<str:email>', views.get_user_by_email)
]
