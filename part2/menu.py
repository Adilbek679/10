import pygame, sys
from db_helper import get_user, create_user, get_leaderboard, get_score, get_connection, load_game
from snake_game import run_snake_game

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Snake Game Menu")

font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 30)

menu_items = ["Login/Register", "Start Game", "Leaderboard", "Profile", "Exit"]
selected_index = 0


background = pygame.transform.scale(pygame.image.load("images/menu_bg.png"), (800,800))

current_user = None

def draw_menu():
    screen.blit(background, (0,0))
    for i, item in enumerate(menu_items):
        color = (255, 0, 0) if i == selected_index else (255, 255, 255)
        text = font.render(item, True, color)
        screen.blit(text, (250, 150 + i*80))
    pygame.display.update()

def input_username():
    global current_user
    username = ""
    input_active = True
    while input_active:
        screen.blit(background, (0,0))
        prompt = small_font.render("Enter your username:", True, (255,255,255))
        screen.blit(prompt, (250,200))
        text_surf = font.render(username, True, (255,255,0))
        screen.blit(text_surf, (250,300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_ESCAPE:  
                    return None
                else:
                    username += event.unicode

    if username.strip() == "":
        return None 

    user = get_user(username)
    if not user:
        create_user(username)
        user = get_user(username)
    current_user = user
    return user



def show_leaderboard():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.username, user_score.score, user_score.level
        FROM user_score
        JOIN users ON users.id = user_score.user_id
        ORDER BY user_score.score DESC
        LIMIT 10
    """)
    leaders = cursor.fetchall()
    cursor.close()
    conn.close()

    running = True
    while running:
        screen.blit(background, (0,0))
        title = font.render("Leaderboard", True, (255,255,0))
        screen.blit(title, (250,50))
        for i, (username, score, level) in enumerate(leaders):
            line = small_font.render(f"{i+1}. {username} - Score: {score} - Level: {level}",
                                     True, (255,255,255))
            screen.blit(line, (250, 150 + i*40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


def show_continue_menu():
    running = True
    selected = 0
    options = ["Continue", "New Game"]
    while running:
        screen.fill((0,0,0))
        for i, opt in enumerate(options):
            color = (255,0,0) if i==selected else (255,255,255)
            screen.blit(font.render(opt, True, color), (300, 300 + i*60))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected == 0



def show_profile():
    global current_user
    if not current_user:
        return  

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT score, level FROM user_score
        WHERE user_id=%s
    """, (current_user[0],))
    data = cursor.fetchone()

    if data:
        score, level = data
    else:
        score, level = 0, 1

    cursor.close()
    conn.close()

    running = True
    while running:
        screen.blit(background, (0,0))
        title = font.render("Profile", True, (255,255,0))
        screen.blit(title, (300,50))

        name_text = small_font.render(f"Username: {current_user[1]}", True, (255,255,255))
        score_text = small_font.render(f"Record: {score}", True, (255,255,255))
        level_text = small_font.render(f"Level: {level}", True, (255,255,255))

        screen.blit(name_text, (250,200))
        screen.blit(score_text, (250,250))
        screen.blit(level_text, (250,300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


running = True
while running:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(menu_items)
            elif event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                choice = menu_items[selected_index]

                if choice == "Login/Register":
                    input_username()
                elif choice == "Start Game":
                    if current_user:
                        run_snake_game(current_user)
                elif choice == "Leaderboard":
                    if current_user:
                        show_leaderboard()
                elif choice == "Profile":
                    if current_user:
                        show_profile()
                elif choice == "Exit":
                    pygame.quit()
                    sys.exit()

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            for i in range(len(menu_items)):
                if 150 + i*80 <= my <= 150 + i*80 + 50:
                    selected_index = i
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                choice = menu_items[selected_index]

                if choice == "Login/Register":
                    input_username()
                elif choice == "Start Game":
                    if current_user:
                        saved = load_game(current_user[0])
                        if saved:
                            continue_game = show_continue_menu()
                            if continue_game:
                                snake, score, level, direction = saved
                                run_snake_game(current_user, snake, score, level, direction)
                            else:
                                run_snake_game(current_user)
                        else:
                            run_snake_game(current_user)

                elif choice == "Leaderboard":
                    if current_user:
                        show_leaderboard()
                elif choice == "Profile":
                    if current_user:
                        show_profile()
                elif choice == "Exit":
                    pygame.quit()
                    sys.exit()
