from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, FacturaSubida
from django.utils.html import format_html

admin.site.register(Usuario, UserAdmin)

@admin.register(FacturaSubida)
class FacturaSubidaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'numero', 'descripcion', 'fecha', 'categoria', 'monto', 'archivo_link')
    readonly_fields = ('archivo_preview',)
    search_fields = ('numero', 'descripcion', 'usuario__username', 'nit')
    list_filter = ('categoria', 'fecha', 'usuario')
    fields = ('archivo_preview', 'usuario', 'descripcion', 'numero', 'nit', 'fecha', 'categoria', 'monto', 'tipo_monto', 'archivo', 'fecha_subida')

    def archivo_link(self, obj):
        if obj.archivo:
            url = obj.archivo.url
            if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                return format_html('<a href="{}" target="_blank"><img src="{}" style="max-height:50px; max-width:70px; border-radius:4px;" /></a>', url, url)
            return format_html('<a href="{}" target="_blank">Ver archivo</a>', url)
        return "Sin archivo"
    archivo_link.short_description = 'Archivo'

    def archivo_preview(self, obj):
        if obj.archivo and obj.archivo.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return format_html('<img src="{}" style="max-height:150px; max-width:200px;" />', obj.archivo.url)
        elif obj.archivo:
            return format_html('<a href="{}" target="_blank">Descargar archivo</a>', obj.archivo.url)
        return "Sin archivo"
    archivo_preview.short_description = 'Vista previa archivo'
