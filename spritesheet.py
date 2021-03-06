import pygame
import json


class Spritesheet:
    """
    Defines the spritesheet manager.
    Used to convert each spritesheet into an dictionary of images by parsing the associated
    JSON metadata file.
    """

    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace("png", "json")
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def parse_sprite(self, name):
        """
        Parses the JSON metadata for the x, y, w, h of the image with the given name.
        Returns the image.
        """

        def get_sprite(self, x, y, w, h):
            """
            Returns a surface with image of the specific x, y, w, h from a spritesheet.
            """
            sprite = pygame.Surface((w, h))
            sprite.set_colorkey((0, 0, 255))  # sets a color to show empyness
            sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
            return sprite

        sprite = self.data["frames"][name]["frame"]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = get_sprite(self, x, y, w, h)
        return image

    def parse_box_sprites(self):
        """
        Returns a dictionary of all the individual sprites from the box spritesheet.
        """
        sheet = Spritesheet("Sprites/box_sheet.png")
        sprites = {
            "box_empty": sheet.parse_sprite("box_empty.png"),
            "box_1": sheet.parse_sprite("box_1.png"),
            "box_2": sheet.parse_sprite("box_2.png"),
            "box_3": sheet.parse_sprite("box_3.png"),
            "box_4": sheet.parse_sprite("box_4.png"),
            "box_5": sheet.parse_sprite("box_5.png"),
            "box_6": sheet.parse_sprite("box_6.png"),
            "box_7": sheet.parse_sprite("box_7.png"),
            "box_8": sheet.parse_sprite("box_8.png"),
            "box_bomb": sheet.parse_sprite("box_bomb.png"),
            "box_no_bomb": sheet.parse_sprite("box_no_bomb.png"),
            "box_red_bomb": sheet.parse_sprite("box_red_bomb.png"),
            "box_flag": sheet.parse_sprite("box_flag.png"),
            "box_full": sheet.parse_sprite("box_full.png"),
        }
        return sprites

    def parse_number_sprites(self):
        """
        Returns a list of all the individual sprites from the numbers spritesheet.
        """
        sheet = Spritesheet("Sprites/number_sheet.png")
        sprites = [
            sheet.parse_sprite("number_none.png"),
            sheet.parse_sprite("number_1.png"),
            sheet.parse_sprite("number_2.png"),
            sheet.parse_sprite("number_3.png"),
            sheet.parse_sprite("number_4.png"),
            sheet.parse_sprite("number_5.png"),
            sheet.parse_sprite("number_6.png"),
            sheet.parse_sprite("number_7.png"),
            sheet.parse_sprite("number_8.png"),
            sheet.parse_sprite("number_9.png"),
            sheet.parse_sprite("number_0.png"),
        ]
        return sprites

    def parse_border_sprites(self):
        """
        Returns a dictionary of all the individual sprites from the borders spritesheet.
        """
        sheet = Spritesheet("Sprites/border_sheet.png")
        borders = {
            "top_left": sheet.parse_sprite("top_left.png"),
            "top_right": sheet.parse_sprite("top_right.png"),
            "bottom_left": sheet.parse_sprite("bottom_left.png"),
            "bottom_right": sheet.parse_sprite("bottom_right.png"),
            "right_t": sheet.parse_sprite("right_t.png"),
            "left_t": sheet.parse_sprite("left_t.png"),
            "horizontal_bar": sheet.parse_sprite("horizontal_bar.png"),
            "vertical_bar": sheet.parse_sprite("vertical_bar.png"),
        }
        return borders

    def parse_face_sprites(self):
        """
        Returns a dictionary of all the individual sprites from the faces spritesheet.
        """
        sheet = Spritesheet("Sprites/faces_sheet.png")
        faces = {
            "smile": sheet.parse_sprite("face_smile.png"),
            "dead": sheet.parse_sprite("face_dead.png"),
            "supprise": sheet.parse_sprite("face_supprise.png"),
            "win": sheet.parse_sprite("face_win.png"),
            "pressed": sheet.parse_sprite("face_pressed.png"),
        }
        return faces

    def parse_button_sprites(self):
        """
        Returns a dictionary of all the individual sprites from the button spritesheet.
        """
        sheet = Spritesheet("Sprites/button_sheet.png")
        buttons = {
            "button": sheet.parse_sprite("button.png"),
            "button_pressed": sheet.parse_sprite("button_pressed.png"),
        }
        return buttons
