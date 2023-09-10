from entities import *
from player import Player

# Rooms
from lobby import Lobby
from giftshop import GiftShop
from breakroom import Breakroom
from left import Left
from right import Right, colors
from central import Central


class Adventure(World):
    def __init__(self, name: str = "The Factory"):
        super().__init__(name)
        self.set_world(self)
        self.player = Player("No name")
        self.player.set_parent(self)
        self.player.set_world(self)
        Lobby().set_parent(self)
        GiftShop().set_parent(self)
        Breakroom().set_parent(self)
        Left().set_parent(self)
        Right().set_parent(self)
        Central().set_parent(self)

    def main(self):
        self.player.send_message((
            "$div"
            " _____ _\n"
            "|_   _| |__   ___\n"
            "  | | | '_ \ / _ \\\n"
            "  | | | | | |  __/\n"
            "  |_| |_| |_|\___|\n"
            " _____          _\n"
            "|  ___|_ _  ___| |_ ___  _ __ _   _\n"
            "| |_ / _` |/ __| __/ _ \| '__| | | |\n"
            "|  _| (_| | (__| || (_) | |  | |_| |\n"
            "|_|  \__,_|\___|\__\___/|_|   \__, |\n"
            "                              |___/\n"
            "$div"
            "Welcome to $room!\n"
            "I say \"Welcome\" out of politeness and habit, "
            "but in all honesty, you shouldn't be here.\n"
            "People get stuck here.  They cry and lose their minds...."
            "....well...\n"
            "Let's get to know you."
        ))
        self.player.name = self.player.ask("What's your name?")
        self.player.send_message("Great to meet you $player")
        options = []
        for color_id in colors.keys():
            options.append((color_id, colors[color_id]["name"]))
        self.player.favorite_color = self.player.ask_option("Out of these, what is your favorite color?", options, False)
        self.player.send_message("One more question.")
        while self.player.age < 10 or self.player.age > 99:
            self.player.age = self.player.ask_number("How old are you?")
            if self.player.age < 10:
                self.player.send_message("$age is a little young.  You seem older than that.")
            elif self.player.age > 99:
                self.player.send_message("$age is too old.  You seem younger than that.")
        self.player.send_message((
            "Age $color...favorite color...$age...right.  Something like that.\n"
            "Ok...well...everything seems to be in order.\n"
            "So head right in and I'll be right...\n"
            "\n"
            "<DOOR SLAMS BEHIND YOU!>"
        ))
        self.player.set_parent(self.rooms["Lobby"])
        while not self.done:
            self.player.look()


Adventure().main()
