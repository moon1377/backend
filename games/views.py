from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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
    board = game.get_board_as_list()

    if request.method == "POST" and request.user == game.owner:
        square = int(request.POST.get("square"))
        if board[square] == " ":

            
            token = "X" if game.active_player == 1 else "O"
            board[square] = token
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

    return render(request, "games/play.html", {"game": game, "board": board})


@login_required(login_url='users:login')
def close_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.user == game.owner:
        game.delete()
    return redirect("games:games_list")