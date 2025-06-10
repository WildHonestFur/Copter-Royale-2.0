#Screens: Leaderboard, Waiting Room, Mode Selection, Game, End Screen
#Tables: Status, Game, Data

import pygame
import mysql.connector

cnx = mysql.connector.connect(user='root', password='----', host='----')

cursor = cnx.cursor()
cursor.execute("USE copterroyale;")

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Copter Royale 2.0")

font_medium = pygame.font.SysFont('Courier New', 36)
font_small = pygame.font.SysFont('Courier New', 24)
font_mini = pygame.font.SysFont('Courier New', 20)

logo = pygame.image.load("title.png")
logo = pygame.transform.smoothscale(logo, (300, 300))

clock = pygame.time.Clock()
FPS = 60
running = True

frame = "login"

#Login part
active_box = None
username_text = ""
password_text = ""
loginerror = ""
user = None

#Home part
pcolor = (0, 0, 0)
changecolor = False
name = ""

#Stats part
user_stats = {
    "Games Won": None,
    "Top 3 Finishes": None,
    "Total Kills": None,
    "Average Kills": None,
    "Max Kills": None
}


def draw_button(rect, text, font, mouse_pos, color, colorclick, textcolor):
    background_rect = rect.move(-2, 2)
    if rect.collidepoint(mouse_pos):
        current_color = colorclick
        pygame.draw.rect(screen, current_color, background_rect, border_radius=4)
        
        text_surf = font.render(text, True, textcolor)
        text_rect = text_surf.get_rect(center=background_rect.center)
        screen.blit(text_surf, text_rect)
    else:
        pygame.draw.rect(screen, colorclick, background_rect, border_radius=4)
        current_color = color
        pygame.draw.rect(screen, current_color, rect, border_radius=4)
        
        text_surf = font.render(text, True, textcolor)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

def draw_input_box(rect, text, is_active, coloractive, colorinactive, is_password=False):
    pygame.draw.rect(screen, coloractive if is_active else colorinactive, rect, 2)
    display_text = '*' * len(text) if is_password else text
    txt_surface = font_small.render(display_text, True, (0, 0, 0))
    screen.blit(txt_surface, (rect.x + 10, rect.y + 8))

def create_hue_slider(width, height, saturation=0.8, value=0.95):
    slider = pygame.Surface((width, height))
    for x in range(width):
        color = pygame.Color(0)
        h = x / width * 360
        s = saturation
        v = value
        color.hsva = (h, s * 100, v * 100, 100)
        for y in range(height):
            slider.set_at((x, y), color)
    return slider

