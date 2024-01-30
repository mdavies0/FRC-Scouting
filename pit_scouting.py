from support import QR, Scrolling, UI_Elements
import pygame as pg
import math
from datetime import date
import os
import configparser


def main():
    # it is HIGHLY reccomended that these exist, but you can change parameters such as size, position etc.
    global match_number, team_color, team_number

    if matches:
        team_number = UI_Elements.Dropdown(
            20, 70, 80, 40, matches[match_number.value - 1]['red'], "Team number", 24)
    else:
        team_number = UI_Elements.TextField(
            20, 70, 80, 40, 30, title='Team Number', title_size=24)

    # Initialize data input objects and headers here, QR code lists data in order of initialization

    header = UI_Elements.Header(20, "Pit Scouting", 24)
    
    drivetrain_type = UI_Elements.Dropdown(180, 70, 150, 40, ["Mecanum", "Swerve", "Tank", "Other"], "Drivetrain Type", 24)
    
    cubes = UI_Elements.Checkmark(360, 70, "Can it score cubes?", 32)
    cones = UI_Elements.Checkmark(360, 110, "Can it score cones?", 32)
    
    level_1 = UI_Elements.Checkmark(360, 150, "Can it score level 1?", 32)
    level_2 = UI_Elements.Checkmark(360, 190, "Can it score level 2?", 32)
    level_3 = UI_Elements.Checkmark(360, 230, "Can it score level 3?", 32)

    charging_station = UI_Elements.Dropdown(360, 300, 400, 40, ["Can't Balance", "Can balance", "Balance with two other robots"], "Charging station", 24)
    
    auton = UI_Elements.TextField(20, 300, 300, 170, 30, title='What does it do in autonomous?', title_size=24)
    
    score_method = UI_Elements.TextField(20, 500, 300, 170, 30, title='How does it score?', title_size=24)
    
    notes = UI_Elements.TextField(360, 500, 400, 220, 30, title='Comments/Special Elements', title_size=24)

    #!!!=== All code below this line is for drawing the display, handling inputs, generating QR codes, etc. ===!!!
    #!!!===                 It is not reccomended to change anything below this line.                       ===!!!

    # main loop
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            # handles input for UI elements
            UI_Elements.TextField.handleInput(event)
            UI_Elements.Dropdown.handleInput(event)
            UI_Elements.Checkmark.handleInput(event)
            UI_Elements.Counter.handleInput(event)

            # Generate and Reset buttons
            handleActionInputs(event)

            # handles scrolling from scroll offset
            handleScrolling(Scrolling.get_change(event))

        screen_w, screen_h = pg.display.get_surface().get_size()

        # updates UI elements
        UI_Elements.Header.update()
        UI_Elements.Counter.update()
        UI_Elements.Dropdown.update()
        UI_Elements.Checkmark.update()
        UI_Elements.TextField.update()

        if matches:
            team_number.options = matches[match_number.value -
                                          1][team_color.value]

        drawDisplay(screen_w, screen_h)


pg.font.init()

WIN = pg.display.set_mode((800, 450))

# initialize other scripts
Scrolling.init()
UI_Elements.init()

# load settings from config file
config = configparser.ConfigParser()
config.read(os.path.basename(__file__)[0:-3] + '_config.ini')

matches = list(eval(config['Matches']['match_list'])
               ) if config['Matches']['match_list'] != '' else None

Scrolling.scroll_speed = int(config['Scrolling']['scroll_speed'])
Scrolling.display_height = int(config['Scrolling']['display_height'])

screen_w = int(config['Window']['screen_w'])
screen_h = int(config['Window']['screen_h'])
window_caption = config['Window']['window_caption']
window_icon_path = config['Window']['window_icon_path']
background_path = config['Window']['background_path']

action_buttons_pos = tuple(
    map(int, config['ActionButtons']['action_buttons_pos'].split(',')))
action_buttons_size = int(config['ActionButtons']['action_buttons_size'])
generate_button_color = tuple(
    map(int, config['ActionButtons']['generate_button_color'].split(',')))
generate_text_color = tuple(
    map(int, config['ActionButtons']['generate_text_color'].split(',')))
reset_button_color = tuple(
    map(int, config['ActionButtons']['reset_button_color'].split(',')))
reset_text_color = tuple(
    map(int, config['ActionButtons']['reset_text_color'].split(',')))

QR_display_size = int(config['QRCodes']['display_size'])
QR_save_path = config['QRCodes']['save_path']

