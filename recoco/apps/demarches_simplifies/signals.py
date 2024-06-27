from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from recoco.apps.projects.models import Project
from recoco.apps.survey.models import Answer

from .tasks import call_ds_api_preremplir


def _is_project_ready_for_ds(project: Project) -> bool:
    # TODO: check if project is in a state that can be sent to DS
    return True


@receiver(post_save, sender=Project)
def trigger_ds_from_project(sender: Any, instance: Project, created: bool, **kwargs):
    if _is_project_ready_for_ds(instance):
        call_ds_api_preremplir(project_id=instance.id)


@receiver(post_save, sender=Answer)
def trigger_ds_from_answer(sender: Any, instance: Answer, created: bool, **kwargs):
    project = instance.session.project
    if _is_project_ready_for_ds(project):
        call_ds_api_preremplir(project_id=project.id)
