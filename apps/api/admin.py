from django.contrib import admin
from .models import Parameter, Interpretation

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    readonly_fields = ('name', 'description')
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Interpretation)
class InterpretationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    readonly_fields = ('user', 'dream', 'interpretation', 'created_at')
    search_fields = ('user', 'dream', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False