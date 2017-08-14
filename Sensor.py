import RPi.GPIO as GPIO
import Steering
import time
import sys
import logging


logging.basicConfig(format='[%(levelname)s] %(asctime)s -- %(funcName)s:%(lineno)d: %(msg)s')
logger = logging.getLogger('sensor.py')
logger.setLevel(logging.DEBUG)



def self_test():
    try:
        steering = Steering.Steering()
        logger.debug('<<<<<< SELF TEST >>>')
        logger.debug('Checking pin and motor configs are good...')
        assert steering.LEFT_SENSOR is not None
        assert steering.RIGHT_SENSOR is not None
        assert 0 < steering.motor_speeds <= 250
        assert 0 < steering.cruise_speed <= 250

        steering.dry_run = False

        logger.debug('Turning left')
        steering.turnLeft()
        time.sleep(.05)
        logger.debug('Turning right...')
        steering.turnRight()
        time.sleep(.05)

        logger.debug('Backing up...')
        steering.moveBackwards()
        time.sleep(.05)

        logger.debug('<<<<<<<<< SELF TEST COMPLETE >>>>>>>>>>')
    except Exception as e:
        logger.debug('Error: {}'.format(e.message))
        del steering
        sys.exit(1)

def init_follow_track_mode():

    steering = Steering.Steering()
    steering.dry_run = False

    # IR Sensor Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(steering.LEFT_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(steering.RIGHT_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    lastDir = None
    offTrackCount = 0
    while True:
        try:
            left_active = GPIO.input(steering.LEFT_SENSOR) == 0
            right_active =  GPIO.input(steering.RIGHT_SENSOR) == 0

            # this is indicative of the fact that we're off track
            if left_active and right_active:
                # gone too far, back up for 900 milliseconds
                if offTrackCount > 15:
                    steering.moveBackwards(duration=.4)
                    offTrackCount = 0
                logger.debug('Off Track, turning towards last suggested direction ({})'.format(lastDir))
                offTrackCount += 1
                if lastDir == 'left':
                    steering.turnLeft()
                elif lastDir == 'right':
                    steering.turnRight()
                else:
                    steering.moveForward()
                continue

            elif left_active:
                offTrackCount = 0
                logger.info('Track is curving right, turning right')
                steering.turnRight(duration=None)
                lastDir = 'right'
                continue

            # Track is curving right
            elif right_active:
                offTrackCount = 0
                logger.info('Tracking curving left, turning left')
                steering.turnLeft(duration=None)
                lastDir = 'left'
                continue
            # Track is straight
            else:
                logger.info('Track is straight, moving straight')
                steering.moveForward()

        except Exception as e:
            logger.warning('Error: {}'.format(e.message))
            GPIO.cleanup()
            steering.stopMotors()
            return


if __name__ == '__main__':
    steering = Steering.Steering()
    self_test()
    init_follow_track_mode()

