import sys
import datetime

def log(message):
    print("{}: {}".format(datetime.datetime.now(), message))
    sys.stdout.flush()
