from support import QR, Scrolling, UI_Elements
import pygame as pg
import math
from datetime import date
import os
import configparser


def main():
    # it is HIGHLY reccomended that these exist, but you can change parameters such as size, position etc.
    global match_number, team_color, team_number
    match_number = UI_Elements.Counter(
        20, 80, 48, 1, "Match number", 24)

    team_color = UI_Elements.TeamColorToggle(200, 85, 'Color', 32, alliance_color)

    if matches:
        team_number = UI_Elements.Dropdown(
            350, 80, 100, 40, matches[match_number.value - 1][alliance_color], "Team number", 24)
        team_number.selected_num = alliance_number - 1
        team_number.opened = False
    else:
        team_number = UI_Elements.TextField(
            350, 80, 85, 40, 30, title='Team Number', title_size=24)

    # Initialize data input objects and headers here, QR code lists data in order of initialization
    prematch_header = UI_Elements.Header(32, 'Prematch', 24)
    
    start_position_image = UI_Elements.ImageArray(550, 70, 164, 183, ['assets/red side.png', 'assets/blue side.png'], title='Starting Position', title_size=24, linked_object=team_color)
    start_positions = UI_Elements.MultiCheckmark([UI_Elements.Checkmark(625, 80, '', 32), UI_Elements.Checkmark(625, 145, '', 32), UI_Elements.Checkmark(625, 210, '', 32)])

    auton_header = UI_Elements.Header(270, 'Autonomous', 24)

    a_top_cone = UI_Elements.Counter(20, 300, 48, 0, 'Top cones', 24, 'r')
    a_mid_cone = UI_Elements.Counter(20, 350, 48, 0, 'Mid cones', 24, 'r')
    a_bot_cone = UI_Elements.Counter(20, 400, 48, 0, 'Bot cones', 24, 'r')

    a_top_cube = UI_Elements.Counter(300, 300, 48, 0, 'Top cubes', 24, 'r')
    a_mid_cube = UI_Elements.Counter(300, 350, 48, 0, 'Mid cubes', 24, 'r')
    a_bot_cube = UI_Elements.Counter(300, 400, 48, 0, 'Bot cubes', 24, 'r')

    a_charging_station = UI_Elements.Dropdown(
        590, 305, 100, 32, ['No', 'Docked', 'Engaged'], 'Charging Station', 20)
    a_charging_station_example = UI_Elements.ImageArray(700, 305, 120, 120, ['assets/empty.png', 'assets/docked.png', 'assets/engaged.png'], linked_object=a_charging_station)
    a_left_community = UI_Elements.Checkmark(590, 450, 'Left Community', 32)

    teleop_header = UI_Elements.Header(500, 'Teleop', 24)

    t_top_cone = UI_Elements.Counter(20, 530, 48, 0, 'Top cones', 24, 'r')
    t_mid_cone = UI_Elements.Counter(20, 580, 48, 0, 'Mid cones', 24, 'r')
    t_bot_cone = UI_Elements.Counter(20, 630, 48, 0, 'Bot cones', 24, 'r')

    t_top_cube = UI_Elements.Counter(300, 530, 48, 0, 'Top cubes', 24, 'r')
    t_mid_cube = UI_Elements.Counter(300, 580, 48, 0, 'Mid cubes', 24, 'r')
    t_bot_cube = UI_Elements.Counter(300, 630, 48, 0, 'Bot cubes', 24, 'r')

    links_scored = UI_Elements.Counter(590, 550, 48, 0, 'Links Scored', 24)

    endgame_header = UI_Elements.Header(730, 'Endgame', 24)

    e_charging_station = UI_Elements.Dropdown(20, 770, 150, 32, [
                                              'No', 'Parked', 'Docked', 'Engaged'], 'Charging Station/Community', 24)
    e_charging_station_example = UI_Elements.ImageArray(180, 770, 150, 150, ['assets/empty.png', 'assets/parked.png', 'assets/docked.png', 'assets/engaged.png'], linked_object=e_charging_station)

    postmatch_header = UI_Elements.Header(960, 'Postmatch', 24)

    penalties = UI_Elements.Checkmark(20, 1000, 'Penalties?', 32)

    breakdown = UI_Elements.Checkmark(20, 1050, 'Robot Breakdown?', 32)
    
    tip = UI_Elements.Checkmark(420, 1000, 'Robot Tipped?', 32)

    defense = UI_Elements.Dropdown(20, 1130, 380, 40, [
                                   "Didn't Play Defense", "Played Defense Poorly", "Played Some Defense Well", "All Defense Very Well"], 'Defense', 24)

    comments = UI_Elements.TextField(
        420, 1080, 330, 300, 24, title='Comments/Breakdown Details', title_size=24)

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
            team_color.handleInput(event)


            # Generate and Reset buttons
            try: show_next = handleActionInputs(event, show_next)
            except UnboundLocalError: show_next = handleActionInputs(event, False)

            # handles scrolling from scroll offset
            handleScrolling(Scrolling.get_change(event))

        screen_w, screen_h = pg.display.get_surface().get_size()

        # updates UI elements
        UI_Elements.Header.update()
        UI_Elements.Counter.update()
        UI_Elements.Dropdown.update()
        UI_Elements.Checkmark.update()
        UI_Elements.MultiCheckmark.update()
        UI_Elements.TextField.update()
        team_color.update()
        UI_Elements.ImageArray.update()
        

        if matches and match_number.value > 0 and match_number.value <= len(matches):
            team_number.options = matches[match_number.value -
                                          1][team_color.value]
            team_number.option_renders = []
            for number in team_number.options:
                team_number.option_renders.append(team_number.font.render(number, 1, team_number.font_color))
            team_number.title = f'Team Number (#{team_number.selected_num + 1})'
            team_number.title_render = team_number.title_font.render(
                team_number.title, True, team_number.title_color)
        elif matches:
            team_number.options = ["Invalid!", "Invalid!", "Invalid!"]

            
        if team_color.value == 'red':
            start_position_image.x = 550
        else:
            start_position_image.x = 570

        drawDisplay(screen_w, screen_h, show_next)


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
alliance_color = config['Matches']['default_alliance_color']
alliance_number = int(config['Matches']['default_alliance_number'])

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
next_button_color = tuple(
    map(int, config['ActionButtons']['next_button_color'].split(',')))
