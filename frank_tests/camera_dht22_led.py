import picamera
#import Adafruit_DHT
import RPi.GPIO as GPIO

def getdatetime(timedateformat='complete'):
    from datetime import datetime
    timedateformat = timedateformat.lower()
    if timedateformat == 'day':
        return ((str(datetime.now())).split(' ')[0]).split('-')[2]
    elif timedateformat == 'month':
        return ((str(datetime.now())).split(' ')[0]).split('-')[1]
    elif timedateformat == 'year':
        return ((str(datetime.now())).split(' ')[0]).split('-')[0]
    elif timedateformat == 'hour':
        return (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[0]
    elif timedateformat == 'minute':
        return (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[1]
    elif timedateformat == 'second':
        return (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[2]
    elif timedateformat == 'millisecond':
        return (str(datetime.now())).split('.')[1]
    elif timedateformat == 'yearmonthday':
        return (str(datetime.now())).split(' ')[0]
    elif timedateformat == 'daymonthyear':
        return ((str(datetime.now())).split(' ')[0]).split('-')[2] + '-' + ((str(datetime.now())).split(' ')[0]).split('-')[1] + '-' + ((str(datetime.now())).split(' ')[0]).split('-')[0]
    elif timedateformat == 'hourminutesecond':
        return ((str(datetime.now())).split(' ')[1]).split('.')[0]
    elif timedateformat == 'secondminutehour':
        return (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[2] + ':' + (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[1] + ':' + (((str(datetime.now())).split(' ')[1]).split('.')[0]).split(':')[0]
    elif timedateformat == 'complete':
        return str(datetime.now())
    elif timedateformat == 'datetime':
        return (str(datetime.now())).split('.')[0]
    elif timedateformat == 'timedate':
        return ((str(datetime.now())).split('.')[0]).split(' ')[1] + ' ' + ((str(datetime.now())).split('.')[0]).split(' ')[0]


#sensor = Adafruit_DHT.DHT22
pin = 4
GPIO.setmode(GPIO.BCM)
ledpin = 17
GPIO.setup(ledpin, GPIO.OUT)
GPIO.output(ledpin, GPIO.HIGH)
#sleep(1)
#declare this way to avoid locking the cam for other scripts, this way it should be opened and closed
with picamera.PiCamera() as camera:
    #camera.resolution = (720,720)
    camera.awb_mode= 'sunlight'


    #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    #stringhumidity =  ("%s" % round(humidity,0)).replace('.','_')
    #stringtemperature = ("%s" % round(temperature,0)).replace('.', '_')
    filepath = "/home/pi/Documents/Images/" + getdatetime("year") + getdatetime("month") + getdatetime("day") + getdatetime("hour") + getdatetime("minute") + getdatetime("second")+ ".jpg"
    print (filepath)
    #print (stringhumidity)
    #print(stringtemperature)
    camera.capture(filepath)

    
print("pic taken")
GPIO.output(ledpin, GPIO.LOW)
GPIO.cleanup()


