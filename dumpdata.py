from django.core import serializers
import core.models


JSONSerializer = serializers.get_serializer("json")

with open("cinema_sites.json", "w") as out:
    JSONSerializer().serialize(core.models.SiteCinema.objects.all(), stream=out, indent=2)
    out.close()

with open("news_sites.json", "w") as out:
    JSONSerializer().serialize(core.models.SiteNews.objects.all(), stream=out, indent=2)
    out.close()