from recoco.apps.projects.models import Project, ProjectMember
from datetime import timedelta, date
from django.db.models import Count, DecimalField, Q, ExpressionWrapper
from recoco.apps.tasks.models import Task
from recoco.apps.projects.models import ProjectSwitchtender

mec_site_id = 6


def mec_metrics(nb_days: int = 7):

    for nb_days in [7, 14, 30]:
        print(f"Ces {nb_days} derniers jours:")
        last_n_days = date.today() - timedelta(days=nb_days)

        # 1. CDP connectés au moins 1 fois
        qs = ProjectMember.objects.filter(
            is_owner=True,
            project__sites__pk=mec_site_id,
            member__last_login__date__gte=last_n_days,
        )
        print(f"\t- Nombre de CDP connectés: {qs.count()}")

        # 2. Collectivités connectés au moins 1 fois
        qs = Project.objects.filter(sites__pk=mec_site_id).filter(
            last_members_activity_at__date__gte=last_n_days
        )
        print(f"\t- Nombre de collectivités connectées: {qs.count()}")

        # 3. Conseillers connectés au moins 1 fois
        qs = ProjectSwitchtender.objects.filter(site_id=mec_site_id).filter(
            switchtender__last_login__date__gte=last_n_days
        )
        print(f"\t- Nombre de conseillers connectés: {qs.count()}")

        # 4. Nombre de projets déposés (30 derniers jours + cumulés)
        qs = Project.objects.filter(sites__pk=mec_site_id).filter(
            created_on__date__gte=last_n_days
        )
        print(f"\t- Nombre de projets déposés: {qs.count()}")

    # 5. Nombre de recommandations par statut
    print("Pourcentage de recommandations par statut de projet:")
    agg = Task.objects.filter(site__pk=mec_site_id).aggregate(
        **{
            f"{status.lower()}": ExpressionWrapper(
                expression=Count("pk", filter=Q(project__status=status))
                * 100
                / Count("pk"),
                output_field=DecimalField(max_digits=30, decimal_places=4),
            )
            for status in [s[0] for s in Project.PROJECT_STATES]
        }
    )
    for k, v in agg.items():
        print(f"\t- Statut {k.upper()}: {v}%")

    # 6. % / statut
    print("Pourcentage de projets par statut:")
    agg = Project.objects.filter(sites__pk=mec_site_id).aggregate(
        **{
            f"{status.lower()}": ExpressionWrapper(
                expression=Count("pk", filter=Q(status=status)) * 100 / Count("pk"),
                output_field=DecimalField(max_digits=30, decimal_places=4),
            )
            for status in [s[0] for s in Project.PROJECT_STATES]
        }
    )
    for k, v in agg.items():
        print(f"\t- Statut {k.upper()}: {v}%")

    # 7. Nombre d’interactions entre collectivités x conseillers (30 derniers jours + cumulés)
    #    (interaction = 1 conversation + 1 recommandation)
    # TODO


mec_metrics()
