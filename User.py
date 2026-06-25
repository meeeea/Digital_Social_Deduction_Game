import socket
from GUI.TextBox import InputBox
from GUI.Chat import Chat
from GUI.Timer import Timer
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

        

        # CONTENTS
        chat_input = InputBox(0, 7 * screen.get_height() / 8, screen.get_width() / 3, screen.get_height() / 8, "", FONT)
        chat_reception = Chat(0, 0, screen.get_width() / 3, 7 * screen.get_height() / 8)
        game_timer = Timer(2 * screen.get_width() / 5, 0, screen.get_width() / 5, screen.get_height() / 8)

        end_time = 0

        while running:
            time = datetime.now()

            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                chat_reception.Event_Handle(event)
                if message := chat_input.handle_event(event):
                    S.sendall(f"message {message}".encode())
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("white")
 
            rec, [], [] = select([S], [], [], 0)
            if len(rec):
                data = rec[0].recv(1024).decode().split()
                if data[0] == "message":
                    chat_reception.Add(" ".join(data[1:]), pygame.Color("white"))
                if data[0] == "time":
                    end_time = int(data[1])
            
            
            game_timer.set_time(end_time - int(time.timestamp()))

           

            # RENDER YOUR GAME HERE
            chat_reception.Draw(screen)
            
            chat_input.draw(screen)

            game_timer.draw(screen)

            # flip() the display to put your work on screen
            pygame.display.flip()

            dt = clock.tick(60) / 1000  # limits FPS to 60



        pygame.quit()

if __name__ == "__main__":
    main()
    pygame.quit()
