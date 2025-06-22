from src.backend.character.Ability import Ability
import json

class Character:
    def __init__(self, checksum: int, img_link: str, name: str, hp: int,
                 mp: int, attack: int, defense: int, speed: int, abilities: list):
        self.checksum = checksum
        self.img_link = img_link
        self.loaded_image = None
        self.name = name
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.damage = 3 * attack
        self.abilities: list[Ability] = abilities

    def __str__(self):
        return f'''
=== CHARACTER {self.name} ===
 HP:  {self.hp}
 MP:  {self.mp}
 ATK: {self.attack}
 DEF: {self.defense}
 SPD: {self.speed}
 '''
        '''
 ABL: 
  {'\n  '.join([str(ability) for ability in self.abilities])}
        '''

    def __repr__(self):
        return json.dumps({
                          'checksum': self.checksum,
                          'img_link': self.img_link,
                          'name': self.name,
                          'hp': self.hp,
                          'mp': self.mp
        })
