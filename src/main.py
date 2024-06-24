import json
import os
import random

import ffmpeg
import pygame

MAX_FPS = 60


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (235, 64, 52)
    GREEN = (105, 232, 90)
    BLUE = (91, 148, 240)


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
        self,
        width: int,
        height: int,
        zoom: int,
        particle_radius: int,
        trail_thickness: int,
        max_trail_delay: int,
        filename: str,
    ):
        self.width = width
        self.height = height
        self.particle_radius = particle_radius
        self.zoom = zoom

        self.running = True
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.state_file = open(os.path.join(os.path.dirname(__file__), filename), "r")

        self.frame = 0

        self.game_objects = self.parse_line()
        self.trail_lines = []
        self.trail_thickness = trail_thickness
        self.max_trail_delay = max_trail_delay
        self.color_map = {
            0: Color.RED,
            1: Color.GREEN,
            2: Color.BLUE,
        }
        for i in range(3, len(self.game_objects)):
            self.color_map[i] = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

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
        for i, body in enumerate(self.game_objects):
            pygame.draw.circle(
                self.screen,
                self.color_map[i],
                (body.pos[0], body.pos[1]),
                self.particle_radius,
            )

        for i in range(1, len(self.trail_lines)):
            for j in range(len(self.trail_lines[i])):
                pygame.draw.line(
                    self.screen,
                    self.color_map[j],
                    (self.trail_lines[i][j][0], self.trail_lines[i][j][1]),
                    (self.trail_lines[i - 1][j][0], self.trail_lines[i - 1][j][1]),
                    int(self.trail_thickness * (1 - i / self.max_trail_delay)),
                )

    def update(self):
        self.game_objects = self.parse_line()

        self.trail_lines.insert(
            0, [(obj.pos[0], obj.pos[1]) for obj in self.game_objects]
        )
        if len(self.trail_lines) >= self.max_trail_delay:
            self.trail_lines.pop()

    def parse_line(self) -> list[Body]:
        hw = self.width // 2
        hh = self.height // 2
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
                if item["mass"] != 0
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
        particle_radius=15,
        trail_thickness=15,
        max_trail_delay=15,
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/10_true.json",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/10_predicted.json",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/infinity_true.json",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/ann_infinity.json",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/rnn_infinity.json",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/cnn_infinity.json",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/discovery_ann_infinity.json",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/discovery_rnn_infinity.json",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/discovery_cnn_infinity.json",
        filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/random_0.txt",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/random_8.txt",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/random_9.txt",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/random_10.txt",
        # filename="C:/Users/vinic/Documents/nbody_visualization/results/state_files/lagrange.txt",
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
