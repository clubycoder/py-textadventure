import typing
import os
import pickle
from entities import *
from player import Player

# Rooms
from lobby import Lobby
from giftshop import GiftShop
from breakroom import Breakroom
from left import Left
from right import Right, colors
from central import Central
from playroom import Playroom


saved_game_filename = "save.game"


def save(world: World):
    global saved_game_filename
    f = open(saved_game_filename, "wb")
    pickle.dump(world, f)
    f.close()


def load() -> typing.Optional[World]:
    global saved_game_filename
    if not os.path.isfile(saved_game_filename):
        return None
    f = open(saved_game_filename, "rb")
    world: World = pickle.load(f)
    f.close()
    return world


def delete():
    global saved_game_filename
    if os.path.exists(saved_game_filename):
        os.remove(saved_game_filename)


class Adventure(World):
    def __init__(self, name: str = "The Factory"):
        super().__init__(name)
        self.set_world(self)
        self.player = Player("No name")
        self.player.set_parent(self)
        self.player.set_world(self)
        self.intro_done = False
        self.restart = False
        Lobby().set_parent(self)
        GiftShop().set_parent(self)
        Breakroom().set_parent(self)
        Left().set_parent(self)
        Right().set_parent(self)
        Central().set_parent(self)
        Playroom().set_parent(self)

    def intro(self) -> bool:
        self.intro_done = True
        self.player.send_message((
            "$div"
            " _____ _          .oo( )( )o\n"
            "|_   _| |__   ___          o( )( )o\n"
            "  | | | '_ \ / _ \\      ┌──┐   o( )( )o\n"
            "  | | | | | |  __/      │  │         ┌──┐\n"
            "  |_| |_| |_|\___| ─────┴──┴──┐      │  │\n"
            " _____          _   ▀   ▀  ▀  │──────┴──┴─┐\n"
            "|  ___|_ _  ___| |_ ___  _ __ _   _  ▀  ▀ │\n"
            "| |_ / _` |/ __| __/ _ \| '__| | | |   ▀  │\n"
            "|  _| (_| | (__| || (_) | |  | |_| |      │\n"
            "|_|  \__,_|\___|\__\___/|_|   \__, |──────┴────\n"
            "                              |___/\n"
            "$div"
            "Welcome to $room!  Here we try to solve all of the worlds problems.\n"
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

    def main(self) -> bool:
        if not self.intro_done:
            self.intro()
        while not self.done:
            save(self)
            self.player.look()
            if not self.done:
                self.player.pause()
        return self.restart


world: Adventure = None
restart = True
while restart:
    if world is None:
        world = load()
        if world is not None:
            print("You left off at %s in %s." % (world.player.get_play_time(), world.player.parent.name))
            if not input("Start where you left off (y or n)? ").strip().lower().startswith("y"):
                delete()
                world = None
        if world is None:
            world = Adventure()
    restart = world.main()
    if world.win:
        delete()
    if restart:
        delete()
        world = None
