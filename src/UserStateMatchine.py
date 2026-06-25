import pygame
import socket

from src.gui.TextBox import InputBox
from src.gui.Chat import Chat
from src.gui.Timer import Timer

from src.states.userstates.Day import Day
from src.states.userstates.Lobby import Lobby
from src.states.userstates.Night import Night
from src.states.userstates.UserState import State

class UserStateMatchine:

    def __init__(self, screen, FONT):
        self.state = Day
        self.chat_input = InputBox(0, 7 * screen.get_height() / 8, screen.get_width() / 3, screen.get_height() / 8, "", FONT)
        self.chat_reception = Chat(0, 0, screen.get_width() / 3, 7 * screen.get_height() / 8)
        self.game_timer = Timer(2 * screen.get_width() / 5, 0, screen.get_width() / 5, screen.get_height() / 8)


    def Event_Handle(self, Conn, event):
        self.state.Event_Handle(event)
        self.chat_reception.Event_Handle(event)
        if message := self.chat_input.handle_event(event):
            Conn.sendall(f"message {message}".encode())

    def draw(self, screen):
        self.state.draw(screen)

        self.chat_reception.Draw(screen)
        self.chat_input.draw(screen)
        self.game_timer.draw(screen)

    def Rec(self, data):
        if data[0] == "message":
            self.chat_reception.Add(" ".join(data[1:]), pygame.Color("white"))

    def ShiftState(self, code):
        self.state = self.state.next(code)

    def Update(self, end_time, time):
        self.game_timer.set_time(end_time - int(time.timestamp()))