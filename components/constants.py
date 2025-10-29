from phoenix6.swerve import (
    SwerveDrivetrainConstants,
    SwerveModuleConstantsFactory,
    ClosedLoopOutputType,
    SteerFeedbackType,
    SwerveModuleConstants,
    DriveMotorArrangement
)
from phoenix6.configs import TalonFXConfiguration, CurrentLimitsConfigs
from wpimath.geometry import Translation2d
from wpimath.units import amperes, kilogram_square_meters, volts,inchesToMeters
import json
import os
class LemonSwerveConstants:
    def _init_constants(self, module_number: int, module_key: str) -> SwerveModuleConstants:
        mod = self.constants["Modules"][module_number]
        opts = self.constants["SwerveOptions"]
        steer_config = TalonFXConfiguration().with_current_limits(
            CurrentLimitsConfigs().with_stator_current_limit(amperes(120)).with_stator_current_limit_enable(True)
        )
        factory = (
            SwerveModuleConstantsFactory()
            .with_drive_motor_gear_ratio(opts["SwerveModuleConfiguration"]["DriveRatio"])
            .with_steer_motor_gear_ratio(opts["SwerveModuleConfiguration"]["SteerRatio"])
            .with_wheel_radius(inchesToMeters(opts["WheelRadiusInches"]))  # inches to meters
            .with_coupling_gear_ratio(opts["SwerveModuleConfiguration"]["CouplingRatio"])
            .with_steer_motor_closed_loop_output(ClosedLoopOutputType.VOLTAGE)
            .with_drive_motor_closed_loop_output(ClosedLoopOutputType.VOLTAGE)
            .with_slip_current(amperes(mod["DriveMotor"]["SelectedMotorType"]["SlipCurrentLimit"]))
            .with_speed_at12_volts(opts["kSpeedAt12Volts"])
            .with_drive_motor_type(DriveMotorArrangement.TALON_FX_INTEGRATED) #default for 5113
            .with_steer_motor_type(DriveMotorArrangement.TALON_FX_INTEGRATED)
            .with_feedback_source(SteerFeedbackType.REMOTE_CANCODER)
            .with_steer_inertia(kilogram_square_meters(0.01))
            .with_drive_inertia(kilogram_square_meters(0.01))
            .with_steer_friction_voltage(volts(0.0))
            .with_drive_friction_voltage(volts(0.0))
            .with_drive_motor_initial_configs(TalonFXConfiguration()) 
            .with_steer_motor_initial_configs(steer_config)
        )

        return factory.create_module_constants(
            steer_motor_id=mod["SteerMotor"]["Id"],
            drive_motor_id=mod["DriveMotor"]["Id"],
            encoder_id=mod["Encoder"]["Id"],
            encoder_offset=mod["EncoderOffset"],
            drive_motor_inverted=opts["IsRightSideInverted"] if "Right" in mod["ModuleName"] else opts["IsLeftSideInverted"],
            steer_motor_inverted=mod["IsSteerInverted"],
            encoder_inverted=mod["IsEncoderInverted"],
            location_x=self.MODULE_POSITIONS[module_key].X(),
            location_y=self.MODULE_POSITIONS[module_key].Y(),
        )

    def __init__(self, path: str):
        try:
            with open(path, "r") as f:
                self.constants = json.load(f)
        except:
            print(f"Failed to open path, running from {os.getcwd()}")
            raise
        opts = self.constants["SwerveOptions"]

        self.DRIVETRAIN = (
            SwerveDrivetrainConstants()
            .with_pigeon2_id(opts["Gyro"]["Id"])
            .with_can_bus_name(self.constants["Modules"][0]["Encoder"]["CANbus"])
        )

        offset = 0.381  # 15 inches
        self.MODULE_POSITIONS = {
            "fr": Translation2d(offset, offset),
            "fl": Translation2d(-offset, offset),
            "br": Translation2d(offset, -offset),
            "bl": Translation2d(-offset, -offset),
        }

        self.FL = self._init_constants(0, "fl")
        self.FR = self._init_constants(1, "fr")
        self.BL = self._init_constants(2, "bl")
        self.BR = self._init_constants(3, "br")
