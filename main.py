import time

import pygame, sys, socket, subprocess, pygame_textinput as pg_input

pygame.init()

screen = pygame.display.set_mode((1100,650))


pygame.display.set_caption("Battleship")


mainMenuBackground= pygame.image.load("./img/mainMenuBackground.png").convert_alpha()
outerBackground = pygame.image.load("./img/outerBackgroundResized.png").convert_alpha()

borderBarHorizontal = pygame.image.load("./img/borderBarTop.png").convert_alpha()
borderBarVertical = pygame.image.load("./img/borderBarSide.png").convert_alpha()

grid_background = pygame.image.load("./img/gridBackground.png").convert_alpha()

coords_used = []

# SERVER_IP = '192.168.1.111'
SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5155
client = None



def connect_to_server(connecting_address, connecting_port=5155):
    global client
    print("CONN-1")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("CONN-2")
    try:
        print("CONN-3")

        client.connect((connecting_address, connecting_port))
        print("CONN-4")
        client.setblocking(False)
        print("***WELCOME TO THE SERVER!!!***")
    except Exception as error:
        print("***CANNOT CONNECT***", error)
        sys.exit()




class GridButtonHome: # individual grid squares for Placing Boats
    def __init__(self,x=100,y=100, letter=65, num=1):
        self.x_pos = x
        self.y_pos = y
        self.width = 35
        self.height = 35
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.letter = letter
        self.num = num
        self.coord = f"{chr(self.letter)}{self.num}"

    def clicked(self):
        print(f"I HAVE BEEN CLICKED AT: {self.coord}")

class GridButtonAway: # individual grid squares for Attacking
    def __init__(self,x=100,y=100, letter=65, num=1):
        self.x_pos = x
        self.y_pos = y
        self.width = 35
        self.height = 35
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.letter = letter
        self.num = num
        self.coord = f"{chr(self.letter)}{self.num}"

    def clicked(self):
        global selected_target
        print(f"I HAVE BEEN CLICKED AT: {self.coord}")
        if my_turn and self.coord not in my_attacks:
            selected_target = self.coord
            print(selected_target)




