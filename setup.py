"""percivalui setuptools based setup module.

Created on 23 April 2015
@author: Ulrik Pedersen

"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

rootdir = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(rootdir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='percivalui',

    version='0.1.0',

    description='A Python based user control interface to the Percival detector',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/percival-detector/percivalui',

    # Author details
    author='Ulrik Pedersen',
    author_email='ulrik.pedersen@diamond.ac.uk',

    # Choose your license
    license='Apache Software License, Version 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='Percival Xray Detector Science Syncrotron XFEL',

    # Specify the packages that this project provides (using find_packages() for automation)
    packages=find_packages(exclude=['docs', 'sandbox', 'tests*']),

    # run-time dependencies here. These will be installed by pip when the project is installed.
    install_requires=[],


    # Additional groups of dependencies (e.g. development dependencies). 
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'test': ['nose>=1.3', 'coverage', 'mock'],
    },

    # Data files included in the packages
    #package_data={
    #    'sample': ['package_data.dat'],
    #},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'percival-control=percival.percivalcontrol:main',
            'percival-client=percival.client:main',
            'percival-scan-devices=percival.scandevices:main',
            'percival-hl-configure-sensor-dacs=percival.scripts.hl_configure_sensor_dacs:main',
            'percival-hl-apply-setpoint=percival.scripts.hl_apply_setpoint:main',
            'percival-hl-configure-system-settings=percival.scripts.hl_configure_system_settings:main',
            'percival-hl-configure-chip-readout-settings=percival.scripts.hl_configure_chip_readout_settings:main',
            'percival-hl-configure-clock-settings=percival.scripts.hl_configure_clock_settings:main',
            'percival-hl-configure-sensor-configuration=percival.scripts.hl_configure_sensor_configuration:main',
            'percival-hl-configure-sensor-calibration=percival.scripts.hl_configure_sensor_calibration:main',
            'percival-hl-configure-sensor-debug=percival.scripts.hl_configure_sensor_debug:main',
            'percival-hl-configure-control-groups=percival.scripts.hl_configure_control_groups:main',
            'percival-hl-configure-monitor-groups=percival.scripts.hl_configure_monitor_groups:main',
            'percival-hl-configure-setpoints=percival.scripts.hl_configure_setpoints:main',
            'percival-hl-initialise-channels=percival.scripts.hl_initialise_channels:main',
            'percival-hl-download-channel-settings=percival.scripts.hl_download_channel_settings:main',
            'percival-hl-scan-setpoints=percival.scripts.hl_scan_setpoints:main',
            'percival-hl-safety-setpoint-scan=percival.scripts.hl_safety_setpoint_scan:main',
            'percival-hl-set-channel=percival.scripts.hl_set_channel:main',
            'percival-hl-system-command=percival.scripts.hl_system_command:main',
            'percival-hl-update-monitors=percival.scripts.hl_update_monitors:main',
            'percival-hl-apply-sensor-roi=percival.scripts.hl_apply_sensor_roi:main',
            'percival-hl-set-system-setting=percival.scripts.hl_set_system_setting:main',
        ],
    },
)
