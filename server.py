import random
import socket
import threading

HOST_IP = '192.168.1.111'
PORT = 5159

VISITOR_IP = ''

devices = []
device_objects = []

host_ship_coords = []
visitor_ship_coords = []

coords_received = []

current_turn = ""

select_ship_positions = True
play_game = True


# Create and bind the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST_IP, PORT))
server.listen(2)
print(f"***SERVER LAUNCHED***")




def loop_game():
    global select_ship_positions
    global current_turn
    while True:
        if len(coords_received) == 2 and select_ship_positions:
            select_ship_positions = False
            random_starter_turn = random.randint(0,1)
            if random_starter_turn == 0:
                current_turn = "HOST"
            elif random_starter_turn == 1:
                current_turn = "VISITOR"
            print(f"The {current_turn} has the first move!")
            for device in device_objects:
                device.sendall(f"SERVER: SHIP SELECTION FINISHED!!!\n".encode("utf-8"))
                device.sendall(f"SERVER: The {current_turn} has the first move!\n".encode("utf-8"))




def loop_client(device, address):
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
                    host_ship_coords = new_data.split("SHIP-COORDS:", 2)[1]
                    print(f"Host Ship Coords: {host_ship_coords}")
                    device.sendall(f"SERVER: Coordinates Received.".encode("utf-8"))
                    coords_received.append(1)
                elif address[0] == VISITOR_IP:
                    visitor_ship_coords = new_data.split("SHIP-COORDS:", 2)[1]
                    print(f"Visitor Ship Coords: {visitor_ship_coords}")
                    device.sendall(f"SERVER: Coordinates Received.".encode("utf-8"))
                    coords_received.append(1)

control_game = threading.Thread(target=loop_game)
control_game.start()


while True:
    connection_obj, address = server.accept()

    if address[0] not in devices:
        devices.append(address[0])
        device_objects.append(connection_obj)
        if address[0] != HOST_IP:
            VISITOR_IP = address[0]
    print(devices)
    new_device = threading.Thread(target=loop_client, args=(connection_obj, address))

    new_device.start()

