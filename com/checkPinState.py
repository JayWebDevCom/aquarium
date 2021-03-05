import RPi.GPIO as GPIO
import click

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

@click.command()
@click.option('--pin', '-p', required=True, type=int, help='Enter a pin number to test state')
def test_pin_state(pin: int):
    print(f'testing pin {pin}')
    GPIO.setup(pin, GPIO.OUT)
    pin_state = GPIO.input(pin)
    if pin_state:
        print('on')
    else:
        print('off')

test_pin_state()
GPIIO.cleanup(pin_state)
