from django.contrib import admin
from .models import *



admin.site.register(Customer)
admin.site.register(Department)
admin.site.register(Workrole)
admin.site.register(User)
admin.site.register(Ticket)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username','first_name', "last_name","email","phone"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)



