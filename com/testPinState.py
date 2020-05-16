import RPi.GPIO as GPIO
import click

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

@click.command()
@click.option('--state', '-s', required=True, type=int, help='Enter a pin number to test state')
def test_pin_state(state: int):
    print(f'testing pin {state}')
    GPIO.setup(state, GPIO.OUT)
    pin_state = GPIO.input(state)
    if pin_state:
        print('on')
    else:
        print('off')

test_pin_state()
GPIIO.cleanup(state)
