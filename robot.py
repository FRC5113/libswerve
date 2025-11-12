from lemonlib import LemonRobot
from lemonlib import LemonInput
from components.drivetrain import LemonSwerve

class MyRobot(LemonRobot):
    drivetrain: LemonSwerve
    joystick: LemonInput
    def createObjects(self):
        self.drivetrain = LemonSwerve()
        self.joystick = LemonInput(0)
    def teleopPeriodic(self):
        vX = self.joystick.getLeftX()
        vY = self.joystick.getLeftY()
        rotations = (self.joystick.getRightX() + 1.0) / 2.0 #not sure I like this
        self.drivetrain.drive(vX, vY, rotations, "field")