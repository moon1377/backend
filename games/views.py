from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json  
from .models import Game
from .forms import NewGameForm

@login_required(login_url='users:login') 
def games_list(request):
    games = Game.objects.all() # obtiene todas las partidas
    
    if request.method == "POST":
        form = NewGameForm(request.POST) # crea el formulario con los datos
        
        #mira si es valido. Mira si
        if form.is_valid():
            new_game = form.save(commit=False)
            new_game.owner = request.user # asigna el usuario
            new_game.save()
            return redirect("games:games_list")
    else:
        form = NewGameForm() # sino crea el formulario vacio
    
    return render(request, "games/game.html", {"games": games, "form": form}) 

@login_required(login_url='users:login')
def play_game(request, game_id):
    game = get_object_or_404(Game, id=game_id) # busca juego o da error
    
    board = list(game.board) #convierte el string del tablero en lista
    
    if len(board) != 9:
        board = [" " for _ in range(9)]

    # asignar jugador
    session_key = f'game_{game_id}_player'
    
    if request.user == game.owner:
        # el creador es el 1
        player_number = 1
        player_symbol = 'X'
        request.session[session_key] = 1
        print(f"DEBUG: {request.user.username} es OWNER -> Jugador 1")
    else:
        # para otro el 2
        # vemos si ya tiene una key
        if session_key in request.session:
            player_number = request.session[session_key]
            print(f"DEBUG: {request.user.username} ya tiene asignado -> Jugador {player_number}")
            
        # si es la primera vez que entra se le asigna el 2
        else: 
            
            player_number = 2
            request.session[session_key] = 2
            print(f"DEBUG: {request.user.username} nuevo -> Jugador 2")
        
        player_symbol = 'O' if player_number == 2 else 'X'

    # guarda para play
    game_data = {
        'id': game_id,
        'board': board,
        'state': game.state,
        'active_player': game.active_player,
        'player_number': player_number,
        'player_symbol': player_symbol,
        'is_owner': request.user == game.owner,
        'owner': game.owner.username if game.owner else None
    }

    print(f"DEBUG game_data final: {game_data}")

    return render(request, "games/play.html", {
        "game": game, 
        "board": board,  
        "game_data": json.dumps(game_data)
    })

@login_required(login_url='users:login')
def close_game(request, game_id):
    game = get_object_or_404(Game, id=game_id) #busca partida
    if request.user == game.owner: #solo el dueño puede borrar
        game.delete()
    return redirect("games:games_list")