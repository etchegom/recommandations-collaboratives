from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.db.models import F, Count, Value
from django.db.models.functions import Coalesce

# Number of switchtenders connections per day for a given site


def get_queryset(site_id: int) -> QuerySet:
    return (
        get_user_model()
        .objects.filter(projects_switchtended_on_site__site_id=site_id)
        .annotate(day=F("last_login__date"))
        .values("day")
        .order_by("-day")
        .annotate(count=Coalesce(Count("id", distinct=True), Value(0)))
    )