next_text_color = tuple(
    map(int, config['ActionButtons']['next_text_color'].split(',')))

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
next_render = action_font.render('Next Match', 1, next_text_color)
next_rect = pg.Rect(
    action_buttons_pos[0] + generate_render.get_width() * 1.2, action_buttons_pos[1], next_render.get_width() * 1.1, action_buttons_size)

show_next = False

def compileData(seperator: str = ',') -> str:
    data = ''
    for element in UI_Elements.list:
        if type(element).__name__ == "Counter" or type(element).__name__ == "Checkmark" or type(element).__name__ == "MultiCheckmark" or type(element).__name__ == "TeamColorToggle":
            data += str(element.value) + seperator
        if type(element).__name__ == "Dropdown":
            data += element.selected_str + seperator
        if type(element).__name__ == "TextField":
            data += element.get_string().replace(seperator, "﹐") + seperator
    return data[:len(data) - len(seperator)]


def nextMatch():
    for element in UI_Elements.list:
        if type(element).__name__ == "Counter":
            if element != match_number:
                element.value = 0
        if type(element).__name__ == "Checkmark":
            element.value = False
        if type(element).__name__ == "MultiCheckmark":
            for checkmark in element.checkmark_list:
                checkmark.value = False
        if type(element).__name__ == "Dropdown":
            if element != team_number:
                element.selected_num = -1
                element.opened = True
        if type(element).__name__ == "TextField":
            element.content = ['']
            element.cursor_ln = 0

    handleScrolling(-Scrolling.scroll_off)
    Scrolling.scroll_off = 0
    
    match_number.value += 1


def handleScrolling(scroll_change):
    for element in UI_Elements.list:
        if type(element) != UI_Elements.MultiCheckmark:
            element.y -= scroll_change
    for multiCheckmark in UI_Elements.MultiCheckmark.multiCheckmark_list:
        for checkmark in multiCheckmark.checkmark_list:
            checkmark.y -= scroll_change
    # for header in UI_Elements.Header.header_list:
    #     header.y -= scroll_change
    # for counter in UI_Elements.Counter.counter_list:
    #     counter.y -= scroll_change
    # for checkmark in UI_Elements.Checkmark.checkmark_list:
    #     checkmark.y -= scroll_change
    # for dropdown in UI_Elements.Dropdown.dropdown_list:
    #     dropdown.y -= scroll_change
    # for textField in UI_Elements.TextField.textField_list:
    #     textField.y -= scroll_change
    # team_color.y -= scroll_change

    generate_rect.y -= scroll_change
    next_rect.y -= scroll_change


def handleActionInputs(event, show_next):
    if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
        mouse_pos = pg.mouse.get_pos()
        if generate_rect.collidepoint(mouse_pos):
            show_next = True
            QR.saveAndShow(str(date.today()) + '_Match_' + str(match_number.value) +
                           '_Team_' + (team_number.selected_str if matches else team_number.content[0]), compileData(), QR_display_size, pg.display.get_window_size(), QR_save_path)
        if show_next and next_rect.collidepoint(mouse_pos):
            nextMatch()
            show_next = False
    return show_next


def drawBackground(screen_w, screen_h):
    for x in range(math.floor(screen_w / BACKGROUND_W) + 1):
        for y in range(math.floor(screen_h / BACKGROUND_H) + 1):
            WIN.blit(BACKGROUND, (x * BACKGROUND_W, y * BACKGROUND_H))


def drawDisplay(screen_w, screen_h, show_next):
    drawBackground(screen_w, screen_h)
    
    for image in UI_Elements.ImageArray.imageArrayList:
        image.draw()
    for counter in UI_Elements.Counter.counter_list:
        counter.draw()
    for checkmark in UI_Elements.Checkmark.checkmark_list:
        checkmark.draw()
    # for multiCheckmark in UI_Elements.MultiCheckmark.multiCheckmark_list:
    #     multiCheckmark.draw()
    for dropdown in UI_Elements.Dropdown.dropdown_list:
        dropdown.draw()
    for textField in UI_Elements.TextField.textField_list:
        textField.draw()
    for header in UI_Elements.Header.header_list:
        header.draw()

    team_color.draw()

    pg.draw.rect(WIN, generate_button_color, generate_rect,
                 border_radius=action_buttons_size // 5)
    WIN.blit(generate_render, (generate_rect.x +
             generate_render.get_width() * .05, generate_rect.y - ((generate_render.get_height() - action_buttons_size) / 2)))
    
    if show_next:
        pg.draw.rect(WIN, next_button_color, next_rect,
                    border_radius=action_buttons_size // 5)
        WIN.blit(next_render, (next_rect.x +
                next_render.get_width() * .05, next_rect.y - ((next_render.get_height() - action_buttons_size) / 2)))

    Scrolling.drawScrollBar()

    pg.display.flip()


if __name__ == '__main__':
    main()
