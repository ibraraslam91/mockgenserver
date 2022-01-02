from django.contrib import admin

from .models import Project, Screen, Layer

class ScreenInLine(admin.TabularInline):
    model = Screen

class ProjectAdmin(admin.ModelAdmin):

    model = Project
    inlines = [ScreenInLine]

    list_display = ["id", "name", "added_by", "description"]


class ScreenAdmin(admin.ModelAdmin):

    model = Screen

    list_display = ["id", "name", "project"]


class LayerAdmin(admin.ModelAdmin):

    model = Layer

    list_display = ["id", "created_at", "screen"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Screen, ScreenAdmin)
admin.site.register(Layer, LayerAdmin)
