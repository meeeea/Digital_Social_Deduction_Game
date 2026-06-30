import socket

from src.gui.TextBox import InputBox
from src.gui.Chat import Chat
from src.gui.Timer import Timer

from src.UserStateMatchine import UserStateMatchine

from select import select
from datetime import datetime

import pygame


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as S:
        try:
            S.connect(("127.0.0.1", 50007))
        except:
            print("\nFailed to connet to server")
            return    


        pygame.init()
        screen = pygame.display.set_mode((1600, 900))
        clock = pygame.time.Clock()
        FONT = pygame.font.Font(None, 32)
        running = True

        stateMatchine = UserStateMatchine(screen, FONT)

        end_time = 0

        while running:
            time = datetime.now()

            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                stateMatchine.Event_Handle(S, event)
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("white")
 
            if len(rec := select([S], [], [], 0)[0]):
                data = rec[0].recv(1024).decode().split()
                if data:
                    stateMatchine.Rec(data)
                    if data[0] == "time":
                        end_time = int(data[1])
                
            
            
            # UPDATE
            stateMatchine.Update(end_time, time)
           

            # RENDER 
            stateMatchine.draw(screen)

            # flip() the display to put your work on screen
            pygame.display.flip()

            dt = clock.tick(60) / 1000  # limits FPS to 60



        pygame.quit()

if __name__ == "__main__":
    main()
    pygame.quit()
