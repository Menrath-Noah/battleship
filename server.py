import socket
import sys
import threading

# HOST_IP = '192.168.1.111'
HOST_IP = None
PORT = 5155

VISITOR_IP = None

devices = []
device_objects = {}

host_ship_coords = []
visitor_ship_coords = []

coords_received = []

host_attacks = []
visitor_attacks = []
host_hits = []
visitor_hits = []

play_again = []

current_turn = ""

select_ship_positions = True
play_game = False
check_win_condition = True


# Create and bind the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def loop_game():
    global select_ship_positions, current_turn, play_game, device_objects, check_win_condition
    while True:
        if len(coords_received) == 2 and select_ship_positions:
            select_ship_positions = False
            # random_starter_turn = random.randint(0,1)
            random_starter_turn = 0
            if random_starter_turn == 0:
                current_turn = "HOST"
            elif random_starter_turn == 1:
                current_turn = "VISITOR"
            print(f"The {current_turn} has the first move!")
            for device in device_objects.values():
                device.send(f"SERVER: SHIP SELECTION FINISHED!!!+".encode("utf-8"))
                
                device.send(f"SERVER: The {current_turn} has the first move!+".encode("utf-8"))
                
                device.send(f"VAR:play_game:True+".encode("utf-8"))
            device_objects[current_turn].send(f"VAR:my_turn:True+".encode("utf-8"))
        if "VISITOR" in device_objects and "HOST" in device_objects and not play_game:
            print("BOTH CONNECTED!")
            device_objects["HOST"].send("FUNC:begin_game+".encode("utf-8"))
            device_objects["VISITOR"].send(f"FUNC:begin_game+".encode("utf-8"))
            play_game = True
        if check_win_condition:
            # if len(visitor_ship_coords) == len(host_hits) and len(visitor_ship_coords) > 1:
            if set(host_hits) == set(visitor_ship_coords) and host_hits:
                print("HOST Wins!")
                device_objects["HOST"].send("VAR:end_game:WIN+".encode("utf-8"))
                device_objects["VISITOR"].send("VAR:end_game:LOSE+".encode("utf-8"))
                check_win_condition = False
            # if len(host_ship_coords) == len(visitor_hits) and len(host_ship_coords) > 1:
            if set(visitor_hits) == set(host_ship_coords) and visitor_hits:
                print("VISITOR Wins!")
                device_objects["VISITOR"].send("VAR:end_game:WIN+".encode("utf-8"))
                device_objects["HOST"].send("VAR:end_game:LOSE+".encode("utf-8"))
                check_win_condition = False
        if len(play_again) >= 2:
            device_objects["HOST"].send("FUNC:restart_game+".encode("utf-8"))
            device_objects["VISITOR"].send("FUNC:restart_game+".encode("utf-8"))
            restart_game()
        # print(f"V: {len(visitor_ship_coords)}")
        # print(visitor_ship_coords)
        # print(f"H: {len(host_hits)}")




