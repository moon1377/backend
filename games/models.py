from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    room_name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.CharField(max_length=9, default=" " * 9) 
    active_player = models.IntegerField(default=1) 
    state = models.CharField(max_length=20, default="active")  
   

    def __str__(self):
        return self.room_name


    def get_board_as_list(self):
        return list(self.board)

    def check_winner(self):
        b = self.board
        wins = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for a,b1,c in wins:
            if b[a] == b[b1] == b[c] and b[a] != " ":
                return b[a] 
        if " " not in b:
            return "tie"
        return None