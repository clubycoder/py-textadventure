from entities import *


colors = {
    "purple": { "name": "Purple", "compliment": "yellow" },
    "red": { "name": "Red", "compliment": "green" },
    "orange": { "name": "Orange", "compliment": "blue" },
    "blue": { "name": "Blue", "compliment": "orange" },
    "green": { "name": "Green", "compliment": "red" },
    "yellow": { "name": "Yellow", "compliment": "purple" }
}


class ColorWheel(Item):
    def __init__(self, name="Color Wheel"):
        super().__init__(name)

    def get_description(self) -> str:
        return "There is a color wheel on the wall."

    def get_options(self) -> list[(typing.Union[str, typing.Callable[[], None]], str)]:
        options = [(lambda: self.check(), "Check the color wheel.")]
        return options

    def check(self):
        self.send_message(
            "The color wheel has 6 colors arranged to show you which ones\n"
            "are complimentary.  Complimentary colors are opposite on the wheel:\n"
            "      ___________\n"
            "     /\         /\\\n"
            "    /  \       /  \\\n"
            "   /    \ Red /    \\\n"
            "  /      \   /      \\\n"
            " / Purple \ / Orange \\\n"
            "/          V          \\\n"
            "|----------------------|\n"
            "\\          ^          /\n"
            " \\  Blue  / \\ Yellow /\n"
            "  \\      /   \\      /\n"
            "   \\    /     \\    /\n"
            "    \\  / Green \\  /\n"
            "     \\/_________\\/"
        )


class ColorButtons(Item):
    def __init__(self, name="Color Buttons"):
        super().__init__(name)
        self.active = False
        self.compliment_expected = None

    def get_visible(self) -> bool:
        return self.active

    def get_description(self) -> str:
        return "A row of 6 colored buttons are along the far wall."

    def get_options(self) -> list[(typing.Union[str, typing.Callable[[], None]], str)]:
        options = []
        if not self.world.rooms["Breakroom"].central_right_unlocked:
            options.append((lambda: self.press(), "Press a colored button."))
        return options

    def press(self):
        global colors

        options = []
        for color_id in colors.keys():
            options.append((color_id, colors[color_id]["name"]))
        color = self.ask_option("Press a colored button", options, False)
        self.send_message("You press the %s button and it lights up." % (color))
        if self.compliment_expected is not None:
            if color == self.compliment_expected:
                if color == colors[self.world.player.favorite_color]["compliment"]:
                    self.world.rooms["Breakroom"].central_right_unlocked = True
                    self.send_message((
                        "The colored buttons all light up and a celebratory tune plays\n"
                        "on the piano behind you.\n\n"
                        "<A LOUD CHIME COMES FROM THE BREAKROOM>"
                    ))
                else:
                    self.send_message("You hear a simple click and all of the buttons turn off.")
            else:
                self.send_message((
                    "You hear a buzzer.  Maybe that wasn't the color expected.\n"
                    "All of the buttons turn off."
                ))
            self.compliment_expected = None
        else:
            self.compliment_expected = colors[color]["compliment"]


class SheetMusicGuide(Item):
    def __init__(self, name="Sheet Music Guide"):
        super().__init__(name)

    def get_description(self) -> str:
        return "There is sheet music guide on the counter."

    def get_options(self) -> list[(typing.Union[str, typing.Callable[[], None]], str)]:
        options = [(lambda: self.read(), "Read sheet music guide.")]
        return options

    def read(self):
        self.send_message((
            "Looks like a cheat sheet for how to read sheet music:\n"
            "║---------F-------\n"
            "║               E \n"
            "║-------D---------\n"
            "║             C   \n"
            "║-----B-----------\n"
            "║           A     \n"
            "║---G-------------\n"
            "║         F       \n"
            "║-E---------------\n"
            "     D            \n"
            "       -C-        \n"
            "Lines: Every Good Boy Does Fine\n"
            "Spaces: FACE"
        ))


songs = {
    "M": {
        "name": "Mary Had a Little Lamb",
        "notes": "E-D-C-D-E-E-E-D-D-D-E-F-F",
        "sheet": (
            "║---------│---------│---------│---------|\n"
            "║         │         │         │         |\n"
            "║---------│---------│---------│---------|\n"
            "║         │         │         │         |\n"
            "║---------│---------│---------│---------|\n"
            "║         │         │         │         |\n"
            "║---------│---------│---------│---------|\n"
            "║         │         │         │   O O   │\n"
            "║-O-------│-O-O-O---│---------│-O-------│\n"
            "    O   O             O O O              \n"
            "     -O-                                 "
        )
    },
    "T": {
        "name": "Twinkle, Twinkle, Little Star",
        "notes": "G-G-D-D-E-E-D-C-C-B-B-A-A-G",
        "sheet": (
            "║---------│---------│---------│---------|\n"
            "║         │ O O     │         │         |\n"
            "║-----O-O-│-----O---│---------│---------|\n"
            "║         │         │ O O     │         |\n"
            "║---------│---------│-----O-O-│---------|\n"
            "║         │         │         │ O O     |\n"
            "║-O-O-----│---------│---------│-----O---|\n"
            "║         │         │         │         │\n"
            "║---------│---------│---------│---------│"
        )
    },
    "C": {
        "name": "Camptown Races",
        "notes": "D-D-B-D-E-D-B-B-A-B-A",
        "sheet": (
            "║---------│---------│---------│---------|\n"
            "║         │ O       │         │         |\n"
            "║-O-O---O-│---O-----│---------│---------|\n"
            "║         │         │         │         |\n"
            "║-----O---│-----O---│-O-------│-O-------|\n"
            "║         │         │   O     │   O     |\n"
            "║---------│---------│---------│---------|\n"
            "║         │         │         │         │\n"
            "║---------│---------│---------│---------│"
        )
    }
}


