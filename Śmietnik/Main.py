import pygame
from pyvidplayer2 import Video

# create video object
vid = Video("Hebe.mp4")

win = pygame.display.set_mode(vid.current_size)
pygame.display.set_caption(vid.name)

while vid.active:
    key = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vid.stop()
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)

    # only draw new frames, and only update the screen if something is drawn
    if vid.draw(win, (0, 0), force_draw=False):
        pygame.display.update()
    pygame.time.wait(16) # around 60 fps

# close video when done
vid.close()
pygame.quit()