from lemonlib import LemonRobot
from lemonlib import LemonInput
from components.drivetrain import LemonSwerve
class MyRobot(LemonRobot):
    drivetrain: LemonSwerve
    joystick: LemonInput
    def createObjects(self):
        self.drivetrain = LemonSwerve("constants.json")
        self.joystick = LemonInput(0)
    def teleopPeriodic(self):
        vX = self.joystick.getLeftX()
        vY = self.joystick.getLeftY()
        rotations = self.joystick.getRightX() #not sure I like this
        self.drivetrain.drive(vX, vY, rotations, "field")