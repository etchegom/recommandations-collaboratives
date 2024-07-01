from typing import Any

from recoco.apps.projects.models import Project

from .models import DSResource


def find_ds_resource_for_project(project: Project) -> DSResource | None:
    # FIXME: find a DS resource elligible for the given project
    # for the moment, we return the only one for testing purpose
    return DSResource.objects.filter(
        name="demande-de-subvention-detr-dsil-2024-en-moselle"
    ).first()

    # conditions:
    # EDL à 100% ?
    # code postal correspond au département de la DS DETR  ?


def build_ds_data_from_project(
    project: Project, ds_resource: DSResource
) -> dict[str, Any]:
    # TODO: build the data to send to DS API
    if ds_resource.name == "demande-de-subvention-detr-dsil-2024-en-moselle":
        return {
            "champ_Q2hhbXAtMjk3MTQ0NA": project.name,
        }

    return {}
