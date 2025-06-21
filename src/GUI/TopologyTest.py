from src.backend.CharacterParser import CharacterFactory
from src.backend.CharacterProcessor import CharacterProcessor
from src.backend.Connection import Connection
from src.backend.Host import Host
from src.backend.Inteface import Interface
from src.backend.NetInfo import NetInfo
from src.backend.PlayerProcessor import PlayerProcessor
from src.backend.Router import Router
from src.backend.Switch import Switch
from pathlib import Path
from src.GUI.drawables.ConnectionDrawable import ConnectionDrawable
from src.GUI.GameManager import GameManager
import pygame
from src.GUI.SurfaceRenderer import SurfaceRenderer
from multiprocessing import Process
from threading import Thread
from src.GUI.tracer_utils import setup_game

if __name__ == '__main__':
    print(Path('../characters').absolute())
    character = CharacterFactory().make_characters(Path('./characters'))[0]

    mainRouter = Router(NetInfo(-1, 0), 'net0.router')

    sw1 = Switch(NetInfo(1, 0), 'net1.switch')
    sw2 = Switch(NetInfo(2, 0), 'net2.switch')
    sw0 = Switch(NetInfo(0, 0), 'net0.switch')

    h11 = Host(NetInfo(1, 1), 'net1.host1', CharacterProcessor(character))
    h12 = Host(NetInfo(1, 2), 'net1.host2', CharacterProcessor(character))
    h21 = Host(NetInfo(2, 1), 'net2.host1', CharacterProcessor(character))
    h22 = Host(NetInfo(2, 2), 'net2.host2', CharacterProcessor(character))

    p1 = Host(NetInfo(0, 1), 'net0.player1', PlayerProcessor())
    p2 = Host(NetInfo(0, 2), 'net0.player2', PlayerProcessor())

    drawables = []

    rs1con = Connection(mainRouter, sw1)
    rs1con_drawable = ConnectionDrawable((500, 400), (326, 300))
    rs1con_drawable.connect(rs1con)
    drawables.append(rs1con_drawable)

    rs2con = Connection(mainRouter, sw2)
    rs2con_drawable = ConnectionDrawable((500, 400), (673, 300))
    rs2con_drawable.connect(rs2con)
    drawables.append(rs2con_drawable)

    rs0con = Connection(mainRouter, sw0)
    rs0con_drawable = ConnectionDrawable((500, 400), (500, 600))
    rs0con_drawable.connect(rs0con)
    drawables.append(rs0con_drawable)

    h1s1con = Connection(h11, sw1)
    h1s1con_drawable = ConnectionDrawable((200, 350), (326, 300))
    h1s1con_drawable.connect(h1s1con)
    drawables.append(h1s1con_drawable)

    h2s1con = Connection(h12, sw1)
    h2s1con_drawable = ConnectionDrawable((200, 250), (326, 300))
    h2s1con_drawable.connect(h2s1con)
    drawables.append(h2s1con_drawable)

    h1s2con = Connection(sw2, h21)
    h2s2con = Connection(sw2, h22)

    p1s0con = Connection(sw0, p1)
    p2s0con = Connection(sw0, p2)

    mainRouter.add_interface(Interface(NetInfo(1, 0), rs1con))
    mainRouter.add_interface(Interface(NetInfo(2, 0), rs2con))
    mainRouter.add_interface(Interface(NetInfo(0, 0), rs0con))

    sw1.connect_router(Interface(NetInfo(0, 0), rs1con))
    sw2.connect_router(Interface(NetInfo(0, 0), rs2con))
    sw0.connect_router(Interface(NetInfo(0, 0), rs0con))

    sw1.add_interface(Interface(NetInfo(1, 1), h1s1con))
    sw1.add_interface(Interface(NetInfo(1, 2), h2s1con))
    sw2.add_interface(Interface(NetInfo(2, 1), h1s2con))
    sw2.add_interface(Interface(NetInfo(2, 2), h2s2con))
    sw0.add_interface(Interface(NetInfo(0, 1), p1s0con))
    sw0.add_interface(Interface(NetInfo(0, 2), p2s0con))

    h11.connect_interface(Interface(NetInfo(1, 0), h1s1con))
    h12.connect_interface(Interface(NetInfo(1, 0), h2s1con))
    h21.connect_interface(Interface(NetInfo(2, 0), h1s2con))
    h22.connect_interface(Interface(NetInfo(2, 0), h2s2con))

    p1.connect_interface(Interface(NetInfo(0, 0), p1s0con))
    p2.connect_interface(Interface(NetInfo(0, 0), p2s0con))





    gui_thread = Thread(target=setup_game, args=[drawables])
    gui_thread.start()
    for i in range(10):
        mainRouter.handshake()
    gui_thread.join()

