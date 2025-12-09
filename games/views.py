from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json  
from .models import Game
from .forms import NewGameForm

@login_required(login_url='users:login')
def games_list(request):
    games = Game.objects.all()
    
    if request.method == "POST":
        form = NewGameForm(request.POST)
        if form.is_valid():
            new_game = form.save(commit=False)
            new_game.owner = request.user
            new_game.save()
            return redirect("games:games_list")
    else:
        form = NewGameForm()
    
    return render(request, "games/game.html", {"games": games, "form": form})

@login_required(login_url='users:login')
def play_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    board = list(game.board)
    
    if len(board) != 9:
        board = [" " for _ in range(9)]

    game_data = {
        'id': game_id,
        'player_number': 1 if request.user == game.owner else 2,
        'player_symbol': 'X' if request.user == game.owner else 'O',
        'is_owner': request.user == game.owner
    }

    if request.method == "POST":
        square = request.POST.get("square")
        
        if square is None:
            return render(request, "games/play.html", {
                "game": game, 
                "board": board,
                "game_data": json.dumps(game_data)
            })
        
        try:
            square = int(square)
            if not (0 <= square <= 8):
                raise ValueError
        except (ValueError, TypeError):
            return render(request, "games/play.html", {
                "game": game, 
                "board": board,
                "error": "Invalid move selection!",
                "game_data": json.dumps(game_data)
            })
        
        is_owner = request.user == game.owner
        player_symbol = "X" if is_owner else "O"
        current_turn_symbol = "X" if game.active_player == 1 else "O"
        
        if player_symbol != current_turn_symbol:
            return render(request, "games/play.html", {
                "game": game, 
                "board": board,
                "error": f"Not your turn! It's Player {game.active_player}'s turn ({current_turn_symbol})",
                "game_data": json.dumps(game_data)
            })
        
        if game.board[square] != " ":
            return render(request, "games/play.html", {
                "game": game, 
                "board": board,
                "error": "That cell is already taken!",
                "game_data": json.dumps(game_data)
            })
        
        board[square] = player_symbol
 
        game.board = "".join(board)
        
        win = game.check_winner()  
        
        if win == "X":
            game.state = "won_X"
        elif win == "O":
            game.state = "won_O"
        elif win == "tie":
            game.state = "tie"
        else:

            game.active_player = 2 if game.active_player == 1 else 1
        
        game.save()
        return redirect("games:play_game", game_id=game_id)

    return render(request, "games/play.html", {
        "game": game, 
        "board": board,  
        "game_data": json.dumps(game_data)
    })

@login_required(login_url='users:login')
def close_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.user == game.owner:
        game.delete()
    return redirect("games:games_list")