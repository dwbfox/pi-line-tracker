import time
import atexit
from Adafruit_MotorHAT import Adafruit_MotorHAT
import logging

logging.basicConfig(format='[%(levelname)s] %(asctime)s -- %(funcName)s:%(lineno)d: %(msg)s')
logger = logging.getLogger('Steering.py')
logger.setLevel(logging.DEBUG)


class Steering:

    def __init__(self):

        self.dry_run = False

        # Pin outs
        self.LEFT_SENSOR = 18
        self.RIGHT_SENSOR = 13

        # How often our sensor
        # is measured
        self.motor_speeds = 200

        self.cruise_speed = 250

        # Stepper motors setup
        self.mh = Adafruit_MotorHAT()
        self.left_motor = self.mh.getMotor(2);
        self.right_motor = self.mh.getMotor(1);
        self.left_motor.setSpeed(self.motor_speeds)
        self.right_motor.setSpeed(self.motor_speeds)


    def setSpeedCruiseMode(self):
        self.left_motor.setSpeed(self.cruise_speed)
        self.right_motor.setSpeed(self.cruise_speed)


    def setSpeedTurnMode(self):
        self.left_motor.setSpeed(self.motor_speeds)
        self.right_motor.setSpeed(self.motor_speeds)


    def stopMotors(self, motors=[]):
        if self.dry_run:
            return 
        '''Stops all or specified motors'''
        if len(motors) <= 0:
            self.left_motor.run(Adafruit_MotorHAT.RELEASE)
            self.right_motor.run(Adafruit_MotorHAT.RELEASE)
        else:
            for motor in motors:
                motor.run(Adafruit_MotorHAT.RELEASE)


    def moveForward(self, motors=[]):
        logging.info('Motor moving backwards')
        if self.dry_run:
            return 
        '''Moves all or specified motors forwards'''
        if len(motors) <= 0:
            self.setSpeedCruiseMode()
            self.left_motor.run(Adafruit_MotorHAT.FORWARD)
            self.right_motor.run(Adafruit_MotorHAT.FORWARD)
        else:
            self.setSpeedTurnMode()
            for motor in motors:
                motor.run(Adafruit_MotorHAT.FORWARD)



    def moveBackwards(self, motors=[], duration=None):
        if self.dry_run:
            return 
        '''Moves all or specified motors backwards'''
        self.stopMotors(motors)
        if len(motors) <= 0:
            self.setSpeedTurnMode()
            self.left_motor.run(Adafruit_MotorHAT.BACKWARD)
            self.right_motor.run(Adafruit_MotorHAT.BACKWARD)
        else:
            self.setSpeedTurnMode()
            for motor in motors:
                motor.run(Adafruit_MotorHAT.BACKWARD)
        if duration != None:
            time.sleep(duration)


    def turnRight(self, duration=None):
        '''Stop the right motor and run the left'''
        self.stopMotors(motors=[self.right_motor])
        self.moveForward(motors=[self.left_motor])
        if duration != None:
            time.sleep(duration)


    def turnLeft(self, duration=None):
        '''Stop the left motor and run the right'''
        self.stopMotors(motors=[self.left_motor])
        self.moveForward(motors=[self.right_motor])
        if duration != None:
            time.sleep(duration)

    def __del__(self):
        self.stopMotors()
