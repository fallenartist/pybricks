# Simple tank drive functionality
# using Xbox controller
# with two motors driving left and right track
# and buttons for speed control

from pybricks.hubs import TechnicHub
from pybricks.iodevices import XboxController
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait, StopWatch

# Initialize the hub
hub = TechnicHub()

# Initialize motors for the left and right tracks (swapped)
left_motor = Motor(Port.B, Direction.CLOCKWISE)
right_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)

# Initialize the Xbox controller
controller = XboxController()

# Initialize variables for speed mode
speed_mode = 1  # Default speed mode

# Initialize a stopwatch to track inactivity
inactivity_timer = StopWatch()

# Main loop
while True:
    # Get the x and y positions of the left joystick (values range from -100 to 100)
    x, y = controller.joystick_left()

    # Invert y to correct forward/backward direction
    y = -y

    # Get the pressed buttons
    pressed_buttons = controller.buttons.pressed()

    # Implement dead zone to prevent drift
    dead_zone = 10
    if abs(x) < dead_zone:
        x = 0
    if abs(y) < dead_zone:
        y = 0

    # Update speed mode based on button presses
    if Button.A in pressed_buttons:
        speed_mode = 0.5  # Slow speed
    elif Button.B in pressed_buttons:
        speed_mode = 1    # Normal speed
    elif Button.Y in pressed_buttons:
        speed_mode = 1.5  # Fast speed

    # Calculate motor speeds for tank drive (swapped left and right)
    left_speed = (y - x) * speed_mode
    right_speed = (y + x) * speed_mode

    # Limit the speeds to the range -100 to 100
    left_speed = max(min(left_speed, 100), -100)
    right_speed = max(min(right_speed, 100), -100)

    # Set the motor speeds
    left_motor.dc(left_speed)
    right_motor.dc(right_speed)

    # Check for inactivity
    if x != 0 or y != 0 or pressed_buttons:
        # Reset inactivity timer
        inactivity_timer.reset()
    else:
        # Check if inactivity time exceeds 2 minutes (120,000 milliseconds)
        if inactivity_timer.time() > 120000:
            # Stop the motors
            left_motor.stop()
            right_motor.stop()
            # Shutdown the hub
            hub.system.shutdown()

    # Small delay to prevent overloading the hub's processor
    wait(50)
