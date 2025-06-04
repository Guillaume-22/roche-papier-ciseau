from enum import Enum
import arcade


class AttackType(Enum):
    """ Simple énumération pour représenter les différents types d'attaques. """
    ROCK = 0,
    PAPER = 1,
    SCISSORS = 2


class AttackAnimation(arcade.Sprite):
    ATTACK_SCALE = 0.50
    ANIMATION_SPEED = 5.0
