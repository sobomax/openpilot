#!/usr/bin/env python3
from cereal import car
from common.op_params import opParams
from selfdrive.config import Conversions as CV
from selfdrive.car.hyundai.values import CAR
from selfdrive.car import STD_CARGO_KG, scale_rot_inertia, scale_tire_stiffness, gen_empty_fingerprint
from selfdrive.car.interfaces import CarInterfaceBase

class CarInterface(CarInterfaceBase):

  @staticmethod
  def compute_gb(accel, speed):
    return float(accel) / 1.0

  @staticmethod
  def get_params(candidate, fingerprint=gen_empty_fingerprint(), car_fw=[]):  # pylint: disable=dangerous-default-value
    ret = CarInterfaceBase.get_std_params(candidate, fingerprint)

    ret.carName = "hyundai"
    ret.safetyModel = car.CarParams.SafetyModel.hyundai
    ret.radarOffCan = True

    # Most Hyundai car ports are community features for now
    ret.communityFeature = candidate not in [CAR.SONATA, CAR.PALISADE]

    ret.steerActuatorDelay = 0.3  # Default delay
    ret.steerRateCost = 0.5
    ret.steerLimitTimer = 0.1
    tire_stiffness_factor = 0.7

    if not opParams().get('Enable_INDI'):
      ret.lateralTuning.init('pidnl')
      ret.lateralTuning.pidnl.kpBP = [0., 10., 30.]
      ret.lateralTuning.pidnl.kpV = [0.01, 0.02, 0.03]
      ret.lateralTuning.pidnl.kiBP = [0., 10., 30.]
      ret.lateralTuning.pidnl.kiV = [0.001, 0.0015, 0.002]
      ret.lateralTuning.pidnl.kfBP = [0., 10., 30.]
      ret.lateralTuning.pidnl.kfV = [0.000015, 0.00002, 0.000025]
    else:
      ret.lateralTuning.init('indi')
      ret.lateralTuning.indi.outerLoopGain = 3.  # stock is 2.0.  Trying out 2.5
      ret.lateralTuning.indi.innerLoopGain = 2.
      ret.lateralTuning.indi.timeConstant = 1.4
      ret.lateralTuning.indi.actuatorEffectiveness = 2.

    if candidate == CAR.SANTA_FE:
      ret.mass = 3982. * CV.LB_TO_KG + STD_CARGO_KG
      ret.wheelbase = 2.766
      # Values from optimizer
      ret.steerRatio = 16.55  # 13.8 is spec end-to-end
    elif candidate == CAR.SONATA:
      ret.mass = 1513. + STD_CARGO_KG
      ret.wheelbase = 2.84
      ret.steerRatio = 13.27 * 1.15   # 15% higher at the center seems reasonable
    elif candidate == CAR.SONATA_2019:
      ret.mass = 4497. * CV.LB_TO_KG
      ret.wheelbase = 2.804
      ret.steerRatio = 13.27 * 1.15   # 15% higher at the center seems reasonable
    elif candidate == CAR.PALISADE:
      ret.mass = 1999. + STD_CARGO_KG
      ret.wheelbase = 2.90
      ret.steerRatio = 13.75 * 1.15
    elif candidate in [CAR.ELANTRA, CAR.ELANTRA_GT_I30]:
      ret.mass = 1275. + STD_CARGO_KG
      ret.wheelbase = 2.7
      ret.steerRatio = 15.4            # 14 is Stock | Settled Params Learner values are steerRatio: 15.401566348670535
      ret.minSteerSpeed = 32 * CV.MPH_TO_MS
    elif candidate == CAR.HYUNDAI_GENESIS:
      ret.mass = 2060. + STD_CARGO_KG
      ret.wheelbase = 3.01
      ret.steerRatio = 16.5
      ret.lateralTuning.init('indi')
      ret.lateralTuning.indi.innerLoopGain = 3.5
      ret.lateralTuning.indi.outerLoopGain = 2.0
      ret.lateralTuning.indi.timeConstant = 1.4
      ret.lateralTuning.indi.actuatorEffectiveness = 2.3
      ret.minSteerSpeed = 60 * CV.KPH_TO_MS
    elif candidate == CAR.KONA:
      ret.mass = 1275. + STD_CARGO_KG
      ret.wheelbase = 2.7
      ret.steerRatio = 13.73 * 1.15  # Spec
    elif candidate == CAR.KONA_EV:
      ret.mass = 1685. + STD_CARGO_KG
      ret.wheelbase = 2.7
      ret.steerRatio = 13.73  # Spec
    elif candidate in [CAR.IONIQ, CAR.IONIQ_EV_LTD]:
      ret.mass = 1490. + STD_CARGO_KG   #weight per hyundai site https://www.hyundaiusa.com/ioniq-electric/specifications.aspx
      ret.wheelbase = 2.7
      ret.steerRatio = 13.73   #Spec
      ret.minSteerSpeed = 32 * CV.MPH_TO_MS
    elif candidate == CAR.VELOSTER:
      ret.steerActuatorDelay = 0.1  # Default delay
      ret.steerRateCost = 0.5
      ret.steerLimitTimer = 0.4
      ret.mass = 3558. * CV.LB_TO_KG # actual: 2987
      ret.wheelbase = 2.80 # actual: 2.649
      ret.steerRatio = 13.75 * 1.15
      ret.lateralTuning.pidnl.kpBP = [0., 10., 30.]
      ret.lateralTuning.pidnl.kpV = [0.25, 0.25, 0.25]
      ret.lateralTuning.pidnl.kiBP = [0., 10., 30.]
      ret.lateralTuning.pidnl.kiV = [0.05, 0.05, 0.05]
      ret.lateralTuning.pidnl.kfBP = [0., 10., 30.]
      ret.lateralTuning.pidnl.kfV = [0.00005, 0.00005, 0.00005]

    # Kia
    elif candidate == CAR.KIA_SORENTO:
      ret.mass = 1985. + STD_CARGO_KG
      ret.wheelbase = 2.78
      ret.steerRatio = 14.4 * 1.1   # 10% higher at the center seems reasonable
    elif candidate == CAR.KIA_NIRO_EV:
      ret.mass = 1737. + STD_CARGO_KG
      ret.wheelbase = 2.7
      ret.steerRatio = 13.73  # Spec
    elif candidate in [CAR.KIA_OPTIMA, CAR.KIA_OPTIMA_H]:
      ret.mass = 3558. * CV.LB_TO_KG
      ret.wheelbase = 2.80
      ret.steerRatio = 13.75
    elif candidate == CAR.KIA_STINGER:
      ret.mass = 1825. + STD_CARGO_KG
      ret.wheelbase = 2.78
      ret.steerRatio = 14.4 * 1.15   # 15% higher at the center seems reasonable

    elif candidate == CAR.KIA_FORTE:
      ret.mass = 3558. * CV.LB_TO_KG
      ret.wheelbase = 2.80
      ret.steerRatio = 13.75

    # Genesis
    elif candidate == CAR.GENESIS_G70:
      ret.lateralTuning.init('indi')
      ret.lateralTuning.indi.innerLoopGain = 2.5
      ret.lateralTuning.indi.outerLoopGain = 3.5
      ret.lateralTuning.indi.timeConstant = 1.4
      ret.lateralTuning.indi.actuatorEffectiveness = 1.8
      ret.steerActuatorDelay = 0.1
      ret.mass = 1640.0 + STD_CARGO_KG
      ret.wheelbase = 2.84
      ret.steerRatio = 13.56
    elif candidate == CAR.GENESIS_G80:
      ret.mass = 2060. + STD_CARGO_KG
      ret.wheelbase = 3.01
      ret.steerRatio = 16.5
    elif candidate == CAR.GENESIS_G90:
      ret.mass = 2200
      ret.wheelbase = 3.15
      ret.steerRatio = 12.069

    # these cars require a special panda safety mode due to missing counters and checksums in the messages
    if candidate in [CAR.HYUNDAI_GENESIS, CAR.IONIQ_EV_LTD, CAR.IONIQ, CAR.KONA_EV, CAR.KIA_SORENTO, CAR.SONATA_2019,
                     CAR.KIA_NIRO_EV, CAR.KIA_OPTIMA, CAR.VELOSTER, CAR.KIA_STINGER, CAR.GENESIS_G70, CAR.GENESIS_G80]:
      ret.safetyModel = car.CarParams.SafetyModel.hyundaiLegacy

    ret.centerToFront = ret.wheelbase * 0.4

    # TODO: get actual value, for now starting with reasonable value for
    # civic and scaling by mass and wheelbase
    ret.rotationalInertia = scale_rot_inertia(ret.mass, ret.wheelbase)

    # TODO: start from empirically derived lateral slip stiffness for the civic and scale by
    # mass and CG position, so all cars will have approximately similar dyn behaviors
    ret.tireStiffnessFront, ret.tireStiffnessRear = scale_tire_stiffness(ret.mass, ret.wheelbase, ret.centerToFront,
                                                                         tire_stiffness_factor=tire_stiffness_factor)

    ret.enableCamera = True

    return ret

  def update(self, c, can_strings):
    self.cp.update_strings(can_strings)
    self.cp_cam.update_strings(can_strings)

    ret = self.CS.update(self.cp, self.cp_cam)
    ret.canValid = self.cp.can_valid and self.cp_cam.can_valid

    # speeds
    ret.steeringRateLimited = self.CC.steer_rate_limited if self.CC is not None else False

    events = self.create_common_events(ret)
    #TODO: addd abs(self.CS.angle_steers) > 90 to 'steerTempUnavailable' event

    # low speed steer alert hysteresis logic (only for cars with steer cut off above 10 m/s)
    if ret.vEgo < (self.CP.minSteerSpeed + 2.) and self.CP.minSteerSpeed > 10.:
      self.low_speed_alert = True
    if ret.vEgo > (self.CP.minSteerSpeed + 4.):
      self.low_speed_alert = False
    if self.low_speed_alert:
      events.add(car.CarEvent.EventName.belowSteerSpeed)

    ret.events = events.to_msg()

    self.CS.out = ret.as_reader()
    return self.CS.out

  def apply(self, c):
    can_sends = self.CC.update(c.enabled, self.CS, self.frame, c.actuators,
                               c.cruiseControl.cancel, c.hudControl.visualAlert, c.hudControl.leftLaneVisible,
                               c.hudControl.rightLaneVisible, c.hudControl.leftLaneDepart, c.hudControl.rightLaneDepart)
    self.frame += 1
    return can_sends
