import pygame
import sys
import random

pygame.mixer.init()
jump_sound = pygame.mixer.Sound('jumping.mp3')  # 점프 효과음
background_sound = pygame.mixer.Sound('marioMusic.mp3')  # 배경 음악
game_over_sound = pygame.mixer.Sound('gameOverMusic.mp3')  # 게임 오버 음악
background_sound.play(-1)

# 마리오 클래스 정의
class Mario:
    def __init__(self):
        self.x = 100
        self.y = 200
        self.jump = 0
        self.gravity = 5
        self.jumpspeed = 5
        image = pygame.image.load('superMario.png')
        self.image = pygame.transform.scale(image, (30, 50))
        self.invincible = False
        self.blink = False
        self.on_ground_or_sky = False
        self.continues = 0

    def update(self):
        self.y += self.gravity
        self.gravity += 0.2
        if self.jump:
            self.gravity = -self.jumpspeed
            self.jump -= 1

        if self.y <= 0 or self.y >= 600:
            self.on_ground_or_sky = True
        else:
            self.on_ground_or_sky = False

    def draw(self, window):
        if not self.blink:
            window.blit(self.image, (self.x, self.y))

# 파이프 클래스 정의
class Pipe:
    def __init__(self, current_speed):
        self.x = 400
        self.y = 0
        self.gap = random.randint(100, 300)
        self.width = 100
        self.speed = current_speed
        self.passed = False

    def update(self):
        self.x -= self.speed

    def draw(self, window):
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y, self.width, self.gap))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.gap + 200, self.width, 500))

# 점수 클래스 정의
class Score:
    def __init__(self):
        self.current_score = 0
        self.best_score = 0
        self.previous_speed = 0
        self.previous_time = 0
        self.font = pygame.font.Font(None, 24)

    def increment_score(self):
        self.current_score += 1
        self.update_best_score()

    def update_best_score(self):
        if self.current_score > self.best_score:
            self.best_score = self.current_score

    def reset_score(self):
        self.current_score = 0

    def draw(self, window):
        score_text = self.font.render(f"Score: {self.current_score}", True, (255, 255, 255))
        window.blit(score_text, (10, 10))

        best_score_text = self.font.render(f"Best: {self.best_score}", True, (255, 0, 0))
        window.blit(best_score_text, (window.get_width() - best_score_text.get_width() - 10, 10))

# 충돌 체크 함수
def collision(mario, pipes):
    if mario.invincible:
        return False
    mario_rect = pygame.Rect(mario.x, mario.y, 30, 50)

    for pipe in pipes:
        upper_pipe_rect = pygame.Rect(pipe.x, pipe.y, pipe.width, pipe.gap)
        lower_pipe_rect = pygame.Rect(pipe.x, pipe.y + pipe.gap + 200, pipe.width, 500)

        if mario_rect.colliderect(upper_pipe_rect) or mario_rect.colliderect(lower_pipe_rect):
            return True
    return False

# 게임 오버 화면 함수
def game_over(score, current_speed, game_time):
    global mario
    background_sound.stop()
    game_over_sound.play()
    text = font.render("Game Over", True, (255, 255, 255))
    scoreText = font.render(f"Your Score : {score.current_score}", True, (255, 0, 0))
    restart = font.render("Press R to replay", True, (255, 255, 255))
    cont = font.render("Press C to continue", True, (255, 255, 255))

    text_x = (window.get_width() - text.get_width()) // 2
    scoreText_x = (window.get_width() - scoreText.get_width()) // 2
    restart_x = (window.get_width() - restart.get_width()) // 2
    cont_x = (window.get_width() - cont.get_width()) // 2
    text_y = 300
    scoreText_y = text_y + 35
    restart_y = text_y + 70
    cont_y = text_y + 105

    window.blit(text, (text_x, text_y))
    window.blit(scoreText, (scoreText_x, scoreText_y))
    window.blit(restart, (restart_x, restart_y))
    window.blit(cont, (cont_x, cont_y))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    mario = Mario()
                    mario.blink = False
                    game_over_sound.stop()
                    background_sound.play(-1)
                    score.previous_speed = 2
                    score.previous_time = 0
                    score.reset_score()
                    return False, 2, 0
                elif event.key == pygame.K_c and not mario.on_ground_or_sky:
                    if mario.continues < 2:
                        game_over_sound.stop()
                        background_sound.play(-1)
                        score.previous_speed = current_speed
                        score.previous_time = game_time
                        mario.invincible = True
                        mario.continues += 1
                        pygame.time.set_timer(pygame.USEREVENT, 2000)
                        pygame.time.set_timer(pygame.USEREVENT + 1, 70)
                        return True, current_speed, game_time
                    else:
                        print("You have reached the maximum number of continues. Press R to restart.")

# 초기화 및 게임 창 설정
pygame.init()
window = pygame.display.set_mode((400, 600))
font = pygame.font.Font(None, 36)
timer_font = pygame.font.Font(None, 24)
score = Score()

# 게임 메인 루프
def game():
    global mario, last_speed_increase, current_speed, pipes
    mario = Mario()
    last_speed_increase = 0
    current_speed = 2
    game_start_time = pygame.time.get_ticks()
    pipes = [Pipe(current_speed)]
    clock = pygame.time.Clock()
    isRunning = True
    MAX_SPEED_INCREASE_TIME = 120

    while isRunning:
        game_time = (pygame.time.get_ticks() - game_start_time) // 1000

        if game_time <= MAX_SPEED_INCREASE_TIME:
            if game_time - last_speed_increase >= 5:
                current_speed += 0.1
                last_speed_increase = game_time
        else:
            current_speed = 4.4

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                mario.invincible = False
                mario.blink = False
                pygame.time.set_timer(pygame.USEREVENT, 0)
            elif event.type == pygame.USEREVENT + 1:
                if mario.invincible:
                    mario.blink = not mario.blink
                else:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump_sound.play()
                    mario.jump = 10
                    mario.gravity = 5

        mario.update()

        for i, pipe in enumerate(pipes):
            pipe.update()
            if pipe.x < -pipe.width:
                pipes.pop(i)
                pipes.append(Pipe(current_speed))
            if mario.y > 600 or mario.y < 0:
                isRunning, current_speed, game_time = game_over(score, current_speed, game_time)
            if mario.x > pipe.x + pipe.width and not pipe.passed:
                pipe.passed = True
                score.increment_score()

        if collision(mario, pipes):
            isRunning, current_speed, game_time = game_over(score, current_speed, game_time)

        window.fill((0, 120, 255))
        mario.draw(window)
        for pipe in pipes:
            pipe.draw(window)

        timer_text = timer_font.render(f"Time: {game_time // 60}:{game_time % 60:02}", True, (255, 255, 255))
        window.blit(timer_text, (window.get_width() / 2 - timer_text.get_width() / 2, 10))

        score.draw(window)

        pygame.display.update()
        clock.tick(90)

# 게임 루프 실행
while True:
    game()
