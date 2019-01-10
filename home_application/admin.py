# -*- coding: utf-8 -*-

from home_application.models import T_C_SCRIPT

from django.contrib import admin


@admin.register(T_C_SCRIPT)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'script_content')
