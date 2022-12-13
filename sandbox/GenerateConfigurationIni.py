'''
Created on 24 July 2017

@author: Alan Greer
'''

from builtins import range  # pylint: disable=W0622
from percival_detector.log import log


def main():
    log.info("Generating file SensorCalibration.ini in config dir...")

    try:
        with open("config/SensorConfiguration.ini", "w") as c_file:
            c_file.write("[General]\n")
            c_file.write("Cols<H1>= 704\n")
            c_file.write("Cols<H0>= 704\n")
            c_file.write("Cols<G>= 32\n")
            c_file.write("\n")
            c_file.write("[H1]\n")
            for index in range(704):
                c_file.write("Col<{}>=0\n".format(index))
            c_file.write("\n")
            c_file.write("[H0]\n")
            for index in range(704):
                c_file.write("Col<{}>=0\n".format(index))
            c_file.write("\n")
            c_file.write("[G]\n")
            for index in range(32):
                c_file.write("Col<{}>=0\n".format(index))
            c_file.write("\n")
    except:
        log.info("File generation failed...")

if __name__ == '__main__':
    main()
