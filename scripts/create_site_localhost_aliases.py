# Create Site aliases for freshly loaded production database
# so portals are accessibles through http://[portal-name].localhost:8000
#
# Run like this, from ./manage.py shell
# %run scripts/create_site_localhost_aliases.py


from django.contrib.sites.models import Site

from multisite.models import Alias

for site in Site.objects.all():
    print(site.domain.split("."))
    hostname = site.domain.split(".")[0]
    staging_fqdn = f"{hostname}.localhost"
    Alias.objects.update_or_create(
        domain=staging_fqdn, defaults={"site": site, "redirect_to_canonical": False}
    )
