from django.contrib import admin
from account.models import Account, MyAccountManage


class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'user_name')
    list_display_links = ('id', 'email')
    search_fields = ('id', 'full_name', 'user_name', 'phone_number')
    list_filter = ('id',)


admin.site.register(Account, TodoAdmin)



