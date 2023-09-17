from entities import *


class Drawings(Item):
    def __init__(self, name="Drawings"):
        super().__init__(name)
        self.checked = False

    def get_description(self) -> str:
        return "There are crayon drawings on the walls."

    def get_options(self) -> list[(typing.Union[str, typing.Callable[[], None]], str)]:
        options = []
        options.append((lambda: self.check(), "Check out the crayon drawings on the walls."))
        return options

    def check(self):
        self.checked = True
        self.send_message((
            "You check out all of the crayon drawings on the walls.\n"
            "You see 4 drawings of people in suits and lab coats.  They have names on them:\n"
            " --- Hank Little\n"
            " --- Barbara James\n"
            " --- Chuck Huitt\n"
            " --- Emily Johnson\n\n"
            "You remember!  Those are your brothers and sisters Hank, Barbara, Chuck, and Emily!\n\n"
            "All of you would play together and make up names and pretend you all worked together.\n"
            "They were never as imaginative as you, so would always use their real first names.\n\n"
            "This makes you smile.\n\n"
            "You also see a crayon drawing of someone in a flannel jacket.  It says:\n"
            " --- Employee of the month - $player\n"
            " --- aka - Sam Heart\n\n"
            "That's you!  You remember!\nYour name is Sam Heart!\n\n"
            "You feel the emotion and tears welling up.\n\n"
            "What is happening?"
        ))


class FactoryModel(Item):
    def __init__(self, name="Factory Model"):
        super().__init__(name)
        self.checked = False

    def get_description(self) -> str:
        return "A toy model of a building is in the middle of the room."

    def get_options(self) -> list[(typing.Union[str, typing.Callable[[], None]], str)]:
        options = []
        options.append((lambda: self.check(), "Check out the toy model."))
        return options

    def check(self):
        self.checked = True
        self.send_message((
            "You check out the toy model in the middle of the room.\n"
            "It's made of small boxes, some paper tubes, and what look like pieces of\n"
            "various other toys.  It looks like it has 6 rooms connected with hallways.\n"
            "The paper tubes look like smoke stacks.  There are pieces of wire taped down\n"
            "and running between the rooms to make it look high-tech.\n\n"
            "One of the rooms is covered with colorful stickers and drawings of music notes.\n"
            "Another room has math equations and pictures of the brain draw on it.\n"
            "There is a sign taped to the building that says:\n"
            " --- $world\n\n"
            "This was your favorite game to play with your brothers and sisters!\n"
            "You would pretend to be scientists, artists, and leaders trying to solve\n"
            "the worlds problems.\n\n"
            "You felt like you could accomplish anything!\n\n"
            "But why are you here now?"
        ))


class Playroom(Room):
    def __init__(self, name="Playroom"):
        super().__init__(name)
        Drawings().set_parent(self)
        FactoryModel().set_parent(self)

    def get_description(self) -> str:
        desc = "$div"
        if self.first_look:
            desc += (
                "Nostalgia overwhelms you!  You look around and see your childhood.\n"
                "You are in a simple room surrounded by crayon drawings.  Your eyes\n"
                "widen as you realize they are yours!  This is your playroom as a child."
            )
        else:
            desc += (
                "You are in your playroom."
            )
        for child in self.children:
            if child.get_visible() and not child.is_a("Player"):
                child_desc = child.get_description()
                if len(child_desc) > 0:
                    desc += "\n" + child_desc
        desc += "\nYou feel very safe here, but what is going on?  Are you dreaming?\n"
        return desc

    def get_options(self) -> list[(typing.Union[str, typing.Callable[[], None]], str)]:
        options = super().get_options()
        if self.get_child_by_type(Drawings).checked and self.get_child_by_type(FactoryModel).checked:
            options.append(("P", "Pinch yourself to wake up."))
            options.append(("S", "Stay here and keep play where it's safe."))
        return options

    def handle_option_answer(self, value: str):
        match value:
            case "P":
                self.send_message((
                    "You pinch yourself.\n"
                    "You are no longer in the playroom.\n"
                    "You hear beeping as you open your eyes.  You can't quite focus yet,\n"
                    "but you can tell you are laying down.\n"
                    "You can start to make out white walls around you.  You are in a bed.\n\n"
                    "You can hear excited people talking and footsteps coming close:\n\n"
                    " --- Sam is waking up!\n\n"
                    "You feel someone hold your hand.  You look to your left as your vision becomes more clear.\n\n"
                    " --- Mom! ... Dad!\n\n"
                ))
                self.world.game_over(True, "Congratulations!")
            case "S":
                self.world.restart = True
                self.world.game_over(True, "You decide to stay here and continue to play.")


#from test import test_world
#from player import Player
#player = Player("Jeff Walter Smith")
#playroom = Playroom()
#test_world([playroom], player)