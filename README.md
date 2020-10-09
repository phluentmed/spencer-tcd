# Spencer ST3 PMD150 TCD (Trans-Cranial Doppler) Data Exporter
_______________________________________________________________________________________________________________________________________
## Table of Contents
- [Overview](#overview)
- [Installing Dependencies](#installing-dependencies)
- [Features](#features)
- [Usage](#usage)
- [Examples](#examples)
- [Tests](#examples)
- [Contact](#contact)

________________________________________________________________________________________________________________________________________
## Overview
This script exports data via USB serial from the Spencer ST3 PMD150 Trans-Cranial 
Doppler machine and saves it in CSV format. The script is also capable of sending the 
collected data to an endpoint using HTTP. Tested on python version > 3.7.x.

## Installing Dependencies
To install the project's dependencies, run: <br>
`pip install -r requirements.txt` <br>
from the root directory of the project.

## Features
This script only exports numeric data packets and currently doesn't support envelope
wave data (if you would like this to besupported, either send us an email or open an
issue). Data is exported in two main flavours:

#### CSV Format
Data can be exported into CSV format by running the script and specifying the file path
along with the file name using the '-o' option. The default configuration saves the 
exported data in batches of 10 datapoints, meaning the CSV file will be written to after the machine 
has exported 10 times. See [Examples](#examples) for sample usage.

#### HTTP
Data can also be exported using HTTP requests by running the script and specifying the
endpoint using the '-w' option. The script sends the data in JSON format via a PUT
request every time data is received from the machine. See [Examples](#examples) for 
sample usage.<br>
**Warning:** With the HTTP option, the data isn't being encrypted while being sent over
the network. It is recommended to only use this option on localhost. Error handling is
not robust.

## Usage
The script should be run from the src directory and takes three arguments:<br>

`python main.py -p <portName> -o <outputFile> -w <endpoint>`<br>

'-p' or '--port' specifies the location (or port name) of the usb port the TCD machine
is connected to. The location on linux/mac os will be in a format similar to 
'/dev/ttyUSB0'. On Windows, it will be in the format 'COM*' (where * represents a 
number).<br><br>

'-o' or '--out_file' specifies the file name and location of the CSV file.<br>

'-w' or '--web_out' specifies the HTTP endpoint to export the data.<br>

The script requires a port and at least one export method to run. As mentioned above, 
the script should be run from inside the src directory to function properly.<br>

## Examples
`python main.py -p /dev/ttyUSB0 -o results/data.csv`<br>
The script will save the exported data to a file called 'data.csv' in the results
directory. HTTP exporting is disabled. The script will produce an error if the 
directory doesn't exist. <br>

`python main.py -p /dev/ttyUSB0 -w localhost/data`<br>
The script will sent exported data via HTTP to the endpoint 'localhost/data'. CSV 
exporting is disabled. <br>

## Tests and Contributions
#### Testing
There's a test suite available to verify any changes made to the code. If you extend
the functionality in any way, you can run: <br>
`python tests.py` <br>
from the src directory to verify any changes made won't break the script.<br>
#### Contributions
If there are any changes or features you think will make the script better, submit a 
pull request and we'll take a look!

## Contact

Please email phluentmed@gmail.com or open an issue if you need any help using the 
code, have any questions, or even have some feature suggestions. If you're
experiencing issues, please send the corresponding log file to help us diagnose
the issue.

