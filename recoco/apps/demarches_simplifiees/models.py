from django.db import models
from model_utils.models import TimeStampedModel

from recoco.apps.projects.models import Project
from recoco.apps.resources.models import Resource
from recoco.apps.tasks.models import Task

from .utils import dict_to_hash


class DSResource(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    schema = models.JSONField(default=dict, null=True, blank=True)
    resource = models.ForeignKey(
        Resource, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Démarche simplifiée"
        verbose_name_plural = "Démarches simplifiées"
        ordering = ["name"]

    def __str__(self):
        return self.name

    # TODO: implement properties to get schema fields


class DSFolder(TimeStampedModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    ds_resource = models.ForeignKey(
        DSResource,
        on_delete=models.CASCADE,
    )

    action = models.ForeignKey(
        Task,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    dossier_id = models.CharField(max_length=255)
    dossier_url = models.URLField()
    dossier_number = models.IntegerField()

    content = models.JSONField()
    content_hash = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Dossier de Démarches Simplifiées"
        verbose_name_plural = "Dossiers de Démarches Simplifiées"
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["project", "ds_resource", "content_hash"]),
        ]

    def __str__(self) -> str:
        return self.dossier_id

    def save(self, *args, **kwargs):
        self.content_hash = dict_to_hash(dict(self.content))
        super().save(*args, **kwargs)

    def update_or_create_action(self):
        pass
        # if self.action:
        #     pass
