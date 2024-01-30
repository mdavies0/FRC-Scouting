import pygame as pg

scroll_off = 0
scroll_change = 0
scroll_speed = 1

display_height = 1000


def init():
    global win
    win = pg.display.get_surface()


def get_off(event) -> float:
    global scroll_off
    global scroll_speed
    global selected
    screen_w, screen_h = pg.display.get_surface().get_size()
    mouse_x, mouse_y = pg.mouse.get_pos()
    if pg.mouse.get_pressed().__contains__(1) and mouse_x > pg.display.get_surface().get_size()[0] - 16:
        selected = True
    if not pg.mouse.get_pressed().__contains__(1):
        selected = False
    # calculates new scroll offset
    if screen_h >= display_height:
        scroll_off = 0
    if event.type == pg.MOUSEBUTTONDOWN and screen_h < display_height:
        # if True:
        if event.button == 4:
            scroll_off -= scroll_speed
            if scroll_off < 0:
                scroll_off = 0
        if event.button == 5:
            scroll_off += scroll_speed
            if scroll_off > display_height - screen_h:
                scroll_off = display_height - screen_h
        # if mouse is over scroll bar and click, scroll bar moves
    if selected and screen_h < display_height:
        if mouse_y > scroll_off * screen_h / display_height and mouse_y < (scroll_off * screen_h / display_height) + (screen_h ** 2 / display_height):
            scroll_off += pg.mouse.get_rel()[1] * display_height / screen_h
        else:
            if mouse_y < scroll_off * screen_h / display_height:
                scroll_off = mouse_y * display_height / screen_h
            else:
                scroll_off = (mouse_y - (screen_h ** 2 / display_height)) * display_height / screen_h
        if scroll_off < 0:
            scroll_off = 0
        if scroll_off > display_height - screen_h:
            scroll_off = display_height - screen_h

    pg.mouse.get_rel()
    # scroll_off = float(scroll_off)
    scroll_off = int(scroll_off)
    return scroll_off


def get_change(event) -> float:
    global scroll_change
    old_scroll_off = scroll_off
    # calculates difference between old and new scroll offset
    scroll_change = float(get_off(event) - old_scroll_off)
    return scroll_change


def drawScrollBar(thickness: float = 16):
    screen_w, screen_h = pg.display.get_surface().get_size()
    if screen_h < display_height:
        # define and draw scroll bar
        bar = pg.Surface((thickness, screen_h))
        bar.fill((150, 150, 150))
        bar.set_alpha(160)
        win.blit(bar, (screen_w - thickness, 0))

        # define and draw scroll bar handle
        scroller = pg.Surface((thickness, screen_h ** 2 / display_height))
        scroller.fill((200, 200, 200))
        scroller.set_alpha(160)
        win.blit(scroller, (screen_w - thickness,
                 scroll_off * screen_h / display_height))
