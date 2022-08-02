from django.urls import path, include
from account.api.views import accounts_view, account_register, account_login, account_logout, update_account, user_delete, deactivate_account_view, activate_account_view


app_name = 'account_api'

urlpatterns = [
    path('account/', accounts_view),
    path('account_update/', update_account),
    path('register/', account_register),
    path('login', account_login),
    path('logout/', account_logout),
    path('delete/<int:pk>', user_delete),
    path('deactivate/<int:pk>', deactivate_account_view),
    path('activate/<int:pk>', activate_account_view),
]



