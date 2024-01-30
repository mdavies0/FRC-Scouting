import qrcode
import pygame as pg
import os

pg.font.init()


def saveAndShow(name: str, data: str, size: float, original_display_size: tuple, save_path: str):
    display = pg.display.set_mode((size, size + size // 16))

    # creates QR code
    img = qrcode.make(data)
    img.save(os.path.join(save_path, name + '.png'))
    img = pg.transform.scale(pg.image.load(
        os.path.join(save_path, name + '.png')), (size, size))

    arial = pg.font.SysFont('arial', size // 16)

    # displays QR code until user clicks
    showing = True
    while showing:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                showing = False

            if event.type == pg.QUIT:
                showing = False
        
        background = pg.Surface((size, size + size // 16))
        background.fill((255, 255, 255))
        display.blit(background, (0, 0))
        display.blit(img, (0, size // 16))
        display.blit(arial.render('Click to continue', 1,
                     (0, 0, 0), (255, 255, 255)), (size // 64, 0))
        pg.display.flip()

    # sets display to original size
    pg.display.set_mode(original_display_size, pg.RESIZABLE)
