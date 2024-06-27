from django.db import models
from model_utils.models import TimeStampedModel

from .utils import dict_to_hash


class DemarcheSimplifiee(TimeStampedModel):
    ds_id = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    description = models.TextField()

    # TODO: register fields we can pre-fill and make them match with project fields somehow
    fields = models.JSONField()

    class Meta:
        verbose_name = "Démarche simplifiée"
        verbose_name_plural = "Démarches simplifiées"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class DossierPreRempli(TimeStampedModel):
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
    )
    demarche = models.ForeignKey(
        "demarches_simplifies.DemarcheSimplifiee",
        on_delete=models.CASCADE,
    )

    dossier_id = models.CharField(max_length=255)
    dossier_url = models.URLField()
    dossier_number = models.IntegerField()

    data = models.JSONField()
    hash_data = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Dossier pré-rempli"
        verbose_name_plural = "Dossiers pré-remplis"
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["project", "demarche", "hash_data"]),
        ]

    def __str__(self) -> str:
        return self.dossier_id

    def save(self, *args, **kwargs):
        self.hash_data = dict_to_hash(dict(self.data))
        super().save(*args, **kwargs)
