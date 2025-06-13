from Connection import Connection
from Packet import Packet
from PacketEnums import Target, Command, Team, Value

class Character:
    def __init__(self, port: Connection, checksum: int, img_link: str, name: str, hp: int,
                 mp: int, attack: int, defense: int, speed: int, abilities: list):
        self.checksum = checksum
        self.img_link = img_link
        self.name = name
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.abilities = abilities

        self.port = port

    def send_packet(self, packet: Packet):
        self.port.transfer_packet(self, packet)

    def receive_packet(self, packet):
 

    def __str__(self):
        return f'''
=== CHARACTER {self.name} ===
 HP:  {self.hp}
 MP:  {self.mp}
 ATK: {self.attack}
 DEF: {self.defense}
 SPD: {self.speed}
 ABL: 
  {'\n  '.join([str(ability) for ability in self.abilities])}
        '''

    def __repr__(self):
        return f'''
            Character {self.name}, checksum {self.checksum} 
        '''