def loop_client(device, address):
    global visitor_ship_coords, host_ship_coords, current_turn
    print(f"***DEVICE CONNECTED FROM {address[0]}***")
    while True:
        new_data = device.recv(2048)
        new_data = new_data.decode()
        if len(new_data) > 0:
            # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # client.bind((address[0], address[1]))
            print(new_data)
            if new_data.startswith("SHIP-COORDS:"):
                if address[0] == HOST_IP:
                    # coords = new_data.split("SHIP-COORDS:", 2)[1]
                    # for coord in coords:
                    #     host_ship_coords.append(coord)
                    coords = new_data[12:]
                    host_ship_coords = eval(coords)
                    print(f"Host Ship Coords: {host_ship_coords}")
                    device.send(f"SERVER: Coordinates Received.+".encode("utf-8"))
                    coords_received.append(1)
                elif address[0] == VISITOR_IP:
                    # coords = new_data.split("SHIP-COORDS:", 2)[1]
                    coords = new_data[12:]
                    # for coord in coords:
                    #     visitor_ship_coords.append(coord)
                    visitor_ship_coords = eval(coords)
                    # visitor_ship_coords = new_data.split("SHIP-COORDS:", 2)[1]
                    print(f"Visitor Ship Coords: {visitor_ship_coords}")
                    device.send(f"SERVER: Coordinates Received.+".encode("utf-8"))
                    coords_received.append(1)
                
            if new_data.startswith("POSITION:"):
                if address[0] == HOST_IP:
                    new_data = new_data.split("POSITION:", 2)[1]
                    host_attacks.append(new_data)
                    if new_data in visitor_ship_coords:
                        device.send(f"ATTACK:RECEIVED:HIT:{new_data}+".encode("utf-8"))
                        host_hits.append(new_data)
                        print(f"H: {set(host_hits)}")
                        print(f"V: {set(visitor_ship_coords)}")
                    else:
                        device.send(f"ATTACK:RECEIVED:MISS:{new_data}+".encode("utf-8"))
                    other_player = ""
                    if current_turn == "HOST":
                        other_player = "VISITOR"
                    elif current_turn == "VISITOR":
                        other_player = "HOST"
                    if new_data in visitor_ship_coords:
                        device_objects[other_player].send(f"ATTACK:OPPONENT:HIT:{new_data}+".encode("utf-8"))
                    else:
                        device_objects[other_player].send(f"ATTACK:OPPONENT:MISS:{new_data}+".encode("utf-8"))
                    
                    current_turn = "VISITOR"
                    device.send(f"VAR:my_turn:False+".encode("utf-8"))
                    
                    device_objects[other_player].send(f"VAR:my_turn:True+".encode("utf-8"))

                elif address[0] == VISITOR_IP:
                    new_data = new_data.split("POSITION:", 2)[1]
                    visitor_attacks.append(new_data)
                    if new_data in host_ship_coords:
                        device.send(f"ATTACK:RECEIVED:HIT:{new_data}+".encode("utf-8"))
                        visitor_hits.append(new_data)
                    else:
                        device.send(f"ATTACK:RECEIVED:MISS:{new_data}+".encode("utf-8"))
                    
                    other_player = ""
                    if current_turn == "HOST":
                        other_player = "VISITOR"
                    elif current_turn == "VISITOR":
                        other_player = "HOST"
                    if new_data in host_ship_coords:
                        device_objects[other_player].send(f"ATTACK:OPPONENT:HIT:{new_data}+".encode("utf-8"))
                    else:
                        device_objects[other_player].send(f"ATTACK:OPPONENT:MISS:{new_data}+".encode("utf-8"))
                    current_turn = "HOST"
                    device.send(f"VAR:my_turn:False+".encode("utf-8"))
                    device_objects[other_player].send(f"VAR:my_turn:True+".encode("utf-8"))
            if new_data.startswith("VAR:"):
                if address[0] == HOST_IP:
                    new_data = new_data.split("VAR:", 2)[1]
                    if new_data == "play_again":
                        if "HOST" not in play_again:
                            play_again.append("HOST")
                elif address[0] == VISITOR_IP:
                    new_data = new_data.split("VAR:", 2)[1]
                    if new_data == "play_again":
                        if "VISITOR" not in play_again:
                            play_again.append("VISITOR")


def restart_game():
    global host_ship_coords, visitor_ship_coords, coords_received, host_attacks, visitor_attacks, host_hits, visitor_hits, play_again, current_turn, select_ship_positions, play_game, check_win_condition
    print("Game Restarted!")
    host_ship_coords = []
    visitor_ship_coords = []
    coords_received = []
    host_attacks = []
    visitor_attacks = []
    host_hits = []
    visitor_hits = []
    play_again = []
    current_turn = ""
    select_ship_positions = True
    play_game = False
    check_win_condition = True


if __name__ == "__main__":
    # HOST_IP = "192.168.1.111"
    HOST_IP = sys.argv[1]
    PORT = int(sys.argv[2])
    # server.bind((HOST_IP, PORT))
    server.bind(("0.0.0.0", 5155))
    server.listen(2)
    print(f"***SERVER LAUNCHED ON PORT {PORT}***")
    control_game = threading.Thread(target=loop_game)
    control_game.start()
    while True:
        connection_obj, address = server.accept()

        if address[0] not in devices:
            devices.append(address[0])
            if address[0] == HOST_IP:
                device_objects["HOST"] = connection_obj
            else:
                device_objects["VISITOR"] = connection_obj
            # device_objects.append(connection_obj)
            if address[0] != HOST_IP:
                VISITOR_IP = address[0]
        print(devices)
        new_device = threading.Thread(target=loop_client, args=(connection_obj, address))
        new_device.start()

