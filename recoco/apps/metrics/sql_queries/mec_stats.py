from recoco.apps.projects.models import Project, ProjectMember
from recoco.apps.addressbook.models import Organization
from datetime import timedelta, date
from django.db.models import Count, DecimalField, Q, ExpressionWrapper
from recoco.apps.home.models import UserProfile

mec_site_id = 6

# mec_site = Site.objects.get(pk=mec_site_id)


def list_organizations():
    organizations = Organization.objects.filter(sites__pk=mec_site_id)
    for org in organizations:
        print(org.name)


def list_users():
    mec_users = UserProfile.objects.filter(
        sites__pk=mec_site_id, organization__isnull=False
    )
    # for user in mec_users:
    #     print(
    #         f"{user.user.username}, {user.organization.name}, {user.organization_position}"
    #     )

    qs = mec_users.aggregate(count_org=Count("organization"))
    print(qs)


def cdp_metrics(nb_days: int = 7):

    for nb_days in [7, 14, 30]:
        last_n_days = date.today() - timedelta(days=nb_days)

        # 1. CDP connectés au moins 1 fois
        qs = ProjectMember.objects.filter(
            is_owner=True,
            project__sites__pk=mec_site_id,
            member__last_login__date__gte=last_n_days,
        )
        print(f"Nombre de CDP connectés ces {nb_days} derniers jours: {qs.count()}")

        # 2. Collectivités connectés au moins 1 fois
        qs = Project.objects.filter(sites__pk=mec_site_id).filter(
            last_members_activity_at__date__gte=last_n_days
        )
        print(
            f"Nombre de collectivités connectés ces {nb_days} derniers jours: {qs.count()}"
        )

        # 3. Conseillers connectés au moins 1 fois
        # TODO

    # 4. Nombre de projets déposés (30 derniers jours + cumulés)
    # TODO

    # 5. Nombre de recommandations
    # TODO

    # 6. % / statut
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
        print(f"Pourcentage de projets en statut {k.upper()}: {v}%")

    # 7. Nombre d’interactions entre collectivités x conseillers (30 derniers jours + cumulés)
    #    (interaction = 1 conversation + 1 recommandation)
    # TODO


cdp_metrics()
