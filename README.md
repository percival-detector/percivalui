[![Build Status](https://travis-ci.org/percival-detector/percivalui.svg)](https://travis-ci.org/percival-detector/percivalui)
[![Coverage Status](https://coveralls.io/repos/percival-detector/percivalui/badge.svg?branch=master)](https://coveralls.io/r/percival-detector/percivalui?branch=master)
[![Code Health](https://landscape.io/github/percival-detector/percivalui/master/landscape.svg?style=flat)](https://landscape.io/github/percival-detector/percivalui/master)

# Percival UI #

The Percival detector python user interface.

Please see the central user and developer documentation on the [percival-detector github pages](http://percival-detector.github.io)

The percivalui project allow users and detector engineers to control the Percival detector system from a python based user interface. The userinterface is simply a python class where properties and methods can be manipulated to control the detector.

It is released under the Apache License 2.0.


## Dependencies ##

This package is developed with Python 3.7.
Every git Push is tested using [travis-ci](https://travis-ci.org/percival-detector/percivalui) with Python 3.4.

System dependencies:
* Python (3.7)
* pip - python package manager
* HDF5 libraries (development package)
* ZeroMQ (development package)
* InfluxDB - time series database
* Grafana - analytics and monitoring
* odin-control - 1.1.0 is python3 compatible
* odin-data - 1.6.0 is python3 compatible
* pySerial - for connection with uninterruptible power supply (optional).

Building with setuptools will attempt to use pip to download and install dependencies locally first. The python dependencies are listed in requirements.txt

## Installation ##

### Installing InfluxDB ###

Instructions for installing InfluxDB can be found [here](https://portal.influxdata.com/downloads).  It is recommended that the database be installed as a package for your specific OS.  To install on CentOS the following steps are appropriate:

    cd ~
    mkdir -p packages
    cd packages
    wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.7.6-1.x86_64.rpm
    sudo yum localinstall influxdb-1.8.10.x86_64.rpm

The database is run as a service and can be set to automatically run when the machine boots.  It is also possible to install linux binaries or install from source, visit the link for further information and instructions. If possible, also see the page at confluence.desy.de.

### Installing Grafana OSS ###

You may not need grafana as Influxdb2 has its own graphing capability. It appears here for legacy reasons.
Full instructions for installing Grafana can be found [here](https://grafana.com/grafana/download).  To install on CentOS the following steps are appropriate:

    cd ~
    mkdir -p packages
    cd packages
    wget https://dl.grafana.com/oss/release/grafana-8.2.0.linux-amd64.tar.gz
    tar -zxvf grafana-8.2.0.linux-amd64.tar.gz
    sudo yum localinstall grafana-4.3.2-1.x86_64.rpm

The platform is run as a service and can be set to automatically run when the machine boots.  It is also possible to install linux binaries or install from source, visit the link for further information and instructions.

### Installing Percival Control Software ###

Download the sources of this repository using git. If your site network goes through a HTTP(S) proxy server, you may need to set the environment variables http_proxy and https_proxy:

    export http_proxy=mysite.proxy.server:port
    export https_proxy=mysite.proxy.server:port
    
    git clone https://github.com/percival-detector/percivalui.git
    
If you have a github account, you can load your public ssh key into your profile and enjoy key-authenticated, passwordless access (if you later need to push changes up) via the ssh protocol (no proxy environment settings required):

    git@github.com:percival-detector/percivalui.git


Building and installing the sources and scripts can be done with the usual python package build system (i.e. setuptools)
and it is recommended to setup a virtualenv first:

	cd percivalui
	
	# Setup your virtual python3 environment and activate it
	virtualenv --no-site-packages -p /path/to/python3.7 venv3
	source venv3/bin/activate
	
	# Point to your HDF5 installation if it is not in the system path
	export HDF5_DIR=/path/to/your/hdf5/installation
	
	# Please read requirements.txt and setup any specific requirements for your system.
	# Install the python dependencies
	pip install -r requirements.txt
	
	# Run the unittests to ensure everything is setup in the environment
	# (tested on RHEL7)
	python setup.py nosetests
	
	# Optionally build the documentation
	python setup.py build_sphinx

Once you have everything working you can build and install the product. It is
recommended to install it into a virtual environment in development mode:

    cd percivalui
    
	# activate your virtual python environment 
	source venv3/bin/activate
    
    python setup.py develop (or pip install -e .)

Updating the percivalui code is like this:

    cd percivalui
    
	# activate your virtual python environment 
	source venv3/bin/activate
    
    # Clean up before updating
    python setup.py develop --uninstall
    
    git pull origin
    
    python setup.py develop

## Execution ##

Before attempting to execute ensure that the installation steps above have been completed successfully.

### Configuration Files ###

The configuration file "./config/percival.ini" contains the IP address of the detector hardware as well as the connection details for the InfluxDB database.  This file should be edited and the values set correctly before executing the software.
The file is in a human readable ini format, an example is provided below:

    [Control]
    carrier_ip = "127.0.0.1"

    [Database]
    address = "127.0.0.1"
    port = 8086
    name = "percival"

    [Configuration]
    #setpoints = "config/SetpointGroups.ini"
    #control_groups = "config/ControlGroups.ini"
    #monitor_groups = "config/MonitorGroups.ini"

| Section | Parameter | Description |

| Control | carrier_ip | IP address of Percival control board.  The value of "127.0.0.1" shown above is for use when executing the Odin server against a software-simulation and should be changed to the ip-address of the carrier-board. |
| Database | address | IP address of InfluxDB server.  If the database server is running on the same machine as the Odin server then this value can be set to 127.0.0.1 |
| Database | port | Port number of the InfluxDB server.  The value of 8086 is the recommended norm. |
| Database | name | Name of the database to use for recording data.  If the database does not exist then it is created.  This should not need to be changed from the default value "percival" |


The configuration file "./percival_test.cfg" is used to configure the Odin server instance, containing the information required to load the Percival control plugin into the server.  The file is also used to specify which port the Odin server will serve HTTP requests on.  Currently it is not expected that this file should be changed, the contents are shown below:

    [server]
    debug_mode = 1
    http_port  = 8888
    http_addr  = 0.0.0.0
    static_path = ./static
    adapters   = percival

    [tornado]
    logging = debug

    [adapter.percival]
    module = percival_detector.control.percival_adapter.PercivalAdapter

| Section | Parameter | Description |

| server | debug_mode | Debugging mode for the Odin server application |
| server | http_port | Port number that Odin uses to serve the HTTP requests |
| server | http_addr | Address that Odin binds to for serving HTTP requests |
| server | static_path | Path that is used by Odin to serve the GUI webpages |
| tornado | logging | Log level for the tornado web server that Odin uses |
| adapter.percival | module | Name of module to load into the Odin server, set to percival_detector.control.percival_adapter.PercivalAdapter |

NOTE: The above configuration file "percival_test.cfg" should not need to be changed for the Percival control application.  All of the default values are setup for the Percival control software.

### Running the Odin Server

Once installation is complete running the Odin server requires only the setting up of the Python virtual environment followed by the execution of the Odin instance:

	# cd to the correct location
	cd percivalui

	# activate your virtual python environment
	source venv3/bin/activate

	# Execute the Odin server
	odin_control --config=percival_test.cfg

Once the server is running you can open a web browser and browse to the correct address of the odin server (e.g. 127.0.0.1:8888).  You will be presented with the home page shown below:

![alt text](docs/images/odin_percival_server.png "Odin Server Web Interface")

## Docs ##

The built documentation will be located in `docs/build/html/index.html`
