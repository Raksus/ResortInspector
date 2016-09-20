from django.shortcuts import get_object_or_404, render

from .models import Player, Item

def index(request):
	players = Player.objects.all()
	context = {
		'players': players,
	}
	return render(request, 'inspector/index.html', context)

def detail(request, player_id):
	player = get_object_or_404(Player, pk=player_id)
	items = list(PlayerItem.objects.filter(idplayer=player_id))
	return render(request, 'inspector/detail.html', {'player': player, 'items': items})

def ausencias(request):
	return render(request, 'inspector/ausencias.html', {})
