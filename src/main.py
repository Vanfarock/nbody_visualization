import json
import os

import ffmpeg
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
    def __init__(
        self, width: int, height: int, zoom: int, particle_radius: int, filename: str
    ):
        self.width = width
        self.height = height
        self.particle_radius = particle_radius
        self.zoom = zoom

        self.running = True
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.state_file = open(filename, "r")

        self.frame = 0

        self.game_objects = self.parse_line()

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
                self.screen, f"./screenshots/screenshot_{self.frame:05d}.jpg"
            )
            self.frame += 1

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    self.zoom *= 1.1
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.zoom /= 1.1

    def draw(self):
        for body in self.game_objects:
            pygame.draw.circle(
                self.screen,
                Color.WHITE,
                (body.pos[0], body.pos[1]),
                self.particle_radius,
            )

    def update(self):
        self.game_objects = self.parse_line()

    def parse_line(self) -> list[Body]:
        hw = self.width // 2
        hh = self.height // 2
        print(self.frame)
        if line := self.state_file.readline():
            game_objects = [
                Body(
                    pos=[
                        item["pos"][0] * self.zoom + hw,
                        item["pos"][1] * self.zoom + hh,
                        item["pos"][2],
                    ],
                    vel=item["vel"],
                    mass=item["mass"],
                )
                for item in json.loads(line)
            ]
            return game_objects

        self.running = False
        return []


def create_screenshots_folder(folder_name: str):
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        pass


def generate_video_from_simulation(input_folder: str, output_file: str):
    ffmpeg.input(
        "./screenshots/screenshot_%5d.jpg", pattern_type="sequence", framerate=60
    ).output(output_file, vcodec="libx264").run(
        capture_stdout=True, capture_stderr=True
    )


if __name__ == "__main__":
    folder_name = "screenshots"
    create_screenshots_folder(folder_name)

    game = Game(
        width=1000,
        height=800,
        zoom=100,
        particle_radius=1,
        # filename="infinity.json",
        # filename="predicted_infinity_v2.json",
        # filename="random_0.json",
        # filename="predicted_random_0.json",
        # filename="64_000_true.json",
        # filename="64_000_predicted.json",
        # filename="64_000_1_true.json",
        filename="64_000_1_predicted.json",
    )
    game.run()

    # try:
    #     print("Starting video parsing")
    #     generate_video_from_simulation(
    #         input_folder=f"./{folder_name}/*.png",
    #         output_file="simulation01.mp4",
    #     )
    # except Exception as e:
    #     print("stdout", e.stdout.decode("utf-8"))
    #     print("stderr", e.stderr.decode("utf-8"))
    #     raise e
