from entities import *
from player import Player


def test_world(rooms: list[Room], player: Player):
    world = World("The Factory")
    world.set_world(world)
    world.player = player
    world.player.set_parent(world)
    world.player.set_world(world)
    for room in rooms:
        room.set_parent(world)
    world.player.set_parent(rooms[0])
    while not world.done:
        world.player.look()
        world.player.pause()
