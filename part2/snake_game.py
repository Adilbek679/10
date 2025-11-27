import pygame, sys, random
from db_helper import update_user_score, get_score, save_game # функция для обновления очков в базе

def run_snake_game(current_user, snake=None, score=0, level=1, direction="right"):
    pygame.init()

    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Змейка")

    # background and sound
    background = pygame.transform.scale(pygame.image.load("images/back.png"), (800,800))
    pygame.mixer.init()
    eat_sound = pygame.mixer.Sound("images/eatsound.mp3")

    # snake images
    snake_imgs = {
        "head": {
            "up": pygame.transform.scale(pygame.image.load("images/snake/headu.png"), (50,50)),
            "right": pygame.transform.scale(pygame.image.load("images/snake/headr.png"), (50,50)),
            "down": pygame.transform.scale(pygame.image.load("images/snake/headd.png"), (50,50)),
            "left": pygame.transform.scale(pygame.image.load("images/snake/headl.png"), (50,50)),
        },
        "body_h": pygame.transform.scale(pygame.image.load("images/snake/body.png"), (32,32)),
        "body_v": pygame.transform.scale(pygame.image.load("images/snake/bodyver.png"), (32,32)),
        "turn": {
            "lu": pygame.transform.scale(pygame.image.load("images/snake/lu.png"), (32,32)),
            "ru": pygame.transform.scale(pygame.image.load("images/snake/ru.png"), (32,32)),
            "rd": pygame.transform.scale(pygame.image.load("images/snake/rd.png"), (32,32)),
            "ld": pygame.transform.scale(pygame.image.load("images/snake/ld.png"), (32,32)),
        },
        "tail": {
            "up": pygame.transform.scale(pygame.image.load("images/snake/tailu.png"), (32,32)),
            "right": pygame.transform.scale(pygame.image.load("images/snake/tailr.png"), (32,32)),
            "down": pygame.transform.scale(pygame.image.load("images/snake/taild.png"), (32,32)),
            "left": pygame.transform.scale(pygame.image.load("images/snake/taill.png"), (32,32)),
        }
    }

    # food images
    apple = pygame.transform.scale(pygame.image.load("images/apple.png"), (50,50))
    carrot = pygame.transform.scale(pygame.image.load("images/golden_carrot.png"), (50, 50))
    flesh = pygame.transform.scale(pygame.image.load("images/donteat.png"), (50, 50))

    foods = [
        {"img": apple, "value": 1, "type": "apple"},
        {"img": carrot, "value": 3, "type": "carrot"},
        {"img": flesh, "value": -5, "type": "flesh"}
    ]

    font = pygame.font.SysFont("Arial", 50, True)
    small_font = pygame.font.SysFont("Arial", 30, True)

    cell = 32
    fps = 8
    clock = pygame.time.Clock()

    def reset_game(snake=None, score=0, level=1, direction="right"):
        if snake is not None:
            # продолжаем с переданных данных
            food_x, food_y, cur_food, food_timer = spawn_food(snake)
            turns = []
            game_over = False
        else:
            # начинаем новую игру
            snake = [(100,100),(68,100),(36,100)]
            direction = "right"
            food_x, food_y, cur_food, food_timer = spawn_food(snake)
            turns = []
            game_over = False
            score = 0
            level = 1

        return snake, direction, food_x, food_y, cur_food, turns, game_over, score, level, food_timer


    def spawn_food(snake):
        food = random.choice(foods)
        while True:
            x = random.randint(2, 24) * cell
            y = random.randint(2, 24) * cell
            if (x, y) not in snake:
                food_timer = 4*fps if food["type"]=="flesh" else 8*fps
                return x, y, food, food_timer

    def next_pos(x,y,dir):
        if dir=="up": return (x, y-cell)
        if dir=="down": return (x, y+cell)
        if dir=="left": return (x-cell, y)
        if dir=="right": return (x+cell, y)

    def get_corner(prev, cur, nxt):
        px,py = prev; cx,cy = cur; nx,ny = nxt
        dx1,dy1 = cx-px, cy-py
        dx2,dy2 = nx-cx, ny-cy
        if dx1 > 0 and dy2 < 0: return snake_imgs["turn"]["ru"]
        if dy1 < 0 and dx2 > 0: return snake_imgs["turn"]["ld"]
        if dx1 < 0 and dy2 > 0: return snake_imgs["turn"]["ld"]
        if dy1 > 0 and dx2 > 0: return snake_imgs["turn"]["lu"]
        if dx1 > 0 and dy2 > 0: return snake_imgs["turn"]["rd"]
        if dy1 > 0 and dx2 < 0: return snake_imgs["turn"]["ru"]
        if dx1 < 0 and dy2 < 0: return snake_imgs["turn"]["lu"]
        if dy1 < 0 and dx2 < 0: return snake_imgs["turn"]["rd"]
        return None

    snake, direction, food_x, food_y, cur_food, turns, game_over, score, level, food_timer = reset_game(snake, score, level, direction)
    grow = 0
    paused = False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and e.type == pygame.KEYDOWN:
                # save score before resetting
                update_user_score(current_user[0], score, level)  # current_user[0] — id
                snake, direction, food_x, food_y, cur_food, turns, game_over, score, level, food_timer = reset_game(snake, score, level, direction)
                grow = 0
                fps = 8
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:  # выйти в меню
                    save_game(current_user[0], snake, score, level, direction)
                    return
                if e.key == pygame.K_p:  # пауза
                    paused = not paused
                    if paused:
                        save_game(current_user[0], snake, score, level, direction)


        keys = pygame.key.get_pressed()
        if not game_over and not paused:
            old = direction
            if keys[pygame.K_UP] and direction != "down": direction = "up"
            elif keys[pygame.K_DOWN] and direction != "up": direction = "down"
            elif keys[pygame.K_LEFT] and direction != "right": direction = "left"
            elif keys[pygame.K_RIGHT] and direction != "left": direction = "right"

            if old != direction:
                turns.append((snake[0][0], snake[0][1], direction))

            nx, ny = next_pos(*snake[0], direction)

            # border teleport
            if nx < 0: nx = 800 - cell
            elif nx > 800 - cell: nx = 0
            if ny < 0: ny = 800 - cell
            elif ny > 800 - cell: ny = 0

            snake.insert(0, (nx, ny))

            if pygame.Rect(nx, ny, 32, 32).colliderect(pygame.Rect(food_x, food_y, 50, 50)):
                if cur_food["type"] == "apple":
                    score += cur_food["value"]
                    grow += 1
                elif cur_food["type"] == "carrot":
                    score += cur_food["value"]
                    grow += cur_food["value"]
                    fps += 1
                elif cur_food["type"] == "flesh":
                    score += cur_food["value"]
                    for _ in range(5):
                        if len(snake) > 3:
                            snake.pop()
                        else:
                            game_over = True
                            break
                eat_sound.play(maxtime=1200)
                food_x, food_y, cur_food, food_timer = spawn_food(snake)

            if grow > 0:
                grow -= 1
            else:
                snake.pop()

            if snake[0] in snake[1:]:
                game_over = True

            food_timer -= 1
            if food_timer <= 0:
                food_x, food_y, cur_food, food_timer = spawn_food(snake)


        def save_record():
            if current_user:
                old_score, old_level = get_score(current_user[0])
                new_score = max(score, old_score)
                new_level = max(level, old_level)
                update_user_score(current_user[0], new_score, new_level)

        # Внутри цикла
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:  # выйти в меню
                    save_record()
                    return
            if game_over and e.type == pygame.KEYDOWN:
                save_record()
                snake, direction, food_x, food_y, cur_food, turns, game_over, score, level, food_timer = reset_game(snake, score, level, direction)


        # drawing
        screen.blit(background, (0,0))
        if game_over:
            save_game(current_user[0], snake, score, level, direction)
            screen.blit(background, (0,0))
            text = font.render("GAME OVER", True, (255,0,0))
            restart = small_font.render("Press any key to restart", True, (255,255,255))
            screen.blit(text, (250,350))
            screen.blit(restart, (220,420))
            pygame.display.update()

            paused = True  # временно "замораживаем" игру
            continue  # пропускаем остальной код движения



        # draw snake
        for i, (x,y) in enumerate(snake):
            if i == 0:
                screen.blit(snake_imgs["head"][direction], (x,y))
            elif i == len(snake)-1:
                tx, ty = snake[-1]
                px, py = snake[-2]
                if tx<px: taildir="left"
                elif tx>px: taildir="right"
                elif ty<py: taildir="up"
                else: taildir="down"
                screen.blit(snake_imgs["tail"][taildir], (tx,ty))
            else:
                prev, nxt = snake[i+1], snake[i-1]
                corner = get_corner(prev,(x,y),nxt)
                if corner: screen.blit(corner,(x,y))
                else:
                    img = snake_imgs["body_v"] if prev[0]==nxt[0] else snake_imgs["body_h"]
                    screen.blit(img,(x,y))


        # === Save record only when game ends or paused ===


        screen.blit(cur_food["img"], (food_x,food_y))

        food_seconds = food_timer // fps
        food_timer_text = small_font.render(f"Food: {food_seconds}", True, (255,255,0))
        screen.blit(food_timer_text,(650,10))

        score_text = small_font.render(f"Score: {score}", True, (255,255,255))
        level_text = small_font.render(f"Speed: {fps}", True, (255,255,0))
        screen.blit(score_text,(10,10))
        screen.blit(level_text,(10,40))

        # pause display
        if paused:
            pause_text = font.render("PAUSED", True, (255,255,0))
            screen.blit(pause_text, (300, 350))

        pygame.display.update()
        clock.tick(fps)
