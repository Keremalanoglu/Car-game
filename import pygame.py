import pygame
from pygame.locals import *
import random

pygame.init()

# here i made the screen height and width 
width = 500
height = 500
screen = (width, height)
screen = pygame.display.set_mode(screen)
pygame.display.set_caption("Car Racing Game")

# these are the calor for my game with their calor codes 
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)
gray = (128, 128, 128)

#This is my game settings
gameover = False
speed = 2
score = 0

# Marker sizes
marker_width = 10
marker_height = 50

#I set up the road and edge markers
road = (100, 0, 300, height)
left_marker = (95, 0, marker_width, height)
rigth_marker = (395, 0, marker_width, height)

# these are the lane coordinates left right and center 
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# Animating the movement of the lane markers
lane_marker_xx = 0


class Car(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        # I scale the image size of the lanes to fit
        image_scale = 45 / image.get_rect().width
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Car):
    def __init__(self, x, y):
        image = pygame.image.load("image/car.png")
        super().__init__(image, x, y)


# Player starting point the crodinates 
player_loaction_one = 250
player_location_two = 400

# Creating the player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_loaction_one, player_location_two)
player_group.add(player)

#creating the other cars 
other_cars_images = ["pickup_truck.png", "taxi.png", "van.png", "semi_trailer.png"]

# Group for vehicles for using the other cars 
cars = pygame.sprite.Group()

#loading the crash image 

game_over_image = pygame.image.load("image/gameover.jpg")
game_over_rect = game_over_image.get_rect()



#This is my Game loop and car movements
clock = pygame.time.Clock()
fps = 120
run = True

while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        # Car movements and the left rigth movement 
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100


            for vehicle in cars:
                if pygame.sprite.collide_rect(player, vehicle):
                    gameover = True
    

                    if event.key ==K_LEFT:
                        player.rect.left = vehicle.rect.right
                        game_over_rect.center = [player.rect.left,(player.rect.center[1]+ vehicle.rect.center[1] / 2)]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left 
                        game_over_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]



    # Drawing the grass
    screen.fill(green)

    # The road and painting the road gray
    pygame.draw.rect(screen, gray, road)

    # The edge markers
    pygame.draw.rect(screen, yellow, left_marker)
    pygame.draw.rect(screen, yellow, rigth_marker)

    # Drawing the lane markers
    lane_marker_xx += speed * 2
    if lane_marker_xx >= marker_height * 2:
        lane_marker_xx = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_xx, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_xx, marker_width, marker_height))

    # adding the player's car to the screen 
    player_group.draw(screen)

    # Add up to two vehicles because there is 3 lane so i have to have max 2 car to pass them 
    if len(cars) < 2:
        add_vehicle = True
        for vehicle in cars:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:
            lane = random.choice(lanes)

            # Loading a random image from my other cars 
            image_file = random.choice(other_cars_images)
            image = pygame.image.load("image/" + image_file)

            # Create the vehicle
            vehicle = Car(image, lane, -100)  # Start off-screen
            cars.add(vehicle)

    # Move the other cars
    for vehicle in cars:
        vehicle.rect.y += speed

        # Remove cars that go off screen
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1

            # Speed up after every 5 cars passed
            if score > 0 and score % 5 == 0:
                speed += 1

    # Draw other cars in to the screen
    cars.draw(screen)


    # setting up the score 

    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render("score " + str(score),True ,white)
    text_rect = text.get_rect()
    text_rect.center = (50,450)
    screen.blit(text,text_rect)

    




    #check the collision to make if you hit the cars it crashes 

    if pygame.sprite.spritecollide(player ,cars , True ):
        gameover = True
        game_over_rect.center = [player.rect.center[0],player.rect.top]


    #displaying the game over 
    if gameover:
        screen.blit(game_over_image,game_over_rect)
        pygame.draw.rect(screen,red,(0,50,width,100))
        font = pygame.font.Font(pygame.font.get_default_font(),16)
        text = font.render("Game over suffer again ?(Press Y/N)",True,white )
        text_rect = text.get_rect()
        text_rect.center = (width /2, 100 )
        screen.blit(text,text_rect)
    
    
    # Update display
    pygame.display.update()


    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type  ==QUIT:
                gameover =False
                run = False
    #geting the players answer y/n
            if event.type == KEYDOWN:
                if event.key == K_y:
                    #reseting the game 
                    gameover = False 
                    speed = 3
                    score = 0
                    cars.empty()
                    player.rect.center = [player_loaction_one,player_location_two]
                elif event.key == K_n:
                    gameover = False
                    run = False 


pygame.quit()

