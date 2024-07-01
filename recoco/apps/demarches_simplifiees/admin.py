from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import DSFolder, DSResource
from .tasks import load_ds_resource_schema


@admin.register(DSResource)
class DSResourceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    actions = ("load_schema",)

    @admin.action(description="Charger le schéma publique de la démarche simplifiée")
    def load_schema_action(self, request: HttpRequest, queryset: QuerySet[DSResource]):
        for ds_resource in queryset:
            load_ds_resource_schema.delay(ds_resource.id)
            self.message_user(
                request,
                f"Tâche déclenchée pour la resource {ds_resource.name}.",
                messages.SUCCESS,
            )


@admin.register(DSFolder)
class DSFolderAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "ds_resource",
        "action",
        "dossier_id",
        "dossier_url",
        "dossier_number",
    )
    search_fields = (
        "project",
        "ds_resource",
        "dossier_id",
    )
