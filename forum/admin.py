from django.contrib import admin
from taggit_helpers.admin import TaggitStackedInline

from .models import (
            Profile,
            Project,
            CodeFile,
            SchematicsFile,
        )


class CodeFileInline(admin.TabularInline):
    model = CodeFile
    extra = 1


class SchematicsFileInline(admin.TabularInline):
    model = SchematicsFile
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
    ('Project Details', {'fields': ('title','description','owner','stars','gallery',)}),
    ('Collaborators', {'fields': ('collaborators',)}),
    ('External Links', {'fields': ('website','github','funding')}),
)
    inlines = [CodeFileInline, SchematicsFileInline, TaggitStackedInline, ]


admin.site.register(Profile)
admin.site.register(Project, ProjectAdmin)
admin.site.register(CodeFile)
admin.site.register(SchematicsFile)

