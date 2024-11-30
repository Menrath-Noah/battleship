import pygame, sys, socket

pygame.init()


screen = pygame.display.set_mode((1100,650))


pygame.display.set_caption("Battleship")


outerBackground = pygame.image.load("./img/outerBackgroundResized.png").convert_alpha()

borderBarHorizontal = pygame.image.load("./img/borderBarTop.png").convert_alpha()
borderBarVertical = pygame.image.load("./img/borderBarSide.png").convert_alpha()


coords_used = []

SERVER_IP = '192.168.1.111'  # Change this to your server's IP address if needed
PORT = 5159  # Make sure this matches the server's port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    client.connect((SERVER_IP, PORT))
    print("***WELCOME TO THE SERVER!!!***")
except Exception as e:
    print("***CANNOT CONNECT***", e)
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
        client.sendall(f"{self.coord}".encode("utf-8"))

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
        print(f"I HAVE BEEN CLICKED AT: {self.coord}")



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
    def __init__(self, x=350, y=500):
        super().__init__(x, y)
        self.x_pos = x
        self.y_pos = y
        self.img = pygame.image.load("./img/2SquareBoat.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.default_x = 350
        self.default_y = 500
        self.last_x = 350
        self.last_y = 500
        self.blocks = 2






class FiveSquareBoat(Boat): # class for five square-long boat
    def __init__(self, x=100, y=500):
        super().__init__(x, y)
        self.x_pos = x
        self.y_pos = y
        self.img = pygame.image.load("./img/5SquareBoat.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.default_x = 100
        self.default_y = 500
        self.last_x = 100
        self.last_y = 500
        self.blocks = 5



text_font = pygame.font.SysFont("Roger Bold Serif", 28)

textBoardHome = {}
textBoardAway = {}


#grid = []
gridHome = {}
gridAway = {}


selected_attacked = []
missed_attacks = []
hit_attacks = []

create_game = True
select_ship_positions = True
play_game = False

ships = []
ships.append(TwoSquareBoat())
ships.append(FiveSquareBoat())

currently_selected = None
canceled_action = False

hovering_grid = False

game = True
while game:
    clock = 60

    screen.blit(outerBackground, (0, 0))

    screen.blit(borderBarHorizontal, (92, 92))
    screen.blit(borderBarHorizontal, (92, 459))
    screen.blit(borderBarVertical, (92, 92))
    screen.blit(borderBarVertical, (459, 92))

    screen.blit(borderBarHorizontal, (567, 92))
    screen.blit(borderBarHorizontal, (567, 459))
    screen.blit(borderBarVertical, (567, 92))
    screen.blit(borderBarVertical, (934, 92))



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
        confirm_button = pygame.Rect(225, 600, 100, 35)
        pygame.draw.rect(screen, (45, 25, 92), confirm_button)

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
                if button.rect.collidepoint(event.pos):
                    button.clicked()
                    if key in coords_used:
                        hit_attacks.append(key)
                    else:
                        missed_attacks.append(key)
            if not canceled_action and not currently_selected: # handles selecting a ship to move/place
                for ship in ships:
                    if ship.rect.collidepoint(event.pos) and select_ship_positions:
                        currently_selected = ship
                        currently_selected.update_coords()
                        print("YEPP")
            canceled_action = False
            if confirm_button:
                if confirm_button.collidepoint(event.pos):
                    client.sendall(f"SHIP-COORDS:{coords_used}".encode("utf-8"))
                    print("Ship Coords Locked-In!")
                    currently_selected = None
                    confirm_button = None
                    select_ship_positions = False
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
            if square.rect.collidepoint(mouse_pos): # ship snaps to hovered over square
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


    for button in missed_attacks:
        pygame.draw.circle(screen, (0,0,0), gridAway[button].rect.center, 10)
        # gridButtonAway[area]
    for button in hit_attacks:
        pygame.draw.line(screen, (255,0,0), (gridAway[button].rect.x + 5, gridAway[button].rect.y + 5), (gridAway[button].rect.x+30, gridAway[button].rect.y+30), 4)
        pygame.draw.line(screen, (255,0,0), (gridAway[button].rect.x + 5, gridAway[button].rect.y + 30), (gridAway[button].rect.x+30, gridAway[button].rect.y+5), 4)


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








    pygame.display.flip()
    pygame.display.update()

pygame.quit()
sys.exit()
