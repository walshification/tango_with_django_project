from django.contrib import admin
from rango.models import Category, Page, UserProfile


class AdminPage(admin.ModelAdmin):

    list_display = ('title', 'category', 'url')


class AdminCategory(admin.ModelAdmin):

    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category, AdminCategory)
admin.site.register(Page, AdminPage)
admin.site.register(UserProfile)
