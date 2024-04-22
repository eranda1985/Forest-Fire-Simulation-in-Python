import sys, random, os, time
import pygame
import matplotlib.pyplot as plt


SC_WIDTH, SC_HEIGHT = 800,800
MAP_WIDTH, MAP_HEIGHT = 20, 20
TILE_SIZE = 40
INITIAL_TREE_DENSITY = 0.99
GROW_CHANCE = 0.0
FIRE_CHANCE = 0.01
FIRE_SPREAD_CHANCE = 0.8
PAUSE_LENGTH = 0.5
SIM_LENGTH = 32
FIRES_LIMIT = 15

pygame.init()
screen = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))

TREE_IMG = pygame.image.load(os.path.join("Graphics", "Tree_Small.png")).convert_alpha()
FIRE_IMG = pygame.image.load(os.path.join("Graphics", "Fire_Small.png")).convert_alpha()


trees = []
fires = []

def main():
    forest = createNewForest()
    fire_counter = 0

    
    for _ in range(SIM_LENGTH):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
                
        tree_count = sum(row.count("T") for row in forest)
        tree_land_percentage = (tree_count/(MAP_HEIGHT*MAP_WIDTH))*100
        trees.append(tree_land_percentage)
        
        fire_count = sum(row.count("F") for row in forest)
        fire_land_percentage = (fire_count/(MAP_HEIGHT*MAP_WIDTH))*100
        fires.append(fire_land_percentage)        
        
                        
        next_forest = [["Empty" for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]
        
        screen.fill((137,234,123)) #light green
        displayForest(forest)
        
        #Build next forest
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if next_forest[y][x] != "Empty":
                    continue
                
                
                if (forest[y][x] == " ") and (random.random() <= GROW_CHANCE):
                    #A new tree is born!
                    next_forest[y][x] = "T"
                elif (forest[y][x] == "T") and (random.random() <= FIRE_CHANCE) and (fire_counter <= FIRES_LIMIT):
                    #Tree has been struck by lightning
                    next_forest[y][x] = "F"
                    fire_counter += 1
                elif forest[y][x] == "F":
                    for ix in range(-1,2):
                        for iy in range(-1,2):
                            if (x + ix) >= 0 and (y + iy) >= 0:
                                if (x + ix) <= (MAP_WIDTH-1) and (y + iy) <= (MAP_HEIGHT-1):
                                    if forest[y + iy][x + ix] == "T":
                                        if(random.random() <= FIRE_SPREAD_CHANCE) and (fire_counter <= FIRES_LIMIT):
                                            next_forest[y + iy][x + ix] = "F"
                                            fire_counter += 1
                    #delete tree after fire
                    next_forest[y][x] = " "
                    fire_counter -= 1
                    
                else:
                    next_forest[y][x] = forest[y][x]
        
        fire_counter = sum(ii.count("F") for ii in next_forest)
        print(f"fire counter value: {fire_counter}")
        forest = next_forest
        
        time.sleep(PAUSE_LENGTH) #Pause while loop for a short time
        
        
        pygame.display.update() #Update the screen

    # Following generates a plot indicating the tree percentage and fire percentage left at the end of steps.
    # Temporarily commented out.
    fig, ax = plt.subplots()
    ax.plot(trees, color = 'green', label = 'Trees')
    ax.plot(fires, color = 'red', label = 'Fire')
    ax.legend(loc = 'upper right')
    ax.set_xlabel("Time")
    ax.set_ylabel("Land Occupied (%)")
    plt.show()


#Initialise a Random Map of Trees
def createNewForest():
    map = [["T" if random.random() <= INITIAL_TREE_DENSITY else " " for x in range(MAP_WIDTH) ] for y in range(MAP_HEIGHT)]
    return map

def displayForest(forest):
    for x in range(MAP_WIDTH):
       for y in range(MAP_HEIGHT):
            if forest[y][x] == "T":
                screen.blit(TREE_IMG, (x*TILE_SIZE, y*TILE_SIZE))
            elif forest[y][x] == "F":
                screen.blit(FIRE_IMG, (x*TILE_SIZE, y*TILE_SIZE))


if __name__ == '__main__':
    main()