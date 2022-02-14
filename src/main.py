import argparse
import datetime
import logging
import os
import shutil
import signal
import sys

from Components.Controller import Controller
from Components.SerialConnection import SerialConnection
from Components.MockSerialConnection import MockSerialConnection
from sys import exit

### Get cmd line arguments from user ###

parser = argparse.ArgumentParser(description='TCD Data Collection')
logging_dir = 'Logs'

parser.add_argument('-o', '--out_file')
# TODO: Add validation to make sure the suffix is .csv
parser.add_argument('-w', '--web_out')
parser.add_argument('-p', '--port', default='/dev/ttyUSB0')
parser.add_argument('-m', '--mode', default='normal')

args = parser.parse_args()

if args.out_file == None and args.web_out == None:
    print('specify at least one output destination')
    exit()

arg_outfile = args.out_file
arg_web_out = args.web_out
arg_port = args.port


if not os.path.isdir(logging_dir):
    try:
        os.mkdir(logging_dir)
    except FileExistsError:
        print("Directory ", logging_dir, " already exists")

# Initialize logger
LOGGER_FILENAME = logging_dir + '/spencer_tcd' + datetime.datetime.now().isoformat() + '.log'
LOGGER_LEVEL = logging.DEBUG
LOGGER_FORMAT = '%(levelname)s:%(message)s'

file_handler = logging.FileHandler(filename=LOGGER_FILENAME)
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(handlers=handlers, level=LOGGER_LEVEL, format=LOGGER_FORMAT)


controller = None
if args.mode == 'demo':
    MockSerialConnection.is_demo = True
    controller = Controller(MockSerialConnection,
                            arg_port,
                            arg_outfile,
                            arg_web_out)
else:
    controller = Controller(SerialConnection,
                            arg_port,
                            arg_outfile,
                            arg_web_out)


### functions to start and stop controller ###

def start_controller():
    controller.start()


def stop_controller(signal, frame):
    print('Ctrl-C detected. Stopping script')
    controller.stop()
    exit(0)


### execute stop_controller when ctrl-c (signal interrupt) is detected ###

signal.signal(signal.SIGINT, stop_controller)


### start the controller ###

start_controller()


### run forever ###

while True:
    continue
