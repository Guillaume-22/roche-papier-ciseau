from enum import Enum
import arcade


class AttackType(Enum):
    """ Simple énumération pour représenter les différents types d'attaques. """
    ROCK = 0,
    PAPER = 1,
    SCISSORS = 2,
    ROCK_pc = 0,
    PAPER_pc = 1,
    SCISSORS_pc = 2


class AttackAnimation(arcade.Sprite):
    ATTACK_SCALE = 0.50
    ANIMATION_SPEED = 5.0

    def __init__(self, attack_type):
        super().__init__()

        self.attack_type = attack_type
        if self.attack_type == AttackType.ROCK or self.attack_type == AttackType.ROCK_pc:
            self.textures = [
                arcade.load_texture("assets/srock.png"),
                arcade.load_texture("assets/srock-attack.png"),
            ]
        elif self.attack_type == AttackType.PAPER or self.attack_type == AttackType.PAPER_pc:
            self.textures = [
                arcade.load_texture("assets/spaper.png"),
                arcade.load_texture("assets/spaper-attack.png"),
            ]
        else:
            self.textures = [
                arcade.load_texture("assets/scissors.png"),
                arcade.load_texture("assets/scissors-close.png"),
            ]

        self.scale = self.ATTACK_SCALE
        self.current_texture = 0
        self.set_texture(self.current_texture)
        self.animation_update_time = 1.0 / AttackAnimation.ANIMATION_SPEED
        self.time_since_last_swap = 0.0

    def on_update(self, delta_time: float = 1 / 60):
        # Update the animation.
        self.time_since_last_swap += delta_time
        if self.time_since_last_swap > self.animation_update_time:
            self.current_texture += 1
            if self.current_texture < len(self.textures):
                self.set_texture(self.current_texture)
            else:
                self.current_texture = 0
                self.set_texture(self.current_texture)
            self.time_since_last_swap = 0.0
