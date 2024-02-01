import pygame
import sys
import random

pygame.mixer.init()  # 믹서 모듈 초기화
jump_sound = pygame.mixer.Sound('jumping.mp3')  # 점프 사운드 로드
background_sound = pygame.mixer.Sound('marioMusic.mp3')  # 배경 음악 로드
game_over_sound = pygame.mixer.Sound('gameOverMusic.mp3')  # 게임 오버 사운드 로드
background_sound.play(-1)  # 배경 음악 반복 재생

class Mario:
    def __init__(self):
        self.x = 100
        self.y = 200
        self.jump = 0
        self.gravity = 5
        self.jumpspeed = 5
        image = pygame.image.load('superMario.png')  # 이미지 로드
        self.image = pygame.transform.scale(image, (30, 50))  # 이미지 크기 조정
        self.invincible = False
        self.blink = False
        self.on_ground_or_sky = False  # add this line in your __init__ function
        self.continues = 0  # Number of continues used

    def update(self):
        self.y += self.gravity
        self.gravity += 0.2
        if self.jump:
            self.gravity = -self.jumpspeed
            self.jump -= 1

        # Update on_ground_or_sky based on Mario's y position
        if self.y <= 0 or self.y >= 600:  # replace with the dimensions of your ground and sky
            self.on_ground_or_sky = True
        else:
            self.on_ground_or_sky = False

    def draw(self, window):
        if not self.blink:
            window.blit(self.image, (self.x, self.y))


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
#파이프 이미지 추가ver
# class Pipe:
#     def __init__(self, current_speed):
#         self.x = 400
#         self.y = 0
#         self.gap = random.randint(100, 300)
#         self.width = 100
#         self.speed = current_speed
#         self.passed = False
#         image_upper = pygame.image.load('pipeUpper.png')  # load upper pipe image
#         image_lower = pygame.image.load('pipeLower.png')  # load lower pipe image
#         self.image_upper = pygame.transform.scale(image_upper, (self.width, 500))  # scale the upper pipe image
#         self.image_lower = pygame.transform.scale(image_lower, (self.width, 500))  # scale the lower pipe image
#
#     def update(self):
#         self.x -= self.speed
#
#     def draw(self, window):
#         window.blit(self.image_upper, (self.x, self.y))
#         window.blit(self.image_lower, (self.x, self.y + self.gap + 200))


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


def collision(mario, pipes):
    if mario.invincible:
        return False  # 무적 모드인 경우 바로 False 반환
    mario_rect = pygame.Rect(mario.x, mario.y, 30, 50)

    for pipe in pipes:
        upper_pipe_rect = pygame.Rect(pipe.x, pipe.y, pipe.width, pipe.gap)
        lower_pipe_rect = pygame.Rect(pipe.x, pipe.y + pipe.gap + 200, pipe.width, 500)

        if mario_rect.colliderect(upper_pipe_rect) or mario_rect.colliderect(lower_pipe_rect):
            return True
    return False

def game_over(score, current_speed, game_time):
    global mario
    background_sound.stop()
    game_over_sound.play()
    text = font.render("Game Over", True, (255, 255, 255))
    scoreText = font.render(f"Your Score : {score.current_score}", True, (255, 0, 0))
    restart = font.render("Press R to replay", True, (255, 255, 255))
    cont = font.render("Press C to continue", True, (255, 255, 255))

    # Calculate the positions to center the text
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
                sys. exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    mario = Mario()  # Reset Mario, which also resets the continues count
                    mario.blink = False
                    game_over_sound.stop()
                    background_sound.play(-1)
                    score.previous_speed = 2 # reset game speed
                    score.previous_time = 0 # reset game time
                    score.reset_score() # reset score
                    return False, 2, 0 # Reset game speed and time, then restart the game
                elif event.key == pygame.K_c and not mario.on_ground_or_sky:
                    if mario.continues < 2:  # Allow continue if it has been used less than 2 times
                        game_over_sound.stop()
                        background_sound.play(-1)
                        score.previous_speed = current_speed  # Save current speed
                        score.previous_time = game_time  # Save game time
                        mario.invincible = True  # Set invincible mode
                        mario.continues += 1  # Increment the count of continues used
                        pygame.time.set_timer(pygame.USEREVENT,
                                              2000)  # Set a timer to disable invincibility after 1 second
                        pygame.time.set_timer(pygame.USEREVENT + 1,
                                              70)  # Set a timer to toggle blinking every 0.1 seconds
                        return True, current_speed, game_time  # Play the game at current game speed and time
                    else:
                        print("You have reached the maximum number of continues. Press R to restart.")


# pygame 초기화
pygame.init()
window = pygame.display.set_mode((400, 600))
font = pygame.font.Font(None, 36)
timer_font = pygame.font.Font(None, 24)
score = Score()  # Score 객체 생성

def game():
    global mario, last_speed_increase, current_speed, pipes
    mario = Mario()
    last_speed_increase = 0
    current_speed = 2
    game_start_time = pygame.time.get_ticks()
    pipes = [Pipe(current_speed)]
    clock = pygame.time.Clock()
    isRunning = True
    MAX_SPEED_INCREASE_TIME = 120  # 2 minutes in seconds

    while isRunning:
        game_time = (pygame.time.get_ticks() - game_start_time) // 1000  # 게임 시간 계산

        if game_time <= MAX_SPEED_INCREASE_TIME:
            if game_time - last_speed_increase >= 5:
                current_speed += 0.1
                last_speed_increase = game_time
        else:
            current_speed = 4.4  # Set the speed to a fixed value after 2 minutes

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:  # 무적 모드 해제 이벤트
                mario.invincible = False
                mario.blink = False
                pygame.time.set_timer(pygame.USEREVENT, 0)  # 타이머 취소
            elif event.type == pygame.USEREVENT + 1:  # 깜빡임 토글 이벤트
                if mario.invincible:
                    mario.blink = not mario.blink
                else:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancel timer if not invincible
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

while True:
    game()
