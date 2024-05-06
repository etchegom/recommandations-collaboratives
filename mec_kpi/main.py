from recoco.apps.projects.models import Project, ProjectMember
from datetime import timedelta, date
from django.db.models import Count, DecimalField, Q, ExpressionWrapper
from recoco.apps.tasks.models import Task
from recoco.apps.projects.models import ProjectSwitchtender
from django.db.models.query import QuerySet
from django.conf import settings

mec_site_id = 6


def _persist_sql_query(name: str, queryset: QuerySet):
    sql, params = queryset.query.sql_with_params()
    with open(settings.BASE_DIR.parent / "mec_kpi" / f"{name}.sql", "w") as f:
        f.write(f"{sql};")
        f.write(f"\n-- {params}")


def mec_metrics(nb_days: int = 7):

    for nb_days in [7, 14, 30]:
        print(f"Ces {nb_days} derniers jours:")
        last_n_days = date.today() - timedelta(days=nb_days)

        #
        # 1. CDP connectés au moins 1 fois
        #
        queryset = ProjectMember.objects.filter(
            is_owner=True,
            project__sites__pk=mec_site_id,
            member__last_login__date__gte=last_n_days,
        )
        _persist_sql_query(name="cdp_connectes", queryset=queryset)
        print(f"\t- Nombre de CDP connectés: {queryset.count()}")

        #
        # 2. Collectivités connectés au moins 1 fois
        #
        queryset = Project.objects.filter(sites__pk=mec_site_id).filter(
            last_members_activity_at__date__gte=last_n_days
        )
        _persist_sql_query(name="collectivites_connectees", queryset=queryset)
        print(f"\t- Nombre de collectivités connectées: {queryset.count()}")

        #
        # 3. Conseillers connectés au moins 1 fois
        #
        queryset = ProjectSwitchtender.objects.filter(site_id=mec_site_id).filter(
            switchtender__last_login__date__gte=last_n_days
        )
        _persist_sql_query(name="conseillers_connectees", queryset=queryset)
        print(f"\t- Nombre de conseillers connectés: {queryset.count()}")

        # 4. Nombre de projets déposés (30 derniers jours + cumulés)
        queryset = Project.objects.filter(sites__pk=mec_site_id).filter(
            created_on__date__gte=last_n_days
        )
        _persist_sql_query(name="projets_deposes", queryset=queryset)
        print(f"\t- Nombre de projets déposés: {queryset.count()}")

    #
    # 5. Nombre de recommandations par statut
    # Questions:
    # - Est-ce que toutes les tâches sont des recommandations ?
    #
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

    #
    # 6. Nombre d’interactions entre collectivités x conseillers (30 derniers jours + cumulés)
    #    (interaction = 1 conversation + 1 recommandation)
    #
    queryset = (
        Project.objects.filter(sites__pk=mec_site_id)
        .annotate(
            task_count=Count("tasks"),
            # count_switchtender__notes=Count("switchtenders"),
            # count_user__notes=Count("members"),
        )
        .filter(
            task_count__gt=0,
            # count_switchtender__notes__gt=0,
            # count_user__notes__gt=0,
        )
    )
    print(f"Nombre d'interactions: {queryset.count()}")


mec_metrics()
