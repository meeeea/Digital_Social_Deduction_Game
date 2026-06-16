import socket
from TextBox import InputBox
from Chat import Chat
from select import select

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
        chat_input = InputBox(0, 7 * screen.get_height() / 8, screen.get_width(), screen.get_height() / 8, "", FONT)
        chat_reception = Chat(200, 100, screen.get_width() / 2, 7 * screen.get_height() / 8)

        print(screen.get_size())
        print(chat_input.get_size())


        while running:
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
 
            chat_input.update()
            rec, [], [] = select([S], [], [], 0)
            if len(rec):
                chat_reception.Add(rec[0].recv(1024).decode(), pygame.Color("white"))

           

            # RENDER YOUR GAME HERE
            chat_reception.Draw(screen)
            
            chat_input.draw(screen)

            # flip() the display to put your work on screen
            pygame.display.flip()

            dt = clock.tick(60) / 1000  # limits FPS to 60



        pygame.quit()

if __name__ == "__main__":
    main()
    pygame.quit()
