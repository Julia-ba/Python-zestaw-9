"""
Zadanie 9.3 z zestawu 9
"""

import pygame
import random
import sys

# Stale
GAME_DURATION = 6 * 60 * 1000
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
FPS = 8
GROWTH = 1

# Kolory
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 25)

# Ladowanie i skalowanie obrazow
apple_img = pygame.image.load("apple.jpg")
poison_img = pygame.image.load("poison.png")
apple_img = pygame.transform.scale(apple_img, (GRID_SIZE, GRID_SIZE))
poison_img = pygame.transform.scale(poison_img, (GRID_SIZE, GRID_SIZE))


class Snake:
    """Reprezentuje weza sterowanego przez gracza."""
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)
        self.grow = 0

    def move(self):
        """
        Przesuwa weza o jeden segment w aktualnym kierunku.
        Obsluguje warunki brzegowe oraz zderzenie ze soba.
        Zwraca False, jesli nastapi zderzenie.
        """
        x, y = self.body[0]
        dx, dy = self.direction
        new_head = ((x + dx) % WIDTH, (y + dy) % HEIGHT)

        if new_head in self.body[:-1]:
            return False
        self.body.insert(0, new_head)
        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop()
        return True

    def change_direction(self, new_dir):
        """
        Zmienia kierunek ruchu weza.
        """
        dx, dy = new_dir
        cur_dx, cur_dy = self.direction
        if (dx, dy) != (-cur_dx, -cur_dy):
            self.direction = (dx, dy)

    def draw(self, surface):
        """
        Rysuje weza na powierzchni gry.
        """
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (*segment, GRID_SIZE, GRID_SIZE))


class Fruit:
    """Reprezentuje owoc (dobry lub zatruty) na planszy."""
    def __init__(self):
        self.pos = self.random_position()
        self.is_poisoned = random.random() < 0.25
        self.timer = 80

    def random_position(self):
        """
        Zwraca losowa pozycje na siatce planszy.
        """
        return (
            random.randrange(0, WIDTH, GRID_SIZE),
            random.randrange(0, HEIGHT, GRID_SIZE)
        )

    def update(self):
        """
        Aktualizuje licznik czasu zycia owocu.
        Zwraca True, jesli owoc jest nadal widoczny.
         """
        self.timer -= 1
        return self.timer > 0

    def draw(self, surface):
        """
        Rysuje owoc na powierzchni gry.
        """
        img = poison_img if self.is_poisoned else apple_img
        surface.blit(img, self.pos)


def show_intro():
    """
    Pokazuje ekran startowy informujacy o dobrych i zlych owocach.
    """
    screen.fill(BLACK)

    title = font.render("DOBRY I ZŁY OWOC", True, WHITE)
    desc = font.render("Zjedz dobry owoc  |  Unikaj zatrutego", True, WHITE)
    good_text = font.render("DOBRY", True, WHITE)
    bad_text = font.render("ZŁY", True, WHITE)

    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title, title_rect)

    desc_rect = desc.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(desc, desc_rect)

    ICON_Y = HEIGHT // 2 + 10
    LABEL_Y = ICON_Y + GRID_SIZE + 10

    OFFSET_X = 80

    GOOD_X = WIDTH // 2 - OFFSET_X
    BAD_X = WIDTH // 2 + OFFSET_X

    apple_rect = apple_img.get_rect(center=(GOOD_X, ICON_Y))
    screen.blit(apple_img, apple_rect)

    good_text_rect = good_text.get_rect(center=(GOOD_X, LABEL_Y))
    screen.blit(good_text, good_text_rect)

    poison_rect = poison_img.get_rect(center=(BAD_X, ICON_Y))
    screen.blit(poison_img, poison_rect)

    bad_text_rect = bad_text.get_rect(center=(BAD_X, LABEL_Y))
    screen.blit(bad_text, bad_text_rect)

    pygame.display.flip()
    pygame.time.wait(3500)

def main():
    show_intro()

    snake = Snake()
    fruit = Fruit()
    score = 0
    running = True
    speed_counter = 0
    fps = FPS

    start_time = pygame.time.get_ticks()

    while running:
        clock.tick(fps)
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, GAME_DURATION - elapsed_time)

        # Koniec gry po uplywie czasu
        if elapsed_time >= GAME_DURATION:
            running = False
            break

        # Obsluga zdarzen (klawisze, zamkniecie okna)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -GRID_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, GRID_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-GRID_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((GRID_SIZE, 0))

        if not snake.move():
            running = False

        if snake.body[0] == fruit.pos:
            if fruit.is_poisoned:
                score -= 1
                if score < 0:
                    running = False
            else:
                score += 1
                snake.grow += GROWTH
            fruit = Fruit()

        if not fruit.update():
            fruit = Fruit()

        # Zwiekszanie predkości
        speed_counter += 1
        if fps < 20 and speed_counter % 200 == 0:
            fps += 1

        screen.fill(BLACK)
        snake.draw(screen)
        fruit.draw(screen)

        # Wyswietlanie wyniku i czasu
        time_left_sec = remaining_time // 1000
        minutes = time_left_sec // 60
        seconds = time_left_sec % 60
        score_text = font.render(f"Wynik: {score}", True, WHITE)
        time_text = font.render(f"Czas: {minutes:02}:{seconds:02}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (WIDTH - 150, 10))

        pygame.display.flip()


    # Ekran koncowy
    screen.fill(BLACK)
    end_text = font.render(f"KONIEC GRY! Wynik: {score}", True, WHITE)
    screen.blit(end_text, (WIDTH // 2 - 150, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(4000)
    pygame.quit()

if __name__ == "__main__":
    main()


