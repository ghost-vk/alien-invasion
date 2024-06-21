class Settings():
    """Класс для хранения настроек игры Alien Invasion"""

    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        
        self.ship_limit = 3

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 20, 20, 20
        self.bullets_allowed = 3
        self.bullets_disappear_on_collision = True

        self.fleet_drop_speed = 3 

        self.speedup_scale = 1.15
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 10
        self.alien_speed_factor = 3 
        self.bullet_speed_factor = 10 

        # fleet_direction - направление флота (1 - вправо, -1 - влево)
        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