class Boat:
    def __init__(self, x=500, y=500):
        self.x_pos = x
        self.y_pos = y
        self.img = pygame.image.load("./img/2SquareBoat.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.default_x = 500
        self.default_y = 500
        self.last_x = 500
        self.last_y = 500
        self.rotation = 0
        self.blocks = 2
        self.current_squares = []

    def calc_grid_squares(self):
        first_square_x = self.rect.x
        first_square_y = self.rect.y
        first_square = None
        first_square_num = None
        first_square_letter = None
        selected_squares = []
        current_square_count = 0
        if self.rotation == 0:
            for key, block in gridHome.items():
                if block.rect.x == first_square_x and block.rect.y == first_square_y:
                    first_square = key
                    first_square_num = block.num
                    first_square_letter = block.letter
            if first_square:
                while current_square_count != self.blocks:
                    selected_squares.append(f"{chr(first_square_letter)}{first_square_num}")
                    first_square_num += 1
                    current_square_count += 1
                print(selected_squares)
                if len(selected_squares) == self.blocks and first_square_num <= 11:
                    for square in selected_squares:
                        if square in coords_used:
                            return False
                    for square in selected_squares:
                        self.current_squares.append(square)
                        coords_used.append(square)
                    return True
                else:
                    return False
        if self.rotation == -90:
            for key, block in gridHome.items():
                if block.rect.x == first_square_x and block.rect.y == first_square_y:
                    first_square = key
                    first_square_num = block.num
                    first_square_letter = block.letter
            if first_square:
                while current_square_count != self.blocks:
                    selected_squares.append(f"{chr(first_square_letter)}{first_square_num}")
                    first_square_letter += 1
                    current_square_count += 1
                print(selected_squares)
                if len(selected_squares) == self.blocks and first_square_letter <= 75:
                    for square in selected_squares:
                        if square in coords_used:
                            return False
                    for square in selected_squares:
                        self.current_squares.append(square)
                        coords_used.append(square)
                    return True
                else:
                    return False


    def update_coords(self):
        if self.current_squares:
            for square in self.current_squares:
                if square in coords_used:
                    coords_used.remove(square)
            self.current_squares = []



class TwoSquareBoat(Boat): # class for two square-long boat
    def __init__(self, x=395, y=485):
        super().__init__(x, y)
        self.x_pos = x
        self.y_pos = y
        self.img = pygame.image.load("./img/ship2.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.default_x = 395
        self.default_y = 485
        self.last_x = 395
        self.last_y = 485
        self.blocks = 2


class FiveSquareBoat(Boat): # class for five square-long boat
    def __init__(self, x=65, y=485):
        super().__init__(x, y)
        self.x_pos = x
        self.y_pos = y
        self.img = pygame.image.load("./img/ship5Fixed2.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.default_x = 65
        self.default_y = 485
        self.last_x = 65
        self.last_y = 485
        self.blocks = 5


class FourSquareBoat(Boat): # class for five square-long boat
    def __init__(self, x=300, y=535):
        super().__init__(x, y)
        self.x_pos = x
        self.y_pos = y
        self.img = pygame.image.load("./img/4ship.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.default_x = 300
        self.default_y = 535
        self.last_x = 300
        self.last_y = 535
        self.blocks = 4


class FourSquareSecondBoat(Boat): # class for five square-long boat
    def __init__(self, x=100, y=535):
        super().__init__(x, y)
        self.x_pos = x
        self.y_pos = y
        self.img = pygame.image.load("./img/4shipSecond.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.default_x = 100
        self.default_y = 535
        self.last_x = 100
        self.last_y = 535
        self.blocks = 4


class ThreeSquareBoat(Boat): # class for five square-long boat
    def __init__(self, x=265, y=485):
        super().__init__(x, y)
        self.x_pos = x
        self.y_pos = y
        self.img = pygame.image.load("./img/3ship.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.default_x = 265
        self.default_y = 485
        self.last_x = 265
        self.last_y = 485
        self.blocks = 3




menu_font = pygame.font.SysFont("Roger Bold Serif", 48)
text_font = pygame.font.SysFont("Roger Bold Serif", 28)
text_font2 = pygame.font.SysFont("Bondi", 28)
text_font3= pygame.font.SysFont("Bondi", 42)
server_message_font = pygame.font.SysFont("Times New Romand", 32)
server_message_font2 = pygame.font.SysFont("Arial", 22)
game_result_font = pygame.font.SysFont("Roger Bold Serif", 56)

textBoardHome = {}
textBoardAway = {}


#grid = []
gridHome = {}
gridAway = {}

my_attacks = []
my_missed_attacks = []
my_hit_attacks = []

opponent_attacks = []
opponent_missed_attacks = []
opponent_hit_attacks = []


my_turn = False
selected_target = ""

create_game = True
select_ship_positions = True
play_game = False
main_menu = True
end_screen = False
# end_screen = True
# create_game = False
# select_ship_positions = False
# play_game = False
# main_menu = False


ships = []


currently_selected = None
canceled_action = False
attack_button = None

hovering_grid = False

show_server_message = False
server_menu_messageA = ""
server_menu_messageB = ""

server_result_message = ""

ip_input = pg_input.TextInputVisualizer()
port_input = pg_input.TextInputVisualizer()
joining = False
input_border = None
port_input_border = None
ip_input_typing = False
port_input_typing = False
connecting_address = ""
confirm_connection_button = None
game_result = False
play_again = False




def begin_game():
    print("GAME BEGINNING!!!")
    global joining, input_border, ip_input_typing, show_server_message, server_menu_messageA, server_menu_messageB, play_game, main_menu, select_ship_positions
    global end_screen, game_result, server_result_message, play_again, gridHome, gridAway, my_attacks, my_missed_attacks, my_hit_attacks, opponent_attacks, opponent_hit_attacks, opponent_missed_attacks
    global textBoardHome, textBoardAway, create_game, confirm_connection_button, ships, coords_used
    joining = False
    input_border = None
    ip_input_typing = False
    show_server_message = False
    server_menu_messageA = ""
    server_menu_messageB = ""
    server_result_message = ""
    play_game = False
    main_menu = False
    select_ship_positions = True
    create_game = True
    end_screen = False
    game_result = False
    play_again = False
    gridHome = {}
    gridAway = {}
    my_attacks = []
    my_missed_attacks = []
    my_hit_attacks = []
    opponent_attacks = []
    opponent_missed_attacks = []
    opponent_hit_attacks = []
    textBoardHome = {}
    textBoardAway = {}
    confirm_connection_button = None
    ships = []
    coords_used = []
    ships.append(TwoSquareBoat())
    ships.append(FiveSquareBoat())
    ships.append(FourSquareBoat())
    ships.append(FourSquareSecondBoat())
    ships.append(ThreeSquareBoat())

game = True
while game:
    clock = 60

    if main_menu:
        screen.blit(mainMenuBackground, (0,0))
        host_button_border = pygame.Rect(442, 255, 215, 70)
        host_button_inner = pygame.Rect(452, 265, 195, 50)
        join_button_border = pygame.Rect(442, 345, 215, 70)
        join_button_inner = pygame.Rect(452, 355, 195, 50)
        pygame.draw.rect(screen, (0,0,0), host_button_border)
        pygame.draw.rect(screen, (0,0,0), join_button_border)
        pygame.draw.rect(screen, (255,255,255), host_button_inner)
        pygame.draw.rect(screen, (255,255,255), join_button_inner)

        text_renderer_host = menu_font.render("HOST", False, (0,0,0))
        text_renderer_join = menu_font.render("JOIN", False, (0,0,0))
        screen.blit(text_renderer_host, (host_button_inner.x+50,host_button_inner.y+10))
        screen.blit(text_renderer_join, (join_button_inner.x+50,join_button_inner.y+10))




        if show_server_message:
            server_menu_message_border = pygame.Rect(host_button_inner.x+237, 255, 386, 70)
            server_menu_message_inner = pygame.Rect(host_button_inner.x+245, 265, 370, 50)

            pygame.draw.rect(screen, (0,175,0), server_menu_message_border)
            pygame.draw.rect(screen, (255,255,255), server_menu_message_inner)



            text_renderer_server_messageA = server_message_font.render(f"{server_menu_messageA}", False, (0,0,0))
            text_renderer_server_messageB = server_message_font.render(f"{server_menu_messageB}", False, (0,0,0))
            screen.blit(text_renderer_server_messageA, (host_button_inner.x+260,host_button_inner.y+5))
            screen.blit(text_renderer_server_messageB, (host_button_inner.x+260,host_button_inner.y+25))
        if joining:
            input_border = pygame.Rect(join_button_inner.x+237, 390, 386, 70)
            input_inner = pygame.Rect(join_button_inner.x+245, 400, 370, 50)


            pygame.draw.rect(screen, (0,175,0), input_border)
            pygame.draw.rect(screen, (255,255,255), input_inner)




            screen.blit(ip_input.surface, (input_inner.x+15,input_inner.y+12))


            port_input_border = pygame.Rect(join_button_inner.x+237, 520, 150, 70)
            port_input_inner = pygame.Rect(join_button_inner.x+245, 530, 134, 50)

            pygame.draw.rect(screen, (0,175,0), port_input_border)
            pygame.draw.rect(screen, (255,255,255), port_input_inner)
            screen.blit(port_input.surface, (port_input_inner.x+15,port_input_inner.y+12))

            text_renderer_join_address = text_font2.render("IP ADDRESS:", False, (0,0,0))
            screen.blit(text_renderer_join_address, (input_border.x+100, input_border.y-23))
            text_renderer_join_port = text_font2.render("PORT:", False, (0,0,0))
            screen.blit(text_renderer_join_port, (port_input_border.x+50, port_input_border.y-23))

            text_renderer_connect = text_font3.render("CONNECT", False, (0,0,0))
            confirm_connection_button = pygame.Rect(port_input_border.x+200, port_input_border.y, 175, 70)
            confirm_connection_button_inner = pygame.Rect(port_input_border.x+210, port_input_border.y+10, 155, 50)
            pygame.draw.rect(screen, (0,0,0), confirm_connection_button)
            pygame.draw.rect(screen, (255,255,255), confirm_connection_button_inner)
            screen.blit(text_renderer_connect, (confirm_connection_button_inner.x+9, confirm_connection_button_inner.y+13))




        for event in pygame.event.get(): # handles most user input events
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if host_button_border.collidepoint(event.pos):
                    try:
                        my_ip = "192.168.1.111"
                        try:
                            subprocess.run(["start", "powershell", "-Command", f"python server.py"], shell=True)
                        except Exception as error:
                            print(error)
                        time.sleep(1)
                        server_menu_messageA = f"Server Started at {my_ip}"
                        server_menu_messageB = "Waiting for opponent..."
                        try:
                            connect_to_server(my_ip)
                        except Exception as error:
                            print(error)

                    except Exception as error:
                        server_message = f"{error}"
                    show_server_message = True
                if join_button_border.collidepoint(event.pos):
                    joining = True
                if input_border:
                    print("leleellee")
                    if input_border.collidepoint(event.pos):
                        ip_input_typing = True
                    else:
                        ip_input_typing = False
                if port_input_border:
                    if port_input_border.collidepoint(event.pos):
                        port_input_typing = True
                    else:
                        port_input_typing = False
                if joining:
                    if confirm_connection_button:
                        print("YEYEYE")
                        if confirm_connection_button.collidepoint(event.pos):
                            connecting_address = ip_input.value
                            connecting_port = 5155
                            if port_input.value:
                                connecting_port = int(port_input.value)
                            print("YEYEYEYE2")
                            print(connecting_port)
                            try:
                                connect_to_server(connecting_address, connecting_port)
                                print("GOOD")
                            except:
                                pass
            if ip_input_typing:
                if event.type == pygame.KEYDOWN:
                    ip_input.update([event])
            if port_input_typing:
                if event.type == pygame.KEYDOWN:
                    port_input.update([event])

        try:
            new_data = client.recv(2048)
            new_data = new_data.decode()
            new_data = new_data.strip()
            print("----")
            print(new_data)
            print("----")
            if new_data.count("+") > 1:
                new_data = new_data.split("+")
                for data in new_data:
                    if data.startswith("FUNC:"):
                        print("HEHE-1")
                        updated_data = data[5:]
                        updated_data = updated_data.replace("+", "")
                        updated_data = updated_data.strip()
                        if updated_data == "begin_game":
                            print("HEHE-2")
                            begin_game()
                    else:
                        data = data.replace("+", "")
                        data.strip()
                        print(data)
            else:
                if new_data.startswith("FUNC:"):
                    print("HEHE-A")
                    updated_data = new_data[5:]
                    updated_data = updated_data.replace("+", "")
                    updated_data = updated_data.strip()
                    if updated_data == "begin_game":
                        print("HEHE-B")
                        begin_game()
                else:
                    new_data = new_data.replace("+", "")
                    new_data.strip()
                    print(new_data)
        except:
            pass


        pygame.display.flip()
        pygame.display.update()

    elif not main_menu and not end_screen:
        screen.blit(outerBackground, (0, 0))
        # screen.blit(mainMenuBackground, (0, 0))

        # if "A1" in gridHome:
        #     screen.blit(grid_background, (gridHome["A1"].rect.x, gridHome["A1"].rect.y))
        # if "A1" in gridAway:
        #     screen.blit(grid_background, (gridAway["A1"].rect.x, gridAway["A1"].rect.y))

        screen.blit(borderBarHorizontal, (92, 92))
        screen.blit(borderBarHorizontal, (92, 459))
        screen.blit(borderBarVertical, (92, 92))
        screen.blit(borderBarVertical, (459, 92))

        screen.blit(borderBarHorizontal, (567, 92))
        screen.blit(borderBarHorizontal, (567, 459))
        screen.blit(borderBarVertical, (567, 92))
        screen.blit(borderBarVertical, (934, 92))

        if select_ship_positions:
            shipyard_background = pygame.Rect(50, 475, 435, 170)
            pygame.draw.rect(screen, (144, 173, 200), shipyard_background)



        if create_game: # creates the game board
            x_pos = 100-36
            y_pos = 100
            letter = 65
            num = 0

            text_rendererA = text_font.render("A", False, (0,0,0))
            text_rendererB = text_font.render("B", False, (0,0,0))
            text_rendererC = text_font.render("C", False, (0,0,0))
            text_rendererD = text_font.render("D", False, (0,0,0))
            text_rendererE = text_font.render("E", False, (0,0,0))
            text_rendererF = text_font.render("F", False, (0,0,0))
            text_rendererG = text_font.render("G", False, (0,0,0))
            text_rendererH = text_font.render("H", False, (0,0,0))
            text_rendererI = text_font.render("I", False, (0,0,0))
            text_rendererJ = text_font.render("J", False, (0,0,0))

            text_renderer1 = text_font.render("1", False, (0,0,0))
            text_renderer2 = text_font.render("2", False, (0,0,0))
            text_renderer3 = text_font.render("3", False, (0,0,0))
            text_renderer4 = text_font.render("4", False, (0,0,0))
            text_renderer5 = text_font.render("5", False, (0,0,0))
            text_renderer6 = text_font.render("6", False, (0,0,0))
            text_renderer7 = text_font.render("7", False, (0,0,0))
            text_renderer8 = text_font.render("8", False, (0,0,0))
            text_renderer9 = text_font.render("9", False, (0,0,0))
            text_renderer10 = text_font.render("10", False, (0,0,0))

            textBoardHome[f"{chr(letter)}"] = (x_pos+8, y_pos+9)
            textBoardHome[num] = (x_pos+12, y_pos-30)


            for i in range(100):
                if i % 10 == 0 and i != 0:
                    x_pos = 100
                    y_pos += 36
                    num = 1
                    letter += 1
                    textBoardHome[f"{chr(letter)}"] = (x_pos-28, y_pos+9)
                else:
                    x_pos += 36
                    num += 1
                    if chr(letter) == "A":
                        if num == 10:
                            textBoardHome[num] = (x_pos+5, y_pos-30)
                        else:
                            textBoardHome[num] = (x_pos+12, y_pos-30)
                gridHome[f"{chr(letter)}{num}"] = GridButtonHome(x_pos, y_pos, letter, num)
            x_pos = 575-36
            y_pos = 100
            letter = 65
            num = 0
            textBoardAway[f"{chr(letter)}"] = (x_pos+8, y_pos+9)
            textBoardAway[num] = (x_pos+12, y_pos-30)
            for i in range(100):
                if i % 10 == 0 and i != 0:
                    x_pos = 575
                    y_pos += 36
                    num = 1
                    letter += 1
                    textBoardAway[f"{chr(letter)}"] = (x_pos-28, y_pos+9)
                else:
                    x_pos += 36
                    num += 1
                    if chr(letter) == "A":
                        if num == 10:
                            textBoardAway[num] = (x_pos+5, y_pos-30)
                        else:
                            textBoardAway[num] = (x_pos+12, y_pos-30)
                gridAway[f"{chr(letter)}{num}"] = GridButtonAway(x_pos, y_pos, letter, num)

            create_game = False

        for button in gridHome.values(): # draws each individual square in the grid
            pygame.draw.rect(screen, (0, 157, 196), button.rect)
        for button in gridAway.values(): # draws each individual square in the grid
            pygame.draw.rect(screen, (0, 157, 196), button.rect)



        if select_ship_positions:
            confirm_button = pygame.Rect(220, 585, 125, 45)
            confirm_button_border = pygame.Rect(confirm_button.x-5, confirm_button.y-5, 135, 55)
            pygame.draw.rect(screen, (255,255,255), confirm_button_border)
            pygame.draw.rect(screen, (144,238,144), confirm_button)
            text_renderer_confirm_button = text_font2.render("Confirm", False, (0,0,0))
            screen.blit(text_renderer_confirm_button, (confirm_button.x+23, confirm_button.y+11))



        if play_game:
            attack_button = pygame.Rect(720, 500, 100, 35)
            attack_button_border = pygame.Rect(attack_button.x-5, attack_button.y-5, 110, 45)
            text_renderer_attack_button = text_font2.render("Attack", False, (0,0,0))
            if my_turn:
                pygame.draw.rect(screen, (0,0,0), attack_button_border)
                pygame.draw.rect(screen, (255,0,0), attack_button)
                screen.blit(text_renderer_attack_button, (attack_button.x+21, attack_button.y+9))

            else:
                pygame.draw.rect(screen, (128,128,128), attack_button)

        ship_dragged = False
        for event in pygame.event.get(): # handles most user input events
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if currently_selected:
                    if currently_selected.calc_grid_squares(): # only places down the ship on grid if in proper spot
                        currently_selected = None
                        canceled_action = True
                        print(coords_used)
                    elif not hovering_grid: # returns ship to default location if placed not on grid square
                        currently_selected.rect.x = currently_selected.default_x
                        currently_selected.rect.y = currently_selected.default_y
                        currently_selected = None
                        canceled_action = True
                for button in gridHome.values(): # prints out the square that was clicked
                    if button.rect.collidepoint(event.pos):
                        button.clicked()
                for key, button in gridAway.items(): # handles attacking a point
                    extended_square = pygame.Rect(button.rect.x, button.rect.y, button.rect.width + 1, button.rect.height + 1)
                    if extended_square.collidepoint(event.pos):
                        button.clicked()
                        print("HEHEHE")
                        # print(attack_button)
                        # print(my_turn)
                        # if attack_button:
                        #     print(event.pos)
                        #     if attack_button.collidepoint(event.pos) and my_turn:
                        #         if (selected_target not in my_attacks) and selected_target:
                        #             print(selected_target)
                        #             print("INNNN")
                        #             client.send(f"POSITION:{selected_target}".encode("utf-8"))
                        #             selected_target = ""
                        # if key in coords_used:
                        #     my_hit_attacks.append(key)
                        # else:
                        #     my_missed_attacks.append(key)
                if not canceled_action and not currently_selected: # handles selecting a ship to move/place
                    for ship in ships:
                        if ship.rect.collidepoint(event.pos) and select_ship_positions:
                            currently_selected = ship
                            currently_selected.update_coords()
                canceled_action = False
                if confirm_button:
                    if confirm_button.collidepoint(event.pos):
                        if len(ships) > 0:
                            not_ready = False
                            for boat in ships:
                                if boat.rect.x == boat.default_x and boat.rect.y == boat.default_y:
                                    not_ready = True
                            if not not_ready:
                                client.send(f"SHIP-COORDS:{coords_used}".encode("utf-8"))
                                print("Ship Coords Locked-In!")
                                currently_selected = None
                                confirm_button = None
                                select_ship_positions = False
                if attack_button:
                    if attack_button.collidepoint(event.pos) and my_turn and selected_target:
                        print("LEELELELELE")
                        client.send(f"POSITION:{selected_target}".encode("utf-8"))
                        selected_target = ""

            if currently_selected and event.type == pygame.KEYDOWN: # changes rotation angle if 'r' key is pressed when holding ship.
                if event.key == pygame.K_r:
                    if currently_selected.rotation:
                        currently_selected.rotation += 90
                    else:
                        currently_selected.rotation -= 90
                    canceled_action = True



        for ship in ships: # displays the ships to the screen and handles the rotation of the rects
            ship_rotation = pygame.transform.rotate(ship.img,ship.rotation)
            screen.blit(ship_rotation, (ship.rect.x,ship.rect.y))

            rotation_rect = ship_rotation.get_rect(center=ship.rect.center)
            ship.rect = rotation_rect
            #pygame.draw.rect(screen, (255,0,0), ship.rect)



        if currently_selected: # if a ship is selected, handle how it moves
            mouse_pos = pygame.mouse.get_pos()
            hovering_grid = False
            for square in gridHome.values():
                extended_square = pygame.Rect(square.rect.x, square.rect.y, square.rect.width + 1, square.rect.height + 1)
                if extended_square.collidepoint(mouse_pos): # ship snaps to hovered over square
                    hovering_grid = True
                    # print("GRID")
                    currently_selected.rect.x = square.rect.x
                    currently_selected.rect.y = square.rect.y
                    #currently_selected.calc_grid_squares()
                    break
            if not hovering_grid: # if ship is not over a grid square, follow the mouse
                currently_selected.rect.x = mouse_pos[0]
                currently_selected.rect.y = mouse_pos[1]
                # print("NO GRID")


        for button in my_missed_attacks:
            pygame.draw.circle(screen, (0,0,0), gridAway[button].rect.center, 10)
            # gridButtonAway[area]
        for button in my_hit_attacks:
            pygame.draw.line(screen, (255,0,0), (gridAway[button].rect.x + 5, gridAway[button].rect.y + 5), (gridAway[button].rect.x+30, gridAway[button].rect.y+30), 4)
            pygame.draw.line(screen, (255,0,0), (gridAway[button].rect.x + 5, gridAway[button].rect.y + 30), (gridAway[button].rect.x+30, gridAway[button].rect.y+5), 4)

        for button in opponent_missed_attacks:
            pygame.draw.circle(screen, (0,0,0), gridHome[button].rect.center, 10)
            # gridButtonAway[area]
        for button in opponent_hit_attacks:
            pygame.draw.line(screen, (255,0,0), (gridHome[button].rect.x + 5, gridAway[button].rect.y + 5), (gridHome[button].rect.x+30, gridAway[button].rect.y+30), 4)
            pygame.draw.line(screen, (255,0,0), (gridHome[button].rect.x + 5, gridAway[button].rect.y + 30), (gridHome[button].rect.x+30, gridAway[button].rect.y+5), 4)


        def drawBoardText(key, text): # displays board coordinates
            if key == "A":
                screen.blit(text_rendererA, (text[0],text[1]))
            elif key == "B":
                screen.blit(text_rendererB, (text[0],text[1]))
            elif key == "C":
                screen.blit(text_rendererC, (text[0],text[1]))
            elif key == "D":
                screen.blit(text_rendererD, (text[0],text[1]))
            elif key == "E":
                screen.blit(text_rendererE, (text[0],text[1]))
            elif key == "F":
                screen.blit(text_rendererF, (text[0],text[1]))
            elif key == "G":
                screen.blit(text_rendererG, (text[0],text[1]))
            elif key == "H":
                screen.blit(text_rendererH, (text[0],text[1]))
            elif key == "I":
                screen.blit(text_rendererI, (text[0],text[1]))
            elif key == "J":
                screen.blit(text_rendererJ, (text[0],text[1]))
            elif key == 1:
                screen.blit(text_renderer1, (text[0],text[1]))
            elif key == 2:
                screen.blit(text_renderer2, (text[0],text[1]))
            elif key == 3:
                screen.blit(text_renderer3, (text[0],text[1]))
            elif key == 4:
                screen.blit(text_renderer4, (text[0],text[1]))
            elif key == 5:
                screen.blit(text_renderer5, (text[0],text[1]))
            elif key == 6:
                screen.blit(text_renderer6, (text[0],text[1]))
            elif key == 7:
                screen.blit(text_renderer7, (text[0],text[1]))
            elif key == 8:
                screen.blit(text_renderer8, (text[0],text[1]))
            elif key == 9:
                screen.blit(text_renderer9, (text[0],text[1]))
            elif key == 10:
                screen.blit(text_renderer10, (text[0],text[1]))


        for key,text in textBoardHome.items():
            drawBoardText(key, text)

        for key,text in textBoardAway.items():
            drawBoardText(key, text)


        if selected_target:
            pygame.draw.rect(screen, (255,255,255), (gridAway[selected_target].rect.x, gridAway[selected_target].rect.y, 35, 35), 4)


        try:
            new_data = client.recv(2048)
            new_data = new_data.decode()
            new_data = new_data.strip()
            print("----")
            print(new_data)
            print("----")
            if new_data.count("+") > 1:
                new_data = new_data.split("+")
                for data in new_data:
                    if data.startswith("VAR:"):
                        print("A")
                        updated_data = data[4:]
                        var_change = updated_data.split(":")
                        var = var_change[0]
                        var_value = var_change[1]
                        var_value = var_value.replace("+", "")
                        var_value.strip()
                        if var == "play_game":
                            print("B")
                            if var_value == "True":
                                play_game = True
                                print("C")
                            elif var_value == "False":
                                play_game = False
                        if var == "my_turn":
                            print("D")
                            if var_value == "True":
                                print("E")
                                my_turn = True
                            elif var_value == "False":
                                my_turn = False
                                print("F")
                        if var == "end_game":
                            if var_value == "WIN":
                                server_result_message = "YOU WIN!!!"
                                end_screen = True
                                game_result = True
                            elif var_value == "LOSE":
                                server_result_message = "YOU LOSE!!!"
                                end_screen = True
                                game_result = False
                    if data.startswith("ATTACK:"):
                        print("EINS")
                        updated_data = data[7:]
                        var_change = updated_data.split(":")
                        var = var_change[0]
                        var_value = var_change[1]
                        if var == "RECEIVED":
                            print("ZWEI")
                            updated_data = updated_data[9:]
                            var_change = updated_data.split(":")
                            var = var_change[0]
                            var_value = var_change[1]
                            var_value = var_value.replace("+", "")
                            var_value.strip()
                            my_attacks.append(var_value)
                            if var == "HIT":
                                print("DREI")
                                my_hit_attacks.append(var_value)
                            elif var == "MISS":
                                print("VIER")
                                my_missed_attacks.append(var_value)
                        elif var == "OPPONENT":
                            print("FUNF")
                            updated_data = updated_data[9:]
                            var_change = updated_data.split(":")
                            var = var_change[0]
                            var_value = var_change[1]
                            var_value = var_value.replace("+", "")
                            var_value.strip()
                            opponent_attacks.append(var_value)
                            if var == "HIT":
                                print("SECHS")
                                opponent_hit_attacks.append(var_value)
                            elif var == "MISS":
                                print("SIEBEN")
                                opponent_missed_attacks.append(var_value)
                    if data.startswith("FUNC:"):
                        print("HEHE-1")
                        updated_data = data[5:]
                        updated_data = updated_data.replace("+", "")
                        updated_data = updated_data.strip()
                        if updated_data == "begin_game":
                            print("HEHE-2")
                            begin_game()
                        if updated_data == "restart_game":
                            begin_game()
                    else:
                        print(data)
            else:
                if new_data.startswith("VAR:"):
                    print("0")
                    new_data = new_data[4:]
                    var_change = new_data.split(":")
                    var = var_change[0]
                    var_value = var_change[1]
                    var_value = var_value.replace("+", "")
                    var_value.strip()
                    if var == "play_game":
                        print("1")
                        if var_value == "True":
                            play_game = True
                            print("2")
                        elif var_value == "False":
                            play_game = False
                    if var == "my_turn":
                        print("3")
                        print(var)
                        print(var_value)
                        if var_value == "True":
                            print("4")
                            my_turn = True
                        elif var_value == "False":
                            my_turn = False
                            print("5")
                    if var == "end_game":
                        if var_value == "WIN":
                            server_result_message = "YOU WIN!!!"
                            end_screen = True
                            game_result = True
                        elif var_value == "LOSE":
                            server_result_message = "YOU LOSE!!!"
                            end_screen = True
                            game_result = False
                if new_data.startswith("ATTACK:"):
                    print("EINS-2")
                    new_data = new_data[7:]
                    var_change = new_data.split(":")
                    var = var_change[0]
                    var_value = var_change[1]
                    print(var)
                    print(var_value)
                    if var == "RECEIVED":
                        print("ZWEI-2")
                        new_data = new_data[9:]
                        var_change = new_data.split(":")
                        var = var_change[0]
                        var_value = var_change[1]
                        var_value = var_value.replace("+", "")
                        var_value.strip()
                        my_attacks.append(var_value)
                        print(var)
                        print(var_value)
                        if var == "HIT":
                            print("DREI-2")
                            my_hit_attacks.append(var_value)
                        elif var == "MISS":
                            print("VIER-2")
                            my_missed_attacks.append(var_value)
                    elif var == "OPPONENT":
                        print("FUNF-2")
                        new_data = new_data[9:]
                        var_change = new_data.split(":")
                        var = var_change[0]
                        var_value = var_change[1]
                        var_value = var_value.replace("+", "")
                        var_value.strip()
                        opponent_attacks.append(var_value)
                        if var == "HIT":
                            print("SECHS-2")
                            opponent_hit_attacks.append(var_value)
                        elif var == "MISS":
                            print("SIEBEN-2")
                            opponent_missed_attacks.append(var_value)
                if new_data.startswith("FUNC:"):
                    print("HEHE-A")
                    updated_data = new_data[5:]
                    updated_data = updated_data.replace("+", "")
                    updated_data = updated_data.strip()
                    if updated_data == "begin_game":
                        print("HEHE-B")
                        begin_game()
                    if updated_data == "restart_game":
                        begin_game()
                else:
                    new_data = new_data.replace("+", "")
                    new_data.strip()
                    print(new_data)
        except:
            pass

        if play_game:
            text_rendererTurn = text_font.render("MY TURN", False, (0,0,0))
            screen.blit(text_rendererTurn, (480, 25))
            if not my_turn:
                pygame.draw.line(screen, (255,255,255), (465,32), (580,32), 2)




        pygame.display.flip()
        pygame.display.update()

    elif end_screen:
        screen.blit(mainMenuBackground, (0, 0))


        activity_border = pygame.Rect(275, 135, 600, 350)
        activity_inner = pygame.Rect(295, 155, 560, 310)
        if game_result:
            pygame.draw.rect(screen, (0,200,0), activity_border)
        else:
            pygame.draw.rect(screen, (200,0,0), activity_border)
        pygame.draw.rect(screen, (255,255,255), activity_inner)

        text_renderer_game_result = game_result_font.render(server_result_message, False, (0,0,0))
        screen.blit(text_renderer_game_result, (activity_inner.x+175, activity_inner.y+25))

        play_again_button_border = pygame.Rect(activity_inner.x+185, activity_inner.y+85, 200, 45)
        pygame.draw.rect(screen, (0,0,95), play_again_button_border)

        main_menu_button_border = pygame.Rect(activity_inner.x+185, activity_inner.y+150, 200, 45)
        pygame.draw.rect(screen, (0,0,95), main_menu_button_border)

        text_renderer_play_again = menu_font.render("Rematch", False, (144,144,144))
        screen.blit(text_renderer_play_again, (play_again_button_border.x+25, play_again_button_border.y+8))

        text_renderer_main_menu = menu_font.render("Main Menu", False, (144,144,144))
        screen.blit(text_renderer_main_menu, (main_menu_button_border.x+13, main_menu_button_border.y+8))



        if play_again:
            text_renderer_awaiting_rematch = server_message_font.render("Waiting for opponent to rematch...", False, (144,144,144))
            screen.blit(text_renderer_awaiting_rematch, (main_menu_button_border.x-60, main_menu_button_border.y+80))



        for event in pygame.event.get(): # handles most user input events
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_button_border.collidepoint(event.pos):
                    play_again = True
                    client.send(f"VAR:play_again".encode("utf-8"))
                if main_menu_button_border.collidepoint(event.pos):
                    main_menu = True
                    end_screen = False




        try:
            new_data = client.recv(2048)
            new_data = new_data.decode()
            new_data = new_data.strip()
            if new_data.count("+") > 1:
                new_data = new_data.split("+")
                for data in new_data:
                    if data.startswith("FUNC:"):
                        updated_data = data[5:]
                        updated_data = updated_data.replace("+", "")
                        updated_data = updated_data.strip()
                        if updated_data == "restart_game":
                            begin_game()
                    else:
                        print(data)
            else:
                if new_data.startswith("FUNC:"):
                    updated_data = new_data[5:]
                    updated_data = updated_data.replace("+", "")
                    updated_data = updated_data.strip()
                    if updated_data == "restart_game":
                        begin_game()
                else:
                    print(new_data)
        except:
            pass

        pygame.display.flip()
        pygame.display.update()

pygame.quit()
sys.exit()
