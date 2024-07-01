import requests
from celery import shared_task
from django.conf import settings

from recoco.apps.projects.models import Project

from .models import DSFolder, DSResource
from .services import build_ds_data_from_project, find_ds_resource_for_project
from .utils import hash_data


# TODO: handle task retry
@shared_task
def load_ds_resource_schema(ds_resource_id: int):
    try:
        ds_resource = DSResource.objects.get(id=ds_resource_id)
    except DSResource.DoesNotExist:
        # TODO: handle error
        return

    resp = requests.get(
        url=f"{settings.DS_BASE_URL}/preremplir/{ds_resource.name}/schema",
        timeout=30,
    )
    if resp.status_code != 200:
        # TODO: handle error
        return

    ds_resource.schema = resp.json()
    ds_resource.save()


# TODO: handle task retry
@shared_task
def update_or_create_ds_action(project_id: int):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        # TODO: handle error
        return

    ds_resource: DSResource = find_ds_resource_for_project(project=project)
    if ds_resource is None or ds_resource.number is None:
        return

    content = build_ds_data_from_project(
        project=project,
        ds_resource=ds_resource,
    )
    if not len(content):
        return

    if DSFolder.objects.filter(
        project=project,
        ds_resource=ds_resource,
        content_hash=hash_data(content),
    ).exists():
        return

    resp = requests.post(
        url=f"{settings.DS_API_BASE_URL}/demarches/{ds_resource.number}/dossiers",
        json=content,
        timeout=30,
    )
    if resp.status_code != 201:
        # TODO: handle error
        return

    ds_folder, _ = DSFolder.objects.update_or_create(
        project=project,
        ds_resource=ds_resource,
        defaults={
            "content": content,
            **resp.json(),
        },
    )
    ds_folder.update_or_create_action()
