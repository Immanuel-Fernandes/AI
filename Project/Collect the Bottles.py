import time
from pystage.en import Sprite, Stage 

stage = Stage()
stage.add_backdrop('Background')
stage.create_variable('Bottle Collected')
stage.create_variable('Bottle Fallen')
stage.show_variable("Bottle Collected")
stage.set_monitor_position("Bottle Collected", -220, -150)
stage.show_variable("Bottle Fallen")
stage.set_monitor_position("Bottle Fallen", 100, -150)

# Create and initialize sprite 'bin'
bin_sprite = stage.add_a_sprite(None)
bin_sprite.set_name("Bin")
bin_sprite.set_x(122)
bin_sprite.set_y(-91.35)
bin_sprite.go_to_back_layer()
bin_sprite.go_forward(3)
bin_sprite.set_size_to(50)
bin_sprite.add_costume('bin', center_x=30, center_y=15)  

# Create and initialize sprite 'bottle'
bottle = stage.add_a_sprite(None)
bottle.set_name("Bottle")
bottle.set_x(-133)
bottle.set_y(172)
bottle.go_to_back_layer()
bottle.go_forward(2)
bottle.set_size_to(80)
bottle.add_costume('bottle', center_x=31, center_y=31)  
bottle.add_sound('chomp')
bottle.add_sound('collect')

# Scratch Blocks for 'bin'
def when_program_starts_1(self):
    while True:
        # Hill-Climbing logic
        current_distance = abs(self.x_position() - bottle.x_position())
        neighbor_left_distance = abs((self.x_position() - 10) - bottle.x_position())
        neighbor_right_distance = abs((self.x_position() + 10) - bottle.x_position())

        if neighbor_left_distance < current_distance:
            self.change_x_by(-10.0)  # Move left if it reduces the distance
        elif neighbor_right_distance < current_distance:
            self.change_x_by(10.0)  # Move right if it reduces the distance
        
        time.sleep(0.01)  

bin_sprite.when_program_starts(when_program_starts_1)

# Scratch Blocks for 'bottle'
def when_program_starts_2(self):
    self.set_variable("Bottle Collected", 0)
    self.set_variable("Bottle Fallen", 0)
    while True:
        self.change_y_by(-8.0)
        if (self.y_position() < -170):
            self.go_to_random_position()
            self.set_y(180.0)

        if (self.get_variable("Bottle Fallen") == 10):
            self.say_for_seconds("You Lost", 2.0)
            self.stop_all()

        if (self.get_variable("Bottle Collected") == 25):
            self.say_for_seconds("You Win", 2.0)
            self.stop_all()

        if self.touching(bin_sprite) and self.y_position() == -52.0:
            self.change_variable_by("Bottle Collected", 1.0)
            self.play_sound_until_done("collect")
            self.go_to_random_position()
            self.set_y(180.0)
        else:
            if (self.y_position() < -160):
                self.change_variable_by("Bottle Fallen", 1.0)
                self.play_sound_until_done("chomp")
                self.go_to_random_position()
                self.set_y(180.0)
        
        time.sleep(0.01)          

bottle.when_program_starts(when_program_starts_2)

stage.play()
