from django.shortcuts import get_object_or_404, render

from .models import Players, Itemsequiped

def index(request):
	players = Players.objects.all()
	context = {
		'players': players,
	}
	return render(request, 'inspector/index.html', context)

def detail(request, player_id):
	player = get_object_or_404(Players, pk=player_id)
	items = list(Itemsequiped.objects.filter(idplayer=player_id))
	return render(request, 'inspector/detail.html', {'player': player, 'items': items})

def ausencias(request):
	return render(request, 'inspector/ausencias.html', {})
