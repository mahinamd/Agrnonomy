from django.contrib import admin
from .models import Category, Subcategory, Information, DiseaseProblem


# Category admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', 'image', 'name_bn', 'name_en')
    search_fields = ('id', 'created', 'last_modified', 'name_bn', 'name_en')
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified')


admin.site.register(Category, CategoryAdmin)


# Subcategory admin
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', 'category', 'image', 'name_bn', 'name_en')
    search_fields = ('id', 'created', 'last_modified', 'category', 'name_bn', 'name_en')
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified', 'category')


admin.site.register(Subcategory, SubcategoryAdmin)


# Information admin
class InformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', 'subcategory', "name_bn", "details_bn", "name_en", "details_en")
    search_fields = ('id', 'created', 'last_modified', 'subcategory', "name_bn", "details_bn", "name_en", "details_en")
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified')


admin.site.register(Information, InformationAdmin)


# Disease/Problem admin
class DiseaseProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'last_modified', 'subcategory', 'image', "name_bn", "insects_causes_bn", "solution_bn", "warning_bn", "name_en", "insects_causes_en", "solution_en", "warning_en")
    search_fields = ('id', 'created', 'last_modified', 'subcategory', "name_bn", "name_en")
    readonly_fields = ('id', 'created', 'last_modified')
    ordering = ('id', 'created', 'last_modified')


admin.site.register(DiseaseProblem, DiseaseProblemAdmin)
