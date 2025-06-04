"""
Roche papier ciseaux
Par Guillaume Lemieux 402
"""

import arcade
from random import randint
import attack_animation
from game_state import GameState
from attack_animation import AttackType
from attack_animation import AttackAnimation
from pyglet.event import EVENT_HANDLE_STATE

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Roche papier ciseaux"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.DARK_SKY_BLUE)
        # img_list est la liste pour l'image de l'utilisateur et de l'ordi
        self.img_list = arcade.SpriteList()
        self.faceBeard = arcade.Sprite("assets/faceBeard.png")
        self.faceBeard.width = 133
        self.faceBeard.height = 100
        self.faceBeard.center_x = width / 4
        self.faceBeard.center_y = height / 2
        self.compy = arcade.Sprite("assets/compy.png")
        self.compy.width = 133
        self.compy.height = 100
        self.compy.center_x = (width / 2) + (width / 4)
        self.compy.center_y = height / 2
        self.img_list.append(self.faceBeard)
        self.img_list.append(self.compy)

        #object_list est la liste pour les images de roches papiers et ciseaux
        self.object_list = arcade.SpriteList()
        self.SCISSORS = arcade.Sprite("assets/scissors.png")
        self.SCISSORS.center_x = width / 8
        self.SCISSORS.center_y = height / 3
        self.PAPER = arcade.Sprite("assets/spaper.png")
        self.PAPER.center_x = width / 3.7
        self.PAPER.center_y = height / 3
        self.ROCK = arcade.Sprite("assets/srock.png")
        self.ROCK.center_x = width / 2.5
        self.ROCK.center_y = height / 3
        self.object_list.append(self.SCISSORS)
        self.object_list.append(self.PAPER)
        self.object_list.append(self.ROCK)

        #object_list_pc pour l'image du choix de l'ordi
        self.object_list_pc = arcade.SpriteList()
        self.SCISSORS_pc = arcade.Sprite("assets/scissors.png")
        self.SCISSORS_pc.center_x = (width / 2) + (width / 4)
        self.SCISSORS_pc.center_y = height / 3
        self.PAPER_pc = arcade.Sprite("assets/spaper.png")
        self.PAPER_pc.center_x = (width / 2) + (width / 4)
        self.PAPER_pc.center_y = height / 3
        self.ROCK_pc = arcade.Sprite("assets/srock.png")
        self.ROCK_pc.center_x = (width / 2) + (width / 4)
        self.ROCK_pc.center_y = height / 3

        self.game_state = GameState.NOT_STARTED
        self.player_attack = None
        self.pc_attack = None
        self.computer_attack_type = None
        self.player_point = 0
        self.pc_point = 0
        self.player_attack_selected = False
        self.player_state = None
        # AttackType.ROCK
        # self.computer_attack_type = AttackType.PAPER
        # self.computer_attack_type = AttackType.SCISSORS

    def on_draw(self):

        self.clear()
        self.img_list.draw()
        self.object_list.draw()
        # texte
        texte_rpc = arcade.Text("Roche Papier Ciseaux", 0, SCREEN_HEIGHT * 0.9, arcade.color.RED,
                                font_size=50, width=SCREEN_WIDTH, align="center")
        espace_rpc = arcade.Text("Appuyer sur espace pour commencer", 0, SCREEN_HEIGHT * 0.8,
                                 arcade.color.RED, font_size=42, width=SCREEN_WIDTH, align="center")
        text_actif = arcade.Text("Cliquer sur une image pour choisir", 0, SCREEN_HEIGHT * 0.8,
                                 arcade.color.RED, font_size=42, width=SCREEN_WIDTH, align="center")
        text_egalite = arcade.Text("Égalité", 0, SCREEN_HEIGHT * 0.6, arcade.color.RED, font_size=42,
                                   width=SCREEN_WIDTH, align="center")
        text_user_win = arcade.Text("VOUS AVEZ GAGNÉ LE POINT", 0, SCREEN_HEIGHT * 0.6,
                                    arcade.color.RED, font_size=42, width=SCREEN_WIDTH, align="center")
        text_pc_win = arcade.Text("L'ORDI A GAGNER LE POINT", 0, SCREEN_HEIGHT * 0.6,
                                  arcade.color.RED, font_size=42, width=SCREEN_WIDTH, align="center")
        text_player_win_game = arcade.Text("Vous avez gagné la partie!!!!", 0, SCREEN_HEIGHT * 0.8,
                                           arcade.color.RED, font_size=42, width=SCREEN_WIDTH, align="center")
        text_pc_win_game = arcade.Text("L'ordi a gagné la partie!!!!", 0, SCREEN_HEIGHT * 0.8,
                                       arcade.color.RED, font_size=42, width=SCREEN_WIDTH, align="center")
        text_player_pt = arcade.Text(f"Vous avez {self.player_point} points", SCREEN_WIDTH / 6, SCREEN_HEIGHT * 0.2,
                                     arcade.color.RED, font_size=25)
        text_pc_pt = arcade.Text(f"L'ordi a {self.pc_point} points", SCREEN_WIDTH / 1.5, SCREEN_HEIGHT * 0.2,
                                 arcade.color.RED, font_size=25)
        text_start_new_game = arcade.Text("Cliquer sur espace pour commencer une nouvelle partie.",
                                          0, SCREEN_HEIGHT * 0.67, arcade.color.RED, font_size=35,
                                          multiline=True, width=SCREEN_WIDTH, align="center")
        text_player_pt.draw()
        text_pc_pt.draw()
        texte_rpc.draw()
        if self.game_state == GameState.NOT_STARTED:
            espace_rpc.draw()
        elif self.game_state == GameState.ROUND_ACTIVE:
            text_actif.draw()
        elif self.game_state == GameState.ROUND_DONE:
            if self.player_state == 0:
                text_egalite.draw()
            elif self.player_state == 1:
                text_user_win.draw()
            elif self.player_state == 2:
                text_pc_win.draw()
            self.object_list.draw()
            self.object_list_pc.draw()
            espace_rpc.draw()
        elif self.game_state == GameState.GAME_OVER:
            text_start_new_game.draw()
            if self.player_point == 3:
                text_player_win_game.draw()
            elif self.pc_point == 3:
                text_pc_win_game.draw()

    def on_update(self, delta_time):

        if self.player_attack_selected and self.game_state == GameState.ROUND_ACTIVE:
            self.pc_attack = randint(0, 2)
            #print(self.pc_attack)

            self.object_list_pc.clear()
            if self.pc_attack == 0:
                self.computer_attack_type = AttackType.ROCK
                self.object_list_pc.append(self.ROCK_pc)
                #self.object_list.append(self.ROCK_pc)
            elif self.pc_attack == 1:
                self.computer_attack_type = AttackType.PAPER
                self.object_list_pc.append(self.PAPER_pc)
            elif self.pc_attack == 2:
                self.computer_attack_type = AttackType.SCISSORS
                self.object_list_pc.append(self.SCISSORS_pc)
            print(self.computer_attack_type)
            #code pour déterminer qui a gagné

            if self.computer_attack_type == self.player_attack:
                self.player_state = 0
                #self.partie_nulle = True
            elif ((self.computer_attack_type == AttackType.ROCK and self.player_attack == AttackType.PAPER)
                  or (self.computer_attack_type == AttackType.PAPER and self.player_attack == AttackType.SCISSORS)
                  or (self.computer_attack_type == AttackType.SCISSORS and self.player_attack == AttackType.ROCK)):
                self.player_state = 1
                self.player_point += 1
            elif ((self.computer_attack_type == AttackType.PAPER and self.player_attack == AttackType.ROCK)
                  or (self.computer_attack_type == AttackType.SCISSORS and self.player_attack == AttackType.PAPER)
                  or (self.computer_attack_type == AttackType.ROCK and self.player_attack == AttackType.SCISSORS)):
                self.player_state = 2
                self.pc_point += 1

            print(self.player_state)
            print(self.game_state)
            self.game_state = GameState.ROUND_DONE
            print(self.game_state)
            if self.player_point == 3 or self.pc_point == 3:
                self.game_state = GameState.GAME_OVER
            else:
                self.game_state = GameState.ROUND_DONE
        if self.game_state == GameState.NOT_STARTED:
            self.player_attack = None
            self.pc_attack = None
            self.computer_attack_type = None
            self.player_point = 0
            self.pc_point = 0
            self.player_attack_selected = False
            self.player_state = None
            self.object_list.clear()
            self.object_list.append(self.SCISSORS)
            self.object_list.append(self.PAPER)
            self.object_list.append(self.ROCK)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            if self.game_state == GameState.NOT_STARTED:
                self.game_state = GameState.ROUND_ACTIVE
            elif self.game_state == GameState.ROUND_DONE:
                self.player_attack_selected = False
                self.game_state = GameState.ROUND_ACTIVE
                self.object_list.clear()
                self.object_list.append(self.SCISSORS)
                self.object_list.append(self.PAPER)
                self.object_list.append(self.ROCK)
            elif self.game_state == GameState.GAME_OVER:
                self.game_state = GameState.NOT_STARTED

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.player_attack_selected is False:
            if self.ROCK.collides_with_point((x, y)):
                self.object_list.clear()
                self.object_list.append(self.ROCK)
                self.player_attack = AttackType.ROCK
                self.player_attack_selected = True
            elif self.PAPER.collides_with_point((x, y)):
                self.object_list.clear()
                self.object_list.append(self.PAPER)
                self.player_attack = AttackType.PAPER
                self.player_attack_selected = True
            elif self.SCISSORS.collides_with_point((x, y)):
                self.object_list.clear()
                self.object_list.append(self.SCISSORS)
                self.player_attack = AttackType.SCISSORS
                self.player_attack_selected = True
            print(self.player_attack)


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