class MusicBook(Item):
    def __init__(self, name="Music Book"):
        super().__init__(name)

    def get_description(self) -> str:
        return "A music book is on the piano."

    def get_options(self) -> list[(typing.Union[str, typing.Callable[[], None]], str)]:
        options = [(lambda: self.read(), "Read the music book.")]
        return options

    def read(self):
        global songs

        options = []
        for song_id in songs.keys():
            options.append((song_id, songs[song_id]["name"]))
        song = self.ask_option("What song do you want to read?", options, False)
        message = songs[song]["name"] + "\n" + songs[song]["sheet"]
        self.send_message(message)


class Piano(Item):
    def __init__(self, name="Piano"):
        super().__init__(name)
        self.songs_played = {
            "M": False,
            "T": False,
            "C": False
        }
        self.num_songs_played = 0
        self.notes_played = ""

    def get_description(self) -> str:
        return (
            "A piano is in the middle of the room.  The piano has %d lights on it with %d lit."
        ) % (len(self.songs_played.keys()), self.num_songs_played)

    def get_options(self) -> list[(typing.Union[str, typing.Callable[[], None]], str)]:
        options = []
        if self.num_songs_played < len(self.songs_played.keys()):
            options.append((lambda: self.play_key(), "Play key on the piano."))
        return options

    def play_key(self):
        global songs

        if len(self.notes_played) > 0:
            self.send_message("So far you have played: %s" % (self.notes_played))
        prompt = (
            "┌┬──┬──┬─┬┬──┬──┬──┬─┬┬──┬──┬─┬┬──┬──┬──┬─┬─┬┐\n"
            "││  │  │ ││  │  │  │ ││  │  │ ││  │  │  │ │ ││\n"
            "││C#│D#│ ││F#│G#│A#│ ││C#│D#│ ││F#│G#│A#│ │ ││\n"
            "│└─┬┴─┬┘ │└─┬┴─┬┴─┬┘ │└─┬┴─┬┘ │└─┬┴─┬┴─┬┘ │ └┤\n"
            "│C │D │E │F │G │A │B │C │D │E │F │G │A │B │C │\n"
            "└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘\n"
        )
        key = self.ask(prompt, [
            'A', 'B', 'C', 'D', 'E', 'F', 'G',
            'A#', 'C#', 'D#', 'E#', 'F#', 'G#'
        ])
        self.notes_played += ("-" if len(self.notes_played) > 0 else "") + key.upper()
        for song_id in songs.keys():
            if songs[song_id]["notes"].startswith(self.notes_played):
                self.send_message("That sounded nice.")
                if songs[song_id]["notes"] == self.notes_played:
                    self.notes_played = ""
                    self.send_message("Very good! You finished playing %s." % (songs[song_id]["name"]))
                    if not self.songs_played[song_id]:
                        self.songs_played[song_id] = True
                        self.num_songs_played += 1
                        if self.num_songs_played >= len(self.songs_played.keys()):
                            self.parent.get_child_by_type(ColorButtons).active = True
                            self.send_message((
                                "The last light turns on on the piano.\n"
                                "As you played the last note, a row of colored buttons appear on the back wall."
                            ))
                        else:
                            self.send_message("Another light turns on on the piano.")

                return
        self.notes_played = ""
        self.send_message("Ew...that didn't sound right.  You should start over.")


class Right(Room):
    def __init__(self, name="Right"):
        super().__init__(name)
        SheetMusicGuide().set_parent(self)
        MusicBook().set_parent(self)
        Piano().set_parent(self)
        ColorWheel().set_parent(self)
        ColorButtons().set_parent(self)

    def get_description(self) -> str:
        desc = "You are in the Right Wing in a warm and inviting room.  You can feel inspiration and creativity in the air."
        for child in self.children:
            if child.get_visible() and not child.is_a("Player"):
                child_desc = child.get_description()
                if len(child_desc) > 0:
                    desc += "\n" + child_desc
        desc += "\nThere is a door behind you leading back to the breakroom.\n"
        return desc

    def get_options(self) -> list[(typing.Union[str, typing.Callable[[], None]], str)]:
        options = super().get_options()
        options.append(("B", "Go back to the breakroom."))
        return options

    def handle_option_answer(self, value: str):
        match value:
            case "B":
                self.send_message("You head back to the breakroom.")
                self.world.player.set_parent(self.world.rooms["Breakroom"])


from test import test_world
from player import Player
from breakroom import Breakroom
player = Player("Jeff")
player.favorite_color = "red"
right = Right()
piano: Piano = right.get_child_by_type(Piano)
piano.num_songs_played = 2
piano.songs_played["M"] = True
piano.songs_played["T"] = True
#piano.songs_played["C"] = True
piano.notes_played = "D-D-B-D-E-D-B-B-A-B"
test_world([right, Breakroom()], player)
