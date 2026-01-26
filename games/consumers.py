import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Game

class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_id = f"game_{self.room_id}"

        # unirse al grupo
        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )
        await self.accept()

        print(f"DEBUG WebSocket: Cliente conectado a sala {self.room_id}")

    async def disconnect(self, close_code):
        # salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )
        
        print(f"DEBUG WebSocket: Cliente desconectado de sala {self.room_id}")

    async def receive(self, text_data):
        message = json.loads(text_data)
        print(f"DEBUG WebSocket: Mensaje recibido: {message}")
        
        square = int(message.get("square"))
        player = int(message.get("player", 1))
        room_id = message.get("room_id")

        try:
            game = await database_sync_to_async(Game.objects.get)(id=room_id)
        except Game.DoesNotExist:
            print(f"DEBUG: Juego {room_id} no encontrado")
            return
            
        board = list(game.board)
        
        print(f"DEBUG: Jugador que mueve: {player}, Turno actual: {game.active_player}")

        # validación completa
        error_msg = None
        
        if player not in [1, 2]:
            error_msg = "Jugador inválido"
        elif board[square] != " ":
            error_msg = "Casilla ya ocupada"
        elif game.active_player != player:
            error_msg = f"No es tu turno. Es el turno del Jugador {game.active_player}"
        elif game.state != "active":
            error_msg = "El juego ya terminó"
        
        if error_msg:
            print(f"DEBUG: Movimiento rechazado - {error_msg}")
            game_data = {
                "board": list(game.board),
                "active_player": game.active_player,
                "state": game.state,
                "error": error_msg
            }
        else:
            # si el movimiento esta bien se hace
            symbol = "X" if player == 1 else "O"
            board[square] = symbol
            game.board = "".join(board)

            # verificamos el ganador
            win = game.check_winner()
            if win == "X":
                game.state = "won_X"
            elif win == "O":
                game.state = "won_O"
            elif win == "tie":
                game.state = "tie"
            else:
                # cambia turno
                game.active_player = 2 if game.active_player == 1 else 1

            await database_sync_to_async(game.save)()
            
            print(f"DEBUG: Movimiento aceptado. Nuevo turno: Jugador {game.active_player}")

            game_data = {
                "board": list(game.board),
                "active_player": game.active_player,
                "state": game.state,
                "error": None
            }

        # actualiza sala
        await self.channel_layer.group_send(
            self.room_group_id,
            {"type": "game_update", "data": game_data}
        )

    async def game_update(self, event):
        """Enviar actualización a todos los clientes conectados"""
        data = event["data"]
        await self.send(text_data=json.dumps({"my_data": data}))
        print(f"DEBUG: Actualización enviada a cliente: {data}")