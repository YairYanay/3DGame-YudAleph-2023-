import socket
import threading
import protocol
import random

#data
POINT_END_TAME = 5

class Game:
    def __init__(self, game_capacity):
        self.game_start = False
        self.game_capacity = int(game_capacity)
        self.numPlayers = 0
        self.players_name = []
        self.police_players = []   #list with sock and addres
        self.robber_players = []   #list with sock and addres
        self.point_game = [0, 0]   #first police and second robber point
        self.players_deads = []

    def add_player(self, player, name_player):
        if len(self.police_players) < self.game_capacity//2:
            self.police_players.append(player)
            self.numPlayers += 1
            self.players_name.append(name_player)

        elif len(self.robber_players) < self.game_capacity//2:
            self.robber_players.append(player)
            self.numPlayers += 1
            self.players_name.append(name_player)

        if self.game_capacity == self.numPlayers:
            self.game_start = True

    def remove_player(self, player):
        if player in self.players_deads:
            self.players_deads.remove(player)

        if player in self.police_players:
            self.police_players.remove(player)
            self.numPlayers -= 1
            del self.players_name[self.check_number_player(player)]
            self.game_start = False

        elif player in self.robber_players:
            self.robber_players.remove(player)
            del self.players_name[self.check_number_player(player)]
            self.numPlayers -= 1
            del self.players_name[self.check_number_player(player)]
            self.game_start = False

    def is_empty(self):
        return self.numPlayers == 0

    def check_player_police(self, player):
        return player in self.police_players

    def add_point_team(self, team_won):
        if team_won == "police":
            self.point_game[0] += 1

        else:
            self.point_game[1] += 1

        if POINT_END_TAME in self.point_game:
            return True
        return False

    def reset_players_dead(self):
        self.players_deads = []

    def check_number_player(self, player):
        index = 0
        for i in self.police_players + self.robber_players:
            index += 1
            if player == i:
                return index
        return 0

    def return_player_name(self, index):
        return self.players_name[index]

class GameHandler:
    def __init__(self):
        self.games = []

    def add_player(self, player, game_capacity, name_player):
        for game in self.games:
            #add to see the dont play game (add to if not self.game_start)
            if game_capacity == game.game_capacity and game.numPlayers < game.game_capacity:
                game.add_player(player, name_player)
                return

        new_game = Game(game_capacity)
        new_game.add_player(player, name_player)
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
        posx = random.randint(15, 24)
        posy = 0
        posz = random.randint(15, 24)
        if not game.check_player_police(player):
            posx = -posx
            posz = -posz

        return posx, posy, posz

    def check_length(self):
        return len(self.games)

    def check_number_player(self, player):
        game = self.check_player_game(player)
        index = 0
        for i in game.police_players + game.robber_players:
            index += 1
            if player == i:
                return index
        return 0

    def player_dead(self, player):
        game = self.check_player_game(player)
        game.players_deads.append(player)
        if len(game.players_deads) <= game.game_capacity - 1:
            for client in game.police_players:
                if client not in game.players_deads:
                    return "police"
            return "robber"
        return ""

    def team_win(self, player):
        game = self.check_player_game(player)
        for client in game.police_players:
            if client not in game.players_deads:
                return "police"
        return "robber"


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
    for players in game.police_players + game.robber_players:
        print(f'Client {players[0]} disconnected')
        protocol.send_with_size(players[0], 'EXIT')
        players.close()
        # handle_client(player, 'EXIT')
    games.remove_game(game)
    print('remove game!')

def send_other_players_data(game, client, data):
    for player in game.police_players + game.robber_players:
        if player != client:
            protocol.send_with_size(player[0],data)

def return_names_enemy(player, name_player):
    game = games.check_player_game(player)
    if game.check_player_police(player):
        string = f",police"
        for name in game.players_name:
            if name_player != str(name):
                string += ','
                string += str(name)
        return string

    else:
        string = f",robber"
        for name in game.players_name[::-1]:
            if name_player != str(name):
                string += ','
                string += str(name)
        return string

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
                    client[0].close()
                    games.remove_player(client)
                    continue

                # if not data:
                #     client[0].close()

            if data:
                #RCGC = recv game capacity
                if data[:4] == "SDGC":
                    name_player = data.split(',')[2]
                    game_capacity = data.split(',')[1]
                    games.add_player(client, int(game_capacity), name_player)
                    check_start_game = games.check_start_game(client)
                    while not check_start_game:
                        check_start_game = games.check_start_game(client)
                    posx, posy, posz = games.get_first_pos(client)
                    protocol.send_with_size(client[0], f'STGM,{posx},{posy},{posz}')
                    protocol.send_with_size(client[0], f'NMPL{return_names_enemy(client, name_player)}')

                elif data[:4] == 'EXIT':
                    print(f'Client {client[1]} disconnected')
                    client[0].close()
                    games.remove_player(client)

                #ENMP = Enemy position
                elif data[:4] == "ENMP":
                    send_other_players_data(games.check_player_game(client), client, data)

                #BLTP = bullet position
                elif data[:4] == 'BLTP':
                    send_other_players_data(games.check_player_game(client), client, data)

                #GMED = Game End
                # elif data[:4] == 'GMED':
                #     remove_game(client, games)

                # elif data[:4] == 'HTPL':
                #     pass


                # elif data[:4] == 'PLYD':
                #     send_other_players_data(games.check_player_game(client), client, f"PLYD")

                elif data[:4] == 'IMDD':
                    team_win = games.player_dead(client)
                    if team_win:
                        print(team_win + " win!")
                        game = games.check_player_game(client)
                        check_end_game = game.add_point_team(team_win)
                        if check_end_game:
                            for players in game.police_players + game.robber_players:
                                protocol.send_with_size(players[0], f"TMWN,{team_win},{game.point_game[0]},{game.point_game[1]}")
                                print(game.point_game)
                                game.remove_player(players)
                                protocol.send_with_size(players[0], 'EXIT')
                                players[0].close()

                            games.remove_game(game)
                            exit()
                        else:
                            i = 0
                            for player in game.police_players + game.robber_players:
                                protocol.send_with_size(player[0], f"TMWN,{team_win},{game.point_game[0]},{game.point_game[1]}")
                                posx, posy, posz = games.get_first_pos(player)
                                protocol.send_with_size(player[0], f'ENMP,{game.return_player_name(i)},{posx},{posy},{posz}')
                                i += 1
                        game.reset_players_dead()

                data = ""

def run_server():
    global games
    host = '0.0.0.0'
    port = 8220

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
