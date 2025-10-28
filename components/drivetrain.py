from phoenix6.swerve import SwerveDrivetrain
from phoenix6.swerve.requests import FieldCentric, ForwardPerspectiveValue
from phoenix6 import hardware
from constants import LemonSwerveConstants
from wpimath.units import meters_per_second, radians_per_second

class LemonSwerve:
    def __init__(self, constant_path: str):
        self.constants = LemonSwerveConstants(constant_path)
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
    def drive(self, vX: meters_per_second, vY: meters_per_second, rotations: radians_per_second) -> None:
        request = (
            FieldCentric()
            .with_forward_perspective(ForwardPerspectiveValue.OPERATOR_PERSPECTIVE)
            .with_velocity_x(vX * self.max_speed)
            .with_velocity_y(vY * self.max_speed)
            .with_rotational_rate(rotations * self.max_speed)
        )
        self.drivetrain.set_control(request)

s = LemonSwerve("constants.json")
s.drive(1, 1, 0.2)