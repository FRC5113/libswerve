from phoenix6.swerve import SwerveDrivetrain
from phoenix6.swerve.requests import FieldCentric, ForwardPerspectiveValue, RobotCentric
from phoenix6 import hardware
from .constants import LemonSwerveConstants
from wpimath.units import meters_per_second, radians_per_second
from typing import Literal
from lemonlib.smart import SmartPreference,SmartProfile
class LemonSwerve:
    def temp():
        pass
    def setup(self):
        self.constants = LemonSwerveConstants()
        self.foo = SmartPreference(4)
        self.drivetrain = SwerveDrivetrain(
            hardware.TalonFX,
            hardware.TalonFX,
            hardware.CANcoder,
            self.constants.DRIVETRAIN,
            [
                self.constants.FL,
                self.constants.FR,
                self.constants.BL,
                self.constants.BR,
            ],
        )
        self.max_speed = meters_per_second(2) #This is a placeholder value
        self.drivetrain_state = self.drivetrain.SwerveDriveState()

    def on_enable(self):
        self.steer_controller = self.constants.steer_profile.create_ctre_turret_controller()
        self.drive_controler = self.constants.drive_profile.create_ctre_turret_controller()        

    def drive_field_centric(self, vX: meters_per_second, vY: meters_per_second, rotations: radians_per_second) -> None:
        request = (
            FieldCentric()
            .with_forward_perspective(ForwardPerspectiveValue.OPERATOR_PERSPECTIVE)
            .with_velocity_x(vX * self.max_speed)
            .with_velocity_y(vY * self.max_speed)
            .with_rotational_rate(rotations * self.max_speed)
        )
        self.drivetrain.set_control(request)
    def drive_robot_centric(self, vX: meters_per_second, vY: meters_per_second, rotations: radians_per_second) -> None:
        request = (
            RobotCentric()
            .with_velocity_x(vX * self.max_speed)
            .with_velocity_y(vY * self.max_speed)
            .with_rotational_rate(rotations * self.max_speed)
        )
        self.drivetrain.set_control(request)
    def drive(self, vX: meters_per_second, vY: meters_per_second, rotations: radians_per_second, drive_mode: Literal["field", "robot"]):
        if drive_mode == "field":
            self.drive_field_centric(vX, vY, rotations)
        else:
            self.drive_robot_centric(vX, vY, rotations)
    def execute(self):
        self.foo
        pass