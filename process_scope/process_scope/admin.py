from django.contrib import admin
from django import forms
from .models import ProcessTaxonomy, CountryList, ProcessValue

@admin.register(ProcessTaxonomy)
class ProcessTaxonomyAdmin(admin.ModelAdmin):
    list_display = ('category_level1', 'process_group_level2', 'process_level3', 'subprocess_level4', 'activity_level5', 'task_level6', 'standard_local')
    search_fields = ('category_level1', 'process_group_level2', 'process_level3', 'subprocess_level4', 'activity_level5', 'task_level6')
    list_filter = ('standard_local',)

@admin.register(CountryList)
class CountryListAdmin(admin.ModelAdmin):
    list_display = ('country_description', 'cluster', 'region')
    search_fields = ('country_description', 'cluster', 'region')



@admin.register(ProcessValue)

class ProcessValueAdmin(admin.ModelAdmin):
    list_display = ('display_process_taxonomy', 'display_country', 'value')
    search_fields = ('process_taxonomy__category_level1', 'process_taxonomy__process_group_level2', 'country__country_description')
    list_filter = ('process_taxonomy__standard_local',)

    def display_country(self, obj):
        return obj.country.country_description

    def display_process_taxonomy(self, obj):
        return f"{obj.process_taxonomy.category_level1} > {obj.process_taxonomy.process_group_level2} > {obj.process_taxonomy.process_level3} > {obj.process_taxonomy.subprocess_level4} > {obj.process_taxonomy.activity_level5} > {obj.process_taxonomy.task_level6} > {obj.process_taxonomy.standard_local}"

    display_country.short_description = 'Country'
    display_process_taxonomy.short_description = 'Process Taxonomy'