def login():
    global frame, running, username_text, password_text, loginerror
    mouse_pos = pygame.mouse.get_pos()

    login_button = pygame.Rect(WIDTH/2 - 225, 440, 200, 50)
    new_user_button = pygame.Rect(WIDTH/2 + 25, 440, 200, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if login_button.collidepoint(event.pos):
                username_text, password_text, loginerror = "", "", ""
                frame = "logging"
            elif new_user_button.collidepoint(event.pos):
                username_text, password_text, loginerror = "", "", ""
                frame = "newuser"

    screen.fill((200, 200, 200))
    logo_rect = logo.get_rect(center=(WIDTH/2, 170))
    screen.blit(logo, logo_rect)

    draw_button(login_button, "Login", font_medium, mouse_pos, (0, 95, 187), (0, 125, 222), (0, 0, 0))
    draw_button(new_user_button, "New User", font_medium, mouse_pos, (0, 95, 187), (0, 125, 222), (0, 0, 0))

def logging(typeval):
    global frame, running, active_box, username_text, password_text, loginerror, user, pcolor, name
    mouse_pos = pygame.mouse.get_pos()

    back_button = pygame.Rect(20, HEIGHT-70, 200, 50)
    enter_button = pygame.Rect(WIDTH - 220, HEIGHT-70, 200, 50)
    input_box_user = pygame.Rect(WIDTH/2 - 150, 350, 300, 40)
    input_box_pass = pygame.Rect(WIDTH/2 - 150, 430, 300, 40)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                frame = "login"
            elif enter_button.collidepoint(event.pos):
                if typeval == 'old':
                    query = f"SELECT password FROM users WHERE BINARY username = '{username_text}';"
                    cursor.execute(query)
                    data = cursor.fetchone()
                    if data is None or len(username_text) < 1 or len(password_text) < 1:
                        loginerror = "Invalid username/password"
                    else:
                        if data[0] == password_text:
                            user = username_text
                            frame = "home"
                            query = f"SELECT r, g, b FROM player WHERE BINARY user = '{user}';"
                            cursor.execute(query)
                            pcolor = cursor.fetchone()

                            query = f"SELECT name FROM player WHERE BINARY user = '{user}';"
                            cursor.execute(query)
                            name = cursor.fetchone()[0]
                            if name is None:
                                name = ""
                                query = f"UPDATE player SET name = '' WHERE BINARY user = '{user}';"
                                cursor.execute(query)
                                cnx.commit()
                        else:
                            loginerror = "Invalid username/password"
                else:
                    query = f"SELECT password FROM users WHERE BINARY username = '{username_text}';"
                    cursor.execute(query)
                    data = cursor.fetchone()
                    if data is not None:
                        loginerror = "Username taken"
                    else:
                        if len(username_text) < 1 or len(password_text) < 1:
                            loginerror = "Invalid username/password"
                        else:
                            query = f"INSERT INTO users VALUES ('{username_text}', '{password_text}');"
                            cursor.execute(query)
                            cnx.commit()
                            query = f"INSERT INTO player VALUES ('{username_text}', '', 242, 53, 48);"
                            cursor.execute(query)
                            cnx.commit()
                            user = username_text
                            query = f"INSERT INTO stats (user) VALUES ('{user}');"
                            cursor.execute(query)
                            cnx.commit()
                            pcolor = (242, 53, 48)
                            name = ""
                            frame = "home"
            if input_box_user.collidepoint(event.pos):
                active_box = "user"
            elif input_box_pass.collidepoint(event.pos):
                active_box = "pass"
            else:
                active_box = None

        elif event.type == pygame.KEYDOWN:
            if active_box == "user":
                if event.key == pygame.K_BACKSPACE:
                    username_text = username_text[:-1]
                    username_text = username_text.strip()
                elif event.key == pygame.K_TAB:
                    active_box = "pass"
                elif event.key <= 127 and event.unicode.isprintable() and len(username_text) < 20:
                    username_text += event.unicode
                    username_text = username_text.strip()
            elif active_box == "pass":
                if event.key == pygame.K_BACKSPACE:
                    password_text = password_text[:-1]
                    password_text = password_text.strip()
                elif event.key == pygame.K_TAB:
                    active_box = "user"
                elif event.key <= 127 and event.unicode.isprintable() and len(password_text) < 20:
                    password_text += event.unicode
                    password_text = password_text.strip()
 

    screen.fill((200, 200, 200))
    logo_rect = logo.get_rect(center=(WIDTH/2, 170))

    draw_input_box(input_box_user, username_text, active_box == "user", (0, 125, 222), (0, 95, 187), is_password=False)
    draw_input_box(input_box_pass, password_text, active_box == "pass", (0, 125, 222), (0, 95, 187), is_password=True)

    label_user = font_small.render("Username:", True, (0, 0, 0))
    label_pass = font_small.render("Password:", True, (0, 0, 0))
    screen.blit(label_user, (input_box_user.x, input_box_user.y - 25))
    screen.blit(label_pass, (input_box_pass.x, input_box_pass.y - 25))
    
    screen.blit(logo, logo_rect)
    text_surface = font_small.render(loginerror, True, (239, 37, 35))
    text_rect = text_surface.get_rect(center=(WIDTH/2, 500))
    screen.blit(text_surface, text_rect)

    draw_button(back_button, "Back", font_medium, mouse_pos, (0, 95, 187), (0, 125, 222), (0, 0, 0))
    draw_button(enter_button, "Enter", font_medium, mouse_pos, (0, 95, 187), (0, 125, 222), (0, 0, 0))

def home():
    global frame, running, pcolor, changecolor, name, active_box, user, user_stats
    mouse_pos = pygame.mouse.get_pos()

    out_button = pygame.Rect(20, HEIGHT-70, 200, 50)
    stats_button = pygame.Rect(WIDTH - 220, HEIGHT-70, 200, 50)
    color_button = pygame.Rect(WIDTH/2-100, 425, 50, 50)
    input_box_name = pygame.Rect(WIDTH/2 - 110, 350, 300, 40)

    slider_width = 220
    slider_height = 20
    slider_x = WIDTH//2 - slider_width//2 + 80
    slider_y = 440

    slider_surface = create_hue_slider(slider_width, slider_height)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if color_button.collidepoint(event.pos):
                changecolor = not changecolor
            if slider_x <= event.pos[0] <= slider_x + slider_width and slider_y <= event.pos[1] <= slider_y + slider_height and changecolor:
                hue = (event.pos[0] - slider_x) / slider_width * 360
                color = pygame.Color(0)
                color.hsva = (hue, 80, 95, 100)
                pcolor = color

                query = f"UPDATE player SET r = {pcolor.r}, g = {pcolor.g}, b = {pcolor.b} WHERE BINARY user = '{user}';"
                cursor.execute(query)
                cnx.commit()
            elif stats_button.collidepoint(event.pos):
                frame = 'stats'
                changecolor = False

                query = f"SELECT won, topthree, kills, kills/games, maxkills FROM stats WHERE BINARY user = '{user}';"
                cursor.execute(query)
                stat = cursor.fetchone()

                user_stats["Games Won"] = stat[0];
                user_stats["Top 3 Finishes"] = stat[1];
                user_stats["Total Kills"] = stat[2];
                user_stats["Average Kills"] = stat[3];
                user_stats["Max Kills"] = stat[4];        
                
            elif out_button.collidepoint(event.pos):
                frame = 'login'
                user = None
                user_stats = {
                    "Games Won": None,
                    "Top 3 Finishes": None,
                    "Total Kills": None,
                    "Average Kills": None,
                    "Max Kills": None
                }
                active_box = None
                
            if input_box_name.collidepoint(event.pos):
                active_box = "name"
            else:
                active_box = None

        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            if slider_x <= event.pos[0] <= slider_x + slider_width and slider_y <= event.pos[1] <= slider_y + slider_height and changecolor:
                hue = (event.pos[0] - slider_x) / slider_width * 360
                color = pygame.Color(0)
                color.hsva = (hue, 80, 95, 100)
                pcolor = color

                query = f"UPDATE player SET r = {pcolor.r}, g = {pcolor.g}, b = {pcolor.b} WHERE BINARY user = '{user}';"
                cursor.execute(query)
                cnx.commit()

        elif event.type == pygame.KEYDOWN:                
            if active_box == "name":
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                    name = name.strip()
                    query = f"UPDATE player SET name = '{name}' WHERE BINARY user = '{user}';"
                    cursor.execute(query)
                    cnx.commit()    
                elif event.key <= 127 and event.unicode.isprintable() and len(name) < 20:
                    name += event.unicode
                    name = name.strip()
                    query = f"UPDATE player SET name = '{name}' WHERE BINARY user = '{user}';"
                    cursor.execute(query)
                    cnx.commit()
 

    screen.fill((200, 200, 200))
    logo_rect = logo.get_rect(center=(WIDTH/2, 170))
    screen.blit(logo, logo_rect)
    
    text_surface = font_small.render("Color: ", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH/2-150, 450))
    screen.blit(text_surface, text_rect)

    draw_button(color_button, "", font_medium, mouse_pos, pcolor, tuple(map(lambda x: x-40, pcolor)), (0, 0, 0))
    
    text_surface = font_small.render("Name: ", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH/2-155, 370))
    screen.blit(text_surface, text_rect)
    
    draw_input_box(input_box_name, name, active_box == "name", (0, 125, 222), (0, 95, 187), is_password=False)

    draw_button(stats_button, "Stats", font_medium, mouse_pos, (0, 95, 187), (0, 125, 222), (0, 0, 0))
    draw_button(out_button, "Log Out", font_medium, mouse_pos, (0, 95, 187), (0, 125, 222), (0, 0, 0))

    if changecolor:
        screen.blit(slider_surface, (slider_x, slider_y))
        pygame.draw.rect(screen, (0, 0, 0), (slider_x, slider_y, slider_width, slider_height), 2)

        color_obj = pygame.Color(*pcolor)
        hue_pos = int((color_obj.hsva[0] / 360) * slider_width)
        pygame.draw.line(screen, (0, 0, 0), (slider_x + hue_pos, slider_y), (slider_x + hue_pos, slider_y + slider_height-2), 2)

