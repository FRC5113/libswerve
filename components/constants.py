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
from lemonlib.smart import SmartProfile
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
        self.steer_profile = SmartProfile(
            "steer",
            {
                "kP": 3.0,
                "kI": 0.0,
                "kD": 0.0,
                "kS": 0.14,
                "kV": 0.375,
                "kA": 0.0,
            },
            True,
        )
        self.drive_profile = SmartProfile(
            "drive",
            {
                "kP": 0.0,
                "kI": 0.0,
                "kD": 0.0,
                "kS": 0.17,
                "kV": 0.104,
                "kA": 0.01
            },
            True,
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


    def __init__(self):
        self.constants = json.loads(json_file)
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


json_file = """{
  "Version": "1.0.0.0",
  "LastState": 11,
  "Modules": [
    {
      "ModuleName": "Front Left",
      "ModuleId": 0,
      "Encoder": {
        "Id": 23,
        "Name": "Swerve (front left)",
        "Model": "CANCoder",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": null,
        "IsStandaloneFx": false
      },
      "SteerMotor": {
        "Id": 22,
        "Name": "Swerve (front left steer)",
        "Model": "Talon FX",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": {
          "Name": "WCP Kraken x60",
          "FreeSpeedRps": 96.7,
          "SlipCurrentLimit": 120,
          "StatorCurrentLimit": 60
        },
        "IsStandaloneFx": false
      },
      "DriveMotor": {
        "Id": 21,
        "Name": "Swerve (front left drive)",
        "Model": "Talon FX",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": {
          "Name": "WCP Kraken x60",
          "FreeSpeedRps": 96.7,
          "SlipCurrentLimit": 120,
          "StatorCurrentLimit": 60
        },
        "IsStandaloneFx": false
      },
      "IsEncoderInverted": true,
      "IsSteerInverted": false,
      "SelectedEncoderType": "CANcoder",
      "EncoderOffset": 0.15380859375,
      "DriveMotorSelectionState": 1,
      "SteerMotorSelectionState": 1,
      "SteerEncoderSelectionState": 1,
      "IsModuleValidationComplete": true,
      "ValidatedSteerId": 22,
      "ValidatedDriveId": 21,
      "ValidatedEncoderId": 23
    },
    {
      "ModuleName": "Front Right",
      "ModuleId": 1,
      "Encoder": {
        "Id": 33,
        "Name": "Swerve (front right)",
        "Model": "CANCoder",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": null,
        "IsStandaloneFx": false
      },
      "SteerMotor": {
        "Id": 32,
        "Name": "Swerve (front right steer)",
        "Model": "Talon FX",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": {
          "Name": "WCP Kraken x60",
          "FreeSpeedRps": 96.7,
          "SlipCurrentLimit": 120,
          "StatorCurrentLimit": 60
        },
        "IsStandaloneFx": false
      },
      "DriveMotor": {
        "Id": 31,
        "Name": "Swerve (front right drive)",
        "Model": "Talon FX",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": {
          "Name": "WCP Kraken x60",
          "FreeSpeedRps": 96.7,
          "SlipCurrentLimit": 120,
          "StatorCurrentLimit": 60
        },
        "IsStandaloneFx": false
      },
      "IsEncoderInverted": true,
      "IsSteerInverted": false,
      "SelectedEncoderType": "CANcoder",
      "EncoderOffset": -0.250244140625,
      "DriveMotorSelectionState": 1,
      "SteerMotorSelectionState": 1,
      "SteerEncoderSelectionState": 1,
      "IsModuleValidationComplete": true,
      "ValidatedSteerId": 32,
      "ValidatedDriveId": 31,
      "ValidatedEncoderId": 33
    },
    {
      "ModuleName": "Back Left",
      "ModuleId": 2,
      "Encoder": {
        "Id": 13,
        "Name": "Swerve (back left)",
        "Model": "CANCoder",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": null,
        "IsStandaloneFx": false
      },
      "SteerMotor": {
        "Id": 12,
        "Name": "Swerve (back left steer)",
        "Model": "Talon FX",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": {
          "Name": "WCP Kraken x60",
          "FreeSpeedRps": 96.7,
          "SlipCurrentLimit": 120,
          "StatorCurrentLimit": 60
        },
        "IsStandaloneFx": false
      },
      "DriveMotor": {
        "Id": 11,
        "Name": "Swerve (back left drive)",
        "Model": "Talon FX",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": {
          "Name": "WCP Kraken x60",
          "FreeSpeedRps": 96.7,
          "SlipCurrentLimit": 120,
          "StatorCurrentLimit": 60
        },
        "IsStandaloneFx": false
      },
      "IsEncoderInverted": true,
      "IsSteerInverted": false,
      "SelectedEncoderType": "CANcoder",
      "EncoderOffset": -0.314208984375,
      "DriveMotorSelectionState": 1,
      "SteerMotorSelectionState": 1,
      "SteerEncoderSelectionState": 1,
      "IsModuleValidationComplete": true,
      "ValidatedSteerId": 12,
      "ValidatedDriveId": 11,
      "ValidatedEncoderId": 13
    },
    {
      "ModuleName": "Back Right",
      "ModuleId": 3,
      "Encoder": {
        "Id": 43,
        "Name": "Swerve (back right)",
        "Model": "CANCoder",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": null,
        "IsStandaloneFx": false
      },
      "SteerMotor": {
        "Id": 42,
        "Name": "Swerve (back right steer)",
        "Model": "Talon FX",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": {
          "Name": "WCP Kraken x60",
          "FreeSpeedRps": 96.7,
          "SlipCurrentLimit": 120,
          "StatorCurrentLimit": 60
        },
        "IsStandaloneFx": false
      },
      "DriveMotor": {
        "Id": 41,
        "Name": "Swerve (back right drive)",
        "Model": "Talon FX",
        "CANbus": "can0",
        "CANbusFriendly": "",
        "SelectedMotorType": {
          "Name": "WCP Kraken x60",
          "FreeSpeedRps": 96.7,
          "SlipCurrentLimit": 120,
          "StatorCurrentLimit": 60
        },
        "IsStandaloneFx": false
      },
      "IsEncoderInverted": true,
      "IsSteerInverted": false,
      "SelectedEncoderType": "CANcoder",
      "EncoderOffset": -0.33642578125,
      "DriveMotorSelectionState": 1,
      "SteerMotorSelectionState": 1,
      "SteerEncoderSelectionState": 1,
      "IsModuleValidationComplete": true,
      "ValidatedSteerId": 42,
      "ValidatedDriveId": 41,
      "ValidatedEncoderId": 43
    }
  ],
  "SwerveOptions": {
    "kSpeedAt12Volts": 4.731460295787658,
    "Gyro": {
      "Id": 30,
      "Name": "Pigeon 2 vers. S (Device ID 30)",
      "Model": "Pigeon 2 vers. S",
      "CANbus": "can0",
      "CANbusFriendly": "",
      "SelectedMotorType": null,
      "IsStandaloneFx": false
    },
    "IsValidGyroCANbus": true,
    "VerticalTrackSizeInches": 25,
    "HorizontalTrackSizeInches": 25,
    "WheelRadiusInches": 2,
    "IsLeftSideInverted": false,
    "IsRightSideInverted": true,
    "SwerveModuleType": 4,
    "SwerveModuleConfiguration": {
      "ModuleBrand": 4,
      "DriveRatio": 6.746031746031747,
      "SteerRatio": 21.428571428571427,
      "CouplingRatio": 3.5714285714285716,
      "CustomName": "L2"
    },
    "HasVerifiedSteer": true,
    "SelectedModuleManufacturer": "Swerve Drive Specialties (SDS)",
    "HasVerifiedDrive": true,
    "IsValidConfiguration": true
  }
}"""