WIN = pg.display.set_mode((screen_w, screen_h), pg.RESIZABLE)
pg.display.set_caption(window_caption)
icon = pg.image.load(window_icon_path)
pg.display.set_icon(icon)
BACKGROUND = pg.image.load(background_path)
BACKGROUND_W, BACKGROUND_H = BACKGROUND.get_size()

action_font = pg.font.SysFont('arial', action_buttons_size)
generate_render = action_font.render('Generate', 1, generate_text_color)
generate_rect = pg.Rect(
    action_buttons_pos[0], action_buttons_pos[1], generate_render.get_width() * 1.1, action_buttons_size)
reset_render = action_font.render('Reset', 1, reset_text_color)
reset_rect = pg.Rect(
    action_buttons_pos[0] + generate_render.get_width() * 1.2, action_buttons_pos[1], reset_render.get_width() * 1.1, action_buttons_size)


def compileData(seperator: str = ',') -> str:
    data = ''
    for element in UI_Elements.list:
        if type(element).__name__ == "Counter" or type(element).__name__ == "Checkmark" or type(element).__name__ == "TeamColorToggle":
            data += str(element.value) + seperator
        if type(element).__name__ == "Dropdown":
            data += element.selected_str + seperator
        if type(element).__name__ == "TextField":
            data += element.get_string() + seperator
    return data[:len(data) - len(seperator)]


def reset():
    for element in UI_Elements.list:
        if type(element).__name__ == "Counter":
            if element != match_number:
                element.value = 0
        if type(element).__name__ == "Checkmark":
            element.value = False
        if type(element).__name__ == "Dropdown":
            if element != team_number:
                element.selected_num = -1
                element.opened = True
        if type(element).__name__ == "TextField":
            element.content = ['']
            element.cursor_ln = 0

    handleScrolling(-Scrolling.scroll_off)
    Scrolling.scroll_off = 0


def handleScrolling(scroll_change):
    for header in UI_Elements.Header.header_list:
        header.y -= scroll_change
    for counter in UI_Elements.Counter.counter_list:
        counter.y -= scroll_change
    for checkmark in UI_Elements.Checkmark.checkmark_list:
        checkmark.y -= scroll_change
    for dropdown in UI_Elements.Dropdown.dropdown_list:
        dropdown.y -= scroll_change
    for textField in UI_Elements.TextField.textField_list:
        textField.y -= scroll_change

    generate_rect.y -= scroll_change
    reset_rect.y -= scroll_change


def handleActionInputs(event):
    if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
        mouse_pos = pg.mouse.get_pos()
        if generate_rect.collidepoint(mouse_pos):
            QR.saveAndShow(str(date.today()) + '_Pit_Team_' + (team_number.selected_str if matches else team_number.content[0]), compileData(
            ), QR_display_size, pg.display.get_surface().get_size(), QR_save_path)
        if reset_rect.collidepoint(mouse_pos):
            reset()


def drawBackground(screen_w, screen_h):
    for x in range(math.floor(screen_w / BACKGROUND_W) + 1):
        for y in range(math.floor(screen_h / BACKGROUND_H) + 1):
            WIN.blit(BACKGROUND, (x * BACKGROUND_W, y * BACKGROUND_H))


def drawDisplay(screen_w, screen_h):
    drawBackground(screen_w, screen_h)

    for counter in UI_Elements.Counter.counter_list:
        counter.draw()
    for checkmark in UI_Elements.Checkmark.checkmark_list:
        checkmark.draw()
    for dropdown in UI_Elements.Dropdown.dropdown_list:
        dropdown.draw()
    for textField in UI_Elements.TextField.textField_list:
        textField.draw()
    for header in UI_Elements.Header.header_list:
        header.draw()

    pg.draw.rect(WIN, generate_button_color, generate_rect,
                 border_radius=action_buttons_size // 5)
    WIN.blit(generate_render, (generate_rect.x +
             generate_render.get_width() * .05, generate_rect.y - ((generate_render.get_height() - action_buttons_size) / 2)))
    pg.draw.rect(WIN, reset_button_color, reset_rect,
                 border_radius=action_buttons_size // 5)
    WIN.blit(reset_render, (reset_rect.x +
             reset_render.get_width() * .05, reset_rect.y - ((reset_render.get_height() - action_buttons_size) / 2)))

    Scrolling.drawScrollBar()

    pg.display.flip()


if __name__ == '__main__':
    main()
