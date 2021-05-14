import utime, ds18x20, onewire, network
from machine import Signal, Pin

##  disable the built-in MicroPython AP
##  comment this out if you intend to use this software to send data over the Wi-Fi radio
ap = network.WLAN(network.AP_IF)
ap.active(False)
print("\nLocal Access Point has been disabled.")


print("\nBeginning temperature monitoring.")
def main():
    while True:
        gc.collect()
        utime.sleep_ms(2000)  # give board 2 seconds to boot before dicking around with GPIO0
        pin5 = Pin(5, Pin.OUT)  # define pin #5 as output
        fan = Signal(pin5, invert=False)  # invert the output so on = on and off = off. Call it "fan".
        pin13 = Pin(13, Pin.OUT)  # define pin #4 as output
        blue = Signal(pin13, invert=False)  # call and set invert for BLUE LED3..
        pin14 = Pin(14, Pin.OUT) # define pin #14 as an output
        red = Signal(pin14, invert=False)  # option to invert RED LED.
        pin0 = Pin(0, Pin.OUT)
        green = Signal(pin0, invert=False)
        ow12 = onewire.OneWire(Pin(12)) # create a OneWire bus on GPIO12
        sensor = ds18x20.DS18X20(ow12)  # make GPIO12 a dsx1820B sensor, call it 'sensor'.
        scans = sensor.scan()  # scans the OneWire Bus
        sensor.convert_temp()  # converts the OneWire bus data to temperature
        utime.sleep_ms(750)
        for scan in scans:
            sensor.read_temp(scan)
            temperature = sensor.read_temp(scan)
        if temperature > float(30):
            print('Temperature is ' + str(temperature) + '. Cooling.')
            fan.on()
            blue.on()
            green.off()
            red.on()
            utime.sleep_ms(2000)
        elif temperature < float(30):
            if pin5() == 0:
                print('Temperature is ' + str(temperature) + '. Fan idle.')
                green.on()
                red.off()
                blue.off()
                utime.sleep_ms(2000)
            elif pin5() == 1:
                print('Temperature is ' + str(temperature) + '. Spinning down.')
                red.off()
                green.off()
                blue.on()
                utime.sleep_ms(300000)
                fan.off()
                blue.off()
                green.on
            
if __name__ == '__main__':
    main()