import typing


class Entity:
    def __init__(self, name: str):
        self.name: str = name
        self.world: typing.Optional[Entity] = None
        self.parent: typing.Optional[Entity] = None
        self.children: list[Entity] = []
        self.first_look = True

    def is_a(self, entity_type) -> bool:
        try:
            return type(self).__name__ == entity_type or isinstance(self, entity_type)
        except:
            return False

    def set_world(self, world):
        # Keep track of the world
        self.world = world
        # Force all children into the same world
        for child in self.children:
            child.set_world(self.world)
        return self

    def set_parent(self, parent):
        # Remove from existing parent
        if self.parent is not None:
            self.parent.remove_child(self)
        # Add to and keep track of parent
        if parent is not None:
            parent.add_child(self)
            self.parent = parent
        # Use parent to set the world
        while self.world is None and parent is not None:
            if parent.world is not None:
                self.set_world(parent.world)
            elif parent.is_a("World"):
                self.set_world(parent)
            parent = parent.parent
        return self

    def add_child(self, child):
        self.children.append(child)
        child.set_world(self.world)
        return self

    def remove_child(self, child):
        self.children.remove(child)
        return self

    def get_child_by_type(self, entity_type):
        for child in self.children:
            if child.is_a(entity_type):
                return child
        return None

    def get_child_by_name(self, name: str):
        for child in self.children:
            if child.name.lower() == name.lower():
                return child
        return None

    def get_description(self) -> str:
        return ""

    def get_visible(self) -> bool:
        return True

    def look(self):
        if self.world is not None and self.world.player is not None:
            self.world.player.send_message(self.get_description())
            self.first_look = False

    def send_message(self, message: str):
        if self.world is not None and self.world.player is not None:
            self.world.player.send_message(message)

    def ask(self, prompt: str, options: list[str] = []) -> str:
        if self.world is not None and self.world.player is not None:
            return self.world.player.ask(prompt, options)
        return ""

    def ask_number(self, prompt: str, num_digits: int = 0) -> int:
        if self.world is not None and self.world.player is not None:
            return self.world.player.ask_number(prompt, num_digits)
        return 0

    def get_options(self) -> list[(typing.Union[str, typing.Callable[[], None]], str)]:
        options = []
        for child in self.children:
            if child.get_visible():
                for child_option in child.get_options():
                    options.append(child_option)
        return options

    def ask_option(self, prompt: str, options: list[(typing.Union[str, typing.Callable[[], None]], str)], include_defaults=True) -> str:
        if self.world is not None and self.world.player is not None:
            return self.world.player.ask_option(prompt, options, include_defaults)
        return ""


class Item(Entity):
    def __init__(self, name: str):
        super().__init__(name)


class Room(Entity):
    def __init__(self, name: str):
        super().__init__(name)

    def get_options_prompt(self):
        return "What would you like to do?"

    def handle_option_answer(self, value: str):
        pass

    def look(self):
        super().look()
        if self.world is not None and self.world.player is not None:
            self.handle_option_answer(self.world.player.ask_option(self.get_options_prompt(), self.get_options()))


class World(Entity):
    def __init__(self, name: str):
        super().__init__(name)
        self.rooms: dict[str, Room] = {}
        self.player: typing.Optional[Entity] = None
        self.done = False
        self.win = False

    def add_child(self, child):
        super().add_child(child)
        if child.is_a(Room):
            self.rooms[child.name] = child

    def game_over(self, win: bool, message: str):
        self.player.send_message(message)
        self.win = win
        self.done = True

