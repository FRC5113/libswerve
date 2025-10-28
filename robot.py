from lemonlib import LemonRobot
from lemonlib import LemonInput
from components.drivetrain import LemonSwerve
class Main(LemonRobot):
    drivetrain: LemonSwerve
    joystick: LemonInput
    def __init__(self):
        self.drivetrain = LemonSwerve("constants.json")
        self.joystic = LemonInput(0)
    def teleopPeriodic(self):
        vX = self.joystick.getLeftX()
        vY = self.joystic.getLeftY()
        self.drivetrain.drive(vX, vY, 0, "field")