import RPIO
from RPIO import PWM


RPIO.cleanup()

A_DCM1 = 7
A_DCM2 = 8
B_DCM1 = 9
B_DCM2 = 11

MAX_SPEED = 16500

# Init PWM channels
pwm_controller = PWM.Servo()

# Set GPIOs as outputs
RPIO.setup(A_DCM1, RPIO.OUT)
RPIO.setup(A_DCM2, RPIO.OUT)
RPIO.setup(B_DCM1, RPIO.OUT)
RPIO.setup(B_DCM2, RPIO.OUT)


def stop():
    PWM.clear_channel(pwm_controller._dma_channel)


def forward():
    pwm_controller.set_servo(A_DCM1, MAX_SPEED)
    RPIO.output(A_DCM2, False)

    pwm_controller.set_servo(B_DCM1, MAX_SPEED)
    RPIO.output(B_DCM2, False)


def backward():
    pwm_controller.set_servo(A_DCM2, MAX_SPEED)
    RPIO.output(A_DCM1, False)

    pwm_controller.set_servo(B_DCM2, MAX_SPEED)
    RPIO.output(B_DCM1, False)


def left():
    RPIO.output(A_DCM1, False)
    pwm_controller.set_servo(A_DCM2, MAX_SPEED)

    pwm_controller.set_servo(B_DCM1, MAX_SPEED)
    RPIO.output(B_DCM2, False)


def right():
    pwm_controller.set_servo(A_DCM1, MAX_SPEED)
    RPIO.output(A_DCM2, False)

    RPIO.output(B_DCM1, False)
    pwm_controller.set_servo(B_DCM2, MAX_SPEED)