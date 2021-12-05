from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import Follow

User = get_user_model()


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'user')
    empty_value_display = '-пусто-'


class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    empty_value_display = '-пусто-'


admin.site.unregister(User)

admin.site.register(User, MyUserAdmin)
admin.site.register(Follow, FollowAdmin)
