import socket
import threading
import protocol
import random

class Game:
    def __init__(self, game_capacity):
        self.game_start = False
        self.game_capacity = int(game_capacity)
        self.numPlayers = 0
        self.police_players = []   #list with sock and addres
        self.robber_players = []   #list with sock and addres

    def add_player(self, player):
        if len(self.police_players) < self.game_capacity//2:
            self.police_players.append(player)
            self.numPlayers += 1

        elif len(self.robber_players) < self.game_capacity//2:
            self.police_players.append(player)
            self.numPlayers += 1

        if self.game_capacity == self.numPlayers:
            self.game_start = True

    def remove_player(self, player):
        if player in self.police_players:
            self.police_players.remove(player)
            self.numPlayers -= 1

        elif player in self.robber_players:
            self.robber_players.remove(player)
            self.numPlayers -= 1

    def is_empty(self):
        return self.numPlayers == 0

    def check_player_police(self, player):
        return player in self.police_players


class GameHandler:
    def __init__(self):
        self.games = []

    def add_player(self, player, game_capacity):
        for game in self.games:
            #add to see the dont play game (add to if not self.game_start)
            if game_capacity == game.game_capacity and game.numPlayers < game.game_capacity:
                game.add_player(player)
                return

        new_game = Game(game_capacity)
        new_game.add_player(player)
        self.games.append(new_game)

    def remove_player(self, player):
        for game in self.games:
            game.remove_player(player)

            if game.is_empty():
                self.games.remove(game)
                break

    def get_game(self):
        return self.games

    def check_player_game(self, player):
        for game in self.games:
            if player in game.police_players or player in game.robber_players:
                return game

    def remove_game(self, game):
        self.games.remove(game)

    def check_start_game(self, player):
        game = self.check_player_game(player)
        return game.game_start

    def get_first_pos(self, player):
        game = self.check_player_game(player)
        if game.check_player_police(player):
            posx = random.randint(15, 24)
            posy = 1
            posz = random.randint(15, 24)

        else:
            posx = random.randint(-15, -24)
            posy = 1
            posz = random.randint(-15, -24)
        return posx, posy, posz

    def check_length(self):
        return len(self.games)


# def handle_client(client, clients, index_msg):
#     while True:
#         try:
#             # print(len(clients))
#             # print(index_msg)
#             if(len(clients) == 2):
#                 if(index_msg == 0):
#                     protocol.send_with_size(client[0], 'OK')
#
#                 else:
#                     data = protocol.recv_by_size(client[0])
#                     if not data:
#                         break
#
#                     if 'EXIT' in data:
#                         print(f'Client {client[1]} disconnected')
#                         client[0].close()
#                         clients.remove(client)
#                         print("exittttttt")
#                         for c in clients:
#                             protocol.send_with_size(c[0], 'EXIT')
#                             clients.remove(c)
#                             print(f'Client {c[1]} disconnected')
#                         break
#                     # Forward the message to other clients
#                     for c in clients:
#                         if c != client:
#                             protocol.send_with_size(c[0], data)
#                             # print(f"From {client[1]} to {c[1]} data " + data)
#
#                 index_msg += 1
#         except ConnectionResetError:
#             print(f'Client {client[1]} hard disconnected')
#             client[0].close()
#             clients.remove(client)
#             for c in clients:
#                 protocol.send_with_size(c[0], 'Exit')
#                 clients.remove(c)
#                 print(f'Client {c[1]} disconnected')
#             break

# def client_game_capacity_recv(client):
#     while True:
#         data = protocol.recv_by_size(client)
#         if data:
#             #RCGC = recv game capacity
#             if data[:4] == "SDGC":
#                 return data.split(',')[1]

# def handle_request(client, data):
#     if data[:4] == "RCGC":
#         protocol.send_with_size(client[0], data)


def remove_game(client, games):
    game = games.check_player_game(client)
    for player in game.police_players + game.robber_players:
        print(f'Client {player[0]} disconnected')
        protocol.send_with_size(player[0], 'EXIT')
        handle_client(player, 'EXIT')
    games.remove_game(game)
    print('remove game!')

def send_player_move(game, client, data):
    for player in game.police_players + game.robber_players:
        if player != client:
            protocol.send_with_size(player[0],data)

def handle_client(client, data):
    global games
    while True:
            if not data:
                try:
                    data = protocol.recv_by_size(client[0])

                except socket.timeout:
                    # Handle timeout
                    # print("Socket timeout occurred")
                    continue

                except ConnectionResetError:
                    # Handle connection reset by peer
                    # print("Connection reset by peer")
                    continue


            if data:
                #RCGC = recv game capacity
                if data[:4] == "SDGC":
                    game_capacity = data.split(',')[1]
                    games.add_player(client, int(game_capacity))
                    check_start_game = games.check_start_game(client)
                    while not check_start_game:
                        check_start_game = games.check_start_game(client)
                    posx, posy, posz = games.get_first_pos(client)
                    protocol.send_with_size(client[0], f'STGM,{posx},{posy},{posz}')

                elif data[:4] == 'EXIT':
                    print(f'Client {client[1]} disconnected')
                    client[0].close()
                    games.remove_player(client)

                #ENMP = Enemy position
                elif data[:4] == "ENMP":
                    send_player_move(games.check_player_game(client), client, data)


                #GMED = Game End
                elif data[:4] == 'GMED':
                    remove_game(client, games)

                data = ""

def run_server():
    global games
    host = '0.0.0.0'
    port = 8201
    index_msg = 0

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f'Server is listening on {host}:{port}')

    threads = []
    games = GameHandler()
    try:
        while True:
            client = server_socket.accept()
            print(f'New client connected: {client[1]}')

            t = threading.Thread(target=handle_client, args=(client, ""))
            t.start()
            threads.append(t)


    except KeyboardInterrupt:
        print('Closing server...')

    finally:
        print('Main thread: waiting to all threads to die')
        for t in threads:
            t.join()
        print("closing server!")
        server_socket.close()


if __name__ == '__main__':
    run_server()
