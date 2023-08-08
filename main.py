import pygame
import random
import time


def get_sentence():
    with open('sentences.txt') as f:
        sentences = f.read().split('\n')
    return random.choice(sentences)


class TypeSpeedTest:
    def __init__(self):
        self.word = None
        self.reset = None
        self.end = None
        self.time_start = None
        self.input_text = None
        self.active = None
        self.running = None
        self.wpm = None
        self.total_time = None
        self.results = None
        self.accuracy = None
        self.width, self.height = 750, 500
        self.HEAD_C, self.TEXT_C, self.RESULT_C = (255, 213, 102), (240, 240, 240), (255, 70, 70)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Type Speed Test')
        self.open_img = pygame.transform.scale(pygame.image.load('type-speed-open.png'), (self.width, self.height))
        self.bg = pygame.transform.scale(pygame.image.load('background.jpg'), (500, 750))
        self.reset_game()

    def draw_text(self, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.width / 2, y))
        self.screen.blit(text, text_rect)

    def show_results(self):
        self.total_time = time.time() - self.time_start
        count = sum(1 for i, c in enumerate(self.word) if self.input_text[i] == c)
        self.accuracy = count / len(self.word) * 100
        self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
        self.results = f'Time: {round(self.total_time)}s Accuracy: {round(self.accuracy)}% Wpm: {round(self.wpm)}'
        self.screen.blit(pygame.transform.scale(pygame.image.load('icon.png'), (150, 150)),
                         (self.width / 2 - 75, self.height - 140))
        self.draw_text("Reset", self.height - 70, 26, (100, 100, 100))
        pygame.display.update()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update_screen()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                self.handle_key_event(event)

    def handle_mouse_click(self, pos):
        x, y = pos
        if 50 <= x <= 650 and 250 <= y <= 300:
            self.active, self.input_text, self.time_start = True, '', time.time()
        elif 310 <= x <= 510 and y >= 390 and self.end:
            self.reset_game()

    def handle_key_event(self, event):
        if self.active and not self.end:
            if event.key == pygame.K_RETURN:
                self.show_results()
                self.draw_text(self.results, 350, 28, self.RESULT_C)
                self.end = True
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

    def update_screen(self):
        self.screen.fill((0, 0, 0), (50, 250, 650, 50))
        pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)
        self.draw_text(self.input_text, 274, 26, (250, 250, 250))
        pygame.display.update()
        pygame.time.Clock().tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(1)
        self.reset, self.end, self.input_text, self.time_start, self.total_time, self.wpm = False, False, '', 0, 0, 0
        self.word = get_sentence()
        if not self.word:
            self.reset_game()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        self.draw_text("Typing Speed Test", 80, 80, self.HEAD_C)
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)
        self.draw_text(self.word, 200, 28, self.TEXT_C)
        pygame.display.update()


if __name__ == "__main__":
    game = TypeSpeedTest()
    game.run()
