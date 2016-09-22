from django.contrib import admin

from .models import Player, Item, ItemStats, PlayerItem, Artifact, Relic, Trait, ArtifactRelic

# Register your models here.

admin.site.register(Player)
admin.site.register(Item)
admin.site.register(ItemStats)
admin.site.register(PlayerItem)
admin.site.register(Artifact)
admin.site.register(Relic)
admin.site.register(Trait)
admin.site.register(ArtifactRelic)

