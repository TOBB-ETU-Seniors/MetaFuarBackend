from django.urls import path

from . import views

urlpatterns = [path('account',views.account,name='account'),
               path("isUsernameAvailable", views.isUsernameAvailable, name="isUsernameAvailable"),
               path("create_lobby", views.create_lobby, name="create_lobby"),
               path("delete_lobby", views.delete_lobby, name="delete_lobby"),
               path("join_lobby", views.join_lobby, name="join_lobby"),
               path("exit_lobby", views.exit_lobby, name="exit_lobby"),
               path("update_lobby", views.update_lobby, name="update_lobby"),
               path("get_fair_items", views.get_fair_items, name="get_fair_items"),
               path("get_item", views.get_item, name="get_item"),
               path("add_to_users_inventory", views.add_to_users_inventory, name="add_to_users_inventory"),
               path("add_to_inventory", views.add_to_inventory, name="add_to_inventory"),
               path("remove_item_users_inventory", views.remove_item_users_inventory, name="remove_item_users_inventory"),
               path("remove_item_inventory", views.remove_item_inventory, name="remove_item_inventory"),
               path("update_user_balance", views.update_user_balance, name="update_user_balance"),
               path("verify_code", views.verify_code, name="verify_code"),
               path("get_inventory", views.get_inventory, name="get_inventory"),
               path(".well-known/pki-validation/73A6AC1E4BBCA20FB933723456E0208C.txt", views.sslverif, name="sslverif")]