import pygame, sys

pygame.init()


screen = pygame.display.set_mode((600, 600))


pygame.display.set_caption("Battleship")


outerBackground = pygame.image.load("./img/outerBackground.png").convert_alpha()

borderBarHorizontal = pygame.image.load("./img/borderBarTop.png").convert_alpha()
borderBarVertical = pygame.image.load("./img/borderBarSide.png").convert_alpha()


coords_used = []


class GridButton: # individual grid squares
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
            for key, block in grid.items():
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
            for key, block in grid.items():
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
    def __init__(self, x=500, y=500):
        super().__init__(x, y)
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
        self.blocks = 2






class FiveSquareBoat(Boat): # class for five square-long boat
    def __init__(self, x=250, y=500):
        super().__init__(x, y)
        self.x_pos = x
        self.y_pos = y
        self.img = pygame.image.load("./img/5SquareBoat.png").convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.default_x = 250
        self.default_y = 500
        self.last_x = 250
        self.last_y = 500
        self.blocks = 5




#grid = []
grid = {}

create_game = True
select_ship_positions = True

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



    if create_game: # creates the game board
        x_pos = 100-36
        y_pos = 100
        letter = 65
        num = 0
        for i in range(100):

            if i % 10 == 0 and i != 0:
                x_pos = 100
                y_pos += 36
                num = 1
                letter += 1
            else:
                x_pos += 36
                num += 1
            #grid.append(GridButton(x_pos, y_pos, letter, num))
            grid[f"{chr(letter)}{num}"] = GridButton(x_pos, y_pos, letter, num)

        create_game = False

    for button in grid.values(): # draws each individual square in the grid
        # screen.blit(button, (button.x_pos, button.y_pos))
        pygame.draw.rect(screen, (0, 157, 196), button.rect)
    #(211, 211, 211)
    #(64, 64, 64)
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
            for button in grid.values(): # prints out the square that was clicked
                if button.rect.collidepoint(event.pos):
                    button.clicked()
            if not canceled_action and not currently_selected: # handles selecting a ship to move/place
                for ship in ships:
                    if ship.rect.collidepoint(event.pos):
                        currently_selected = ship
                        currently_selected.update_coords()
                        print("YEPP")
            canceled_action = False
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
        for square in grid.values():
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


    # print(grid.keys())

    print(coords_used)

    pygame.display.flip()
    pygame.display.update()

pygame.quit()
sys.exit()
