import argparse
from controller import Controller
import signal
from Components.SerialConnection import SerialConnection

### Get cmd line arguments from user ###

parser = argparse.ArgumentParser(description='Program controller')

parser.add_argument('-o', '--outfile')
parser.add_argument('-w', '--web_out')
parser.add_argument('-p', '--port', default='/dev/ttyUSB0')


args = parser.parse_args()

if args.outfile == None and args.web_out == None:
    print('specify at least one output destination')
    exit()

arg_outfile = args.outfile
arg_web_out = args.web_out
arg_port = args.port

main_controller = Controller(SerialConnection,
                                 arg_outfile,
                                 arg_web_out,
                                 arg_port)


### functions to start and stop controller ###

def start_controller(arg_port, arg_outfile, arg_web_out, main_controller):
    main_controller.start()

def stop_controller(signal, frame, main_controller):
    print('Ctrl-C detected. Stopping script')
    main_controller.stop()
    exit(0)


### execute stop_controller when ctrl-c (signal interrupt) is detected ###

signal.signal(signal.SIGINT, stop_controller(signal, frame, main_controller))


### start the controller ###

start_controller(arg_baud, arg_outfile, arg_web_out, arg_port, main_controller)


### run forever ###

while True:
    pass