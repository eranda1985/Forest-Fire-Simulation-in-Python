import pygame 
import random

class Drone:
    def __init__(self, name:str) -> None:
        self.name = name
        self.position = pygame.Vector2(float(random.choice(range(20))),float(random.choice(range(20))))
    