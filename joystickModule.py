import spidev
from RPLCD.i2c import CharLCD
import time

swt_channel = 0
vrx_channel = 1
vry_channel = 2

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=20, rows=4, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)

def readChannel(channel):
    val = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((val[1] & 3) << 8) + val[2]
    return data

while True:
    vrx_pos = readChannel(vrx_channel)
    vry_pos = readChannel(vry_channel)
    swt_val = readChannel(swt_channel)

    if vrx_pos <= 500 and vry_pos <= 10:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("X-axis: {}".format(vrx_pos))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Y-axis: {}".format(vry_pos))
        lcd.cursor_pos = (3, 0)
        lcd.write_string("Current Axis: Right")
    elif vrx_pos <= 500 and vry_pos >= 1020:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("X-axis: {}".format(vrx_pos))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Y-axis: {}".format(vry_pos))
        lcd.cursor_pos = (3, 0)
        lcd.write_string("Current Axis: Left")
    elif vrx_pos <= 10 and vry_pos >= 500:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("X-axis: {}".format(vrx_pos))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Y-axis: {}".format(vry_pos))
        lcd.cursor_pos = (3, 0)
        lcd.write_string("Current Axis: Up")
    elif vrx_pos >= 1020 and vry_pos >= 500:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("X-axis: {}".format(vrx_pos))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Y-axis: {}".format(vry_pos))
        lcd.cursor_pos = (3, 0)
        lcd.write_string("Current Axis: Down")
    else:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("X-axis: {}".format(vrx_pos))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Y-axis: {}".format(vry_pos))
        lcd.cursor_pos = (3, 0)
        lcd.write_string("Current Axis:")

    time.sleep(0.5)