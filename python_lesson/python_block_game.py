import pygame
import sys
import time

#　初期化
pygame.init()

#　画面サイズ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ブロック崩し")

#　色の定義
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)

#　フォントの設定
font = pygame.font.Font(None, 36)

#　パドル
paddle_width = 100
paddle_height = 10
paddle_speed = 10
paddle_acceleration = 5
left_passed_time = 0
right_passed_time = 0
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 30, paddle_width, paddle_height)

# ボールの設定
ball_radius = 10
ball_speed_x = 5
ball_speed_y = 5
ball_speed_increment = 0.05
ball = pygame.Rect(screen_width // 2, screen_height // 2, ball_radius * 2, ball_radius * 2)

#　ブロックの設定
block_width = 60
block_height = 20
block_rows = 5
block_cols = 11
blocks = []
for row in range(block_rows):
    block_row = []
    for col in range(block_cols):
        block_x = col * (block_width + 10) + 20
        block_y = row * (block_height + 10)+ 35
        block = pygame.Rect(block_x, block_y, block_width, block_height)
        block_row.append(block)
    blocks.append(block_row)

# カウントダウンの数字
for i in range(3, 0, -1):
    screen.fill(black)
    countdown_text = font.render(f"Starting in {i}", True, white)
    screen.blit(countdown_text,(screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2 - countdown_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

running = True
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # パドルの操作
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] :
        left_passed_time += 1
        right_passed_time = 0
        paddle_speed = (10 + paddle_acceleration * left_passed_time)
        if paddle.left > 0:
            paddle.left -= paddle_speed
    elif keys[pygame.K_RIGHT] :
        left_passed_time = 0
        right_passed_time += 1
        paddle_speed = (10 + paddle_acceleration * right_passed_time)
        if paddle.right < screen_width:
            paddle.right += paddle_speed
    else:
        left_passed_time = 0
        right_passed_time = 0
        paddle_speed = 10


    # ボールの移動
    ball.left += ball_speed_x
    ball.top += ball_speed_y

    # ボールと壁の衝突
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_y += (1 + ball_speed_increment)
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y
        ball_speed_y += (1 + ball_speed_increment)
    if ball.bottom >= screen_height:
        running = False

    # ボールとパドルとの衝突判定
    if ball.colliderect(paddle):
        hit_position = (ball.left + ball.right) / 2 - (paddle.left + paddle.right) / 2
        ball_speed_x = hit_position * 0.3
        ball_speed_y += (1 + ball_speed_increment)
        ball_speed_y = -ball_speed_y

    # ボールとブロックの衝突判定
    for row in blocks:
        for block in row:
            if ball.colliderect(block):
                ball_speed_y += (1 + ball_speed_increment)
                ball_speed_y = -ball_speed_y
                row.remove(block)
                score += 100
                break


    #　画面の描画
    screen.fill(black)
    pygame.draw.rect(screen, blue, paddle)
    pygame.draw.ellipse(screen, white, ball)
    for row in blocks:
        for block in row:
            pygame.draw.rect(screen, green, block)

    # スコアの表示
    score_text = font.render(f"Score:{score}", True, white)
    screen.blit(score_text, (10, 10))

    time.sleep(0.03)
    pygame.display.flip()

# ゲーム終了後のスコア表示
screen.fill(black)
final_score_text = font.render(f"Final Score: {score}", True, white)
exit_text = font.render("Press Enter to exit", True, white)
screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2 - final_score_text.get_height() - 20))
screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 - exit_text.get_height() + 20))
pygame.display.flip()

waiting_for_exit = True
while waiting_for_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            pygame.quit()
            sys.exit()