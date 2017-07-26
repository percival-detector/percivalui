'''
Created on 24 July 2017

@author: Alan Greer
'''
from __future__ import print_function
from builtins import range  # pylint: disable=W0622
from percival.log import log


def main():
    log.info("Generating file SensorCalibration.ini in config dir...")

    try:
        with open("config/SensorCalibration.ini", "w") as c_file:
            c_file.write("[General]\n")
            c_file.write("Cols_<H1>= 704\n")
            c_file.write("Cols_<H0>= 704\n")
            c_file.write("Cols_<G>= 32\n")
            c_file.write("\n")
            c_file.write("[H1]\n")
            for index in range(704):
                for cal in range(4):
                    c_file.write("RightCal<{}>Col<{}>=0\n".format(cal, index))
                    c_file.write("LeftCal<{}>Col<{}>=0\n".format(cal, index))
            c_file.write("\n")
            c_file.write("[H0]\n")
            for index in range(704):
                for cal in range(4):
                    c_file.write("RightCal<{}>Col<{}>=0\n".format(cal, index))
                    c_file.write("LeftCal<{}>Col<{}>=0\n".format(cal, index))
            c_file.write("\n")
            c_file.write("[G]\n")
            for index in range(32):
                for cal in range(4):
                    c_file.write("RightCal<{}>Col<{}>=0\n".format(cal, index))
                    c_file.write("LeftCal<{}>Col<{}>=0\n".format(cal, index))
            c_file.write("\n")
    except:
        log.info("File generation failed...")

if __name__ == '__main__':
    main()
