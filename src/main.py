import json

import pygame

MAX_FPS = 60


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class Body:
    pos: list[float]
    vel: list[float]
    mass: float

    def __init__(self, pos: list[float], vel: list[float], mass: float):
        self.pos = pos
        self.vel = vel
        self.mass = mass

    def __str__(self) -> str:
        return f"Pos: [{self.pos[0]}, {self.pos[1]}, {self.pos[2]}]"


class Game:
    def __init__(self, width: int, height: int, filename: str):
        self.width = width
        self.height = height
        self.running = True
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.state_file = open(filename, "r")

        self.game_objects = self.parse_line()

        self.frame = 0

    def run(self):
        pygame.init()

        while self.running:
            self.clock.tick(MAX_FPS)

            self.screen.fill(Color.BLACK)

            self.check_events()

            self.draw()

            self.update()

            pygame.display.flip()

            pygame.image.save(
                self.screen, f"./screenshots/screenshot_{self.frame:05d}.png"
            )
            self.frame += 1

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        for body in self.game_objects:
            pygame.draw.circle(self.screen, Color.WHITE, (body.pos[0], body.pos[1]), 5)

    def update(self):
        self.game_objects = self.parse_line()

    def parse_line(self) -> list[Body]:
        game_objects = [
            Body(
                pos=item["pos"],
                vel=item["vel"],
                mass=item["mass"],
            )
            for item in json.loads(self.state_file.readline())
        ]
        return game_objects


if __name__ == "__main__":
    Game(width=1000, height=800, filename="test.json").run()
