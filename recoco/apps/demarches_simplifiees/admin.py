from django.contrib import admin, messages
from django.db.models import JSONField, QuerySet
from django.http import HttpRequest
from django_json_widget.widgets import JSONEditorWidget

from .models import DSFolder, DSResource
from .tasks import load_ds_resource_schema


@admin.register(DSResource)
class DSResourceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    actions = ("load_schema",)

    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }

    @admin.action(description="Charger le schéma publique de la démarche simplifiée")
    def load_schema_action(self, request: HttpRequest, queryset: QuerySet[DSResource]):
        for ds_resource in queryset:
            load_ds_resource_schema.delay(ds_resource.id)
            self.message_user(
                request,
                f"Tâche déclenchée pour la resource '{ds_resource.name}'.",
                messages.SUCCESS,
            )


@admin.register(DSFolder)
class DSFolderAdmin(admin.ModelAdmin):
    list_display = (
        "dossier_id",
        "project",
        "ds_resource",
        "action",
    )

    search_fields = (
        "project",
        "ds_resource",
        "dossier_id",
    )

    readonly_fields = (
        "project",
        "action",
        "dossier_id",
        "dossier_url",
        "dossier_number",
        "dossier_prefill_token",
        "state",
    )

    actions = ("update_or_create_action",)

    @admin.action(
        description="Créer ou mettre à jour l'action associée au dossier pré-rempli"
    )
    def update_or_create_action(
        self, request: HttpRequest, queryset: QuerySet[DSResource]
    ):
        for ds_folder in queryset:
            ds_folder.update_or_create_action()
            self.message_user(
                request,
                f"Action créée ou mise à jour pour le dossier '{ds_folder.dossier_id}'.",
                messages.SUCCESS,
            )