def stats():
    global frame, running, user
    mouse_pos = pygame.mouse.get_pos()

    back_button = pygame.Rect(20, HEIGHT-70, 200, 50)
    leader_button = pygame.Rect(WIDTH - 220, HEIGHT-70, 200, 50)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(event.pos):
                frame = "home"
            
 

    screen.fill((200, 200, 200))
    logo_rect = logo.get_rect(center=(WIDTH/2, 170))
    screen.blit(logo, logo_rect)

    draw_button(back_button, "Back", font_medium, mouse_pos, (0, 95, 187), (0, 125, 222), (0, 0, 0))
    draw_button(leader_button, "Ranks", font_medium, mouse_pos, (0, 95, 187), (0, 125, 222), (0, 0, 0))

    row_height = 30
    col_width = 250
    num_rows = len(user_stats)
    num_cols = 2
    padding = 10

    table_width = num_cols * col_width
    table_height = num_rows * row_height

    stat_x = (WIDTH - table_width) // 2
    stat_y_start = (HEIGHT - table_height) // 2 + 110

    for i in range(num_rows + 1):
        y = stat_y_start + i * row_height
        pygame.draw.line(screen, (120, 120, 120), (stat_x, y), (stat_x + table_width, y), 1)

    pygame.draw.line(screen, (120, 120, 120), (stat_x + col_width, stat_y_start), (stat_x + col_width, stat_y_start + table_height), 1)
    pygame.draw.line(screen, (120, 120, 120), (stat_x, stat_y_start), (stat_x, stat_y_start + table_height), 1)
    pygame.draw.line(screen, (120, 120, 120), (stat_x + 2*col_width, stat_y_start), (stat_x + 2*col_width, stat_y_start + table_height), 1)

    for i, (label, value) in enumerate(user_stats.items()):
        label_surface = font_mini.render(label, True, (0, 0, 0))
        value_surface = font_mini.render(str(value), True, (0, 0, 0))

        label_pos = label_surface.get_rect(midleft=(stat_x + 10, stat_y_start + i * row_height + row_height // 2))
        value_pos = value_surface.get_rect(midleft=(stat_x + col_width + 10, stat_y_start + i * row_height + row_height // 2))

        screen.blit(label_surface, label_pos)
        screen.blit(value_surface, value_pos)



while running:
    if frame == "login":
        login()
    elif frame == 'logging':
        logging('old')
    elif frame == 'newuser':
        logging('new')
    elif frame == 'home':
        home()
    elif frame == 'stats':
        stats()
        

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
cnx.close()
