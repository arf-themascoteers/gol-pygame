from gol import GOL
import  pygame


if __name__ == '__main__':
    g = GOL()
    while True:
        game_over = g.play_step()
        if game_over == True:
            break
    pygame.quit()