'''
Created on 20 May 2016

@author: Alan Greer
'''


import argparse
import xlrd

from percival_detector.log import log


class WorksheetParser(object):
    def __init__(self, worksheet):
        self._worksheet = worksheet

    def parse(self, field_names):
        empty_count = 0
        column = 0
        fields = {}
        found_channels = {}
        groups = []
        for row in range(0, self._worksheet.nrows):
            value = self._worksheet.cell(row, column).value
            if value == xlrd.empty_cell.value:
                empty_count += 1
            else:
                log.info("Cell: %s", value)
                if '#' in value[0]:
                    log.info("Comment so ignore this cell")
                else:
                    found_field = False
                    for field_name in field_names:
                        if field_name in value:
                            log.info("Found %s tag in row %d", field_name, row)
                            fields[field_name] = row
                            found_field = True
                            break

                    if not found_field:
                        found_channels[value] = row

        # Now loop over all of the columns to capture the group information
        for column in range(1, self._worksheet.ncols):
            group = {}
            # Add the field information to each group dictionary
            for field_name in field_names:
                group[field_name] = self._worksheet.cell(fields[field_name], column).value

            # Now add the channel information
            group["channels"] = {}
            for channel in found_channels:
                value = self._worksheet.cell(found_channels[channel], column).value
                if value == xlrd.empty_cell.value:
                    empty_count += 1
                else:
                    group["channels"][channel] = value
                    log.info("Adding channel [%s] to group", channel)
            groups.append(group)

        return groups


class ControlGroupGenerator(object):
    def __init__(self, workbook):
        self._workbook = workbook

    def generate_ini_file(self, filename):
        if "control_groups" in self._workbook.sheet_names():
            parser = WorksheetParser(self._workbook.sheet_by_name("control_groups"))
            groups = parser.parse(['Group_ID', 'Description'])

            # Now produce an ini file with the group information stored
            group_no = 0
            with open(filename, "w") as file:
                for group in groups:
                    file.write("[Control_Group<{:04d}>]\n".format(group_no))
                    file.write("Group_name = \"{}\"\n".format(group['Group_ID']))
                    file.write("Group_description = \"{}\"\n".format(group['Description']))
                    channel_no = 0
                    for channel in group["channels"]:
                        if group["channels"][channel] == 1:
                            file.write("Channel_name<{:04d}> = \"{}\"\n".format(channel_no, channel))
                            channel_no += 1

                    file.write("\n")
                    group_no += 1


class MonitorGroupGenerator(object):
    def __init__(self, workbook):
        self._workbook = workbook

    def generate_ini_file(self, filename):
        if "monitor_groups" in self._workbook.sheet_names():
            parser = WorksheetParser(self._workbook.sheet_by_name("monitor_groups"))
            groups = parser.parse(['Group_ID', 'Description'])

            # Now produce an ini file with the group information stored
            group_no = 0
            with open(filename, "w") as file:
                for group in groups:
                    file.write("[Monitor_Group<{:04d}>]\n".format(group_no))
                    file.write("Group_name = \"{}\"\n".format(group['Group_ID']))
                    file.write("Group_description = \"{}\"\n".format(group['Description']))
                    channel_no = 0
                    for channel in group["channels"]:
                        if group["channels"][channel] == 1:
                            file.write("Channel_name<{:04d}> = \"{}\"\n".format(channel_no, channel))
                            channel_no += 1

                    file.write("\n")
                    group_no += 1


class SetpointGroupGenerator(object):
    def __init__(self, workbook):
        self._workbook = workbook

    def generate_ini_file(self, filename):
        if "setpoint_groups" in self._workbook.sheet_names():
            parser = WorksheetParser(self._workbook.sheet_by_name("setpoint_groups"))
            groups = parser.parse(['Setpoint_ID', 'Description'])

            # Now produce an ini file with the group information stored
            group_no = 0
            with open(filename, "w") as file:
                for group in groups:
                    file.write("[Setpoint_Group<{:04d}>]\n".format(group_no))
                    file.write("Setpoint_name = \"{}\"\n".format(group['Setpoint_ID']))
                    file.write("Setpoint_description = \"{}\"\n".format(group['Description']))
                    for channel in group["channels"]:
                        file.write("{} = {}\n".format(channel, group["channels"][channel]))

                    file.write("\n")
                    group_no += 1


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, action='store', help="Input spreadsheet to parse")
    parser.add_argument("-d", "--directory", action='store', default=".",
                        help="Output directory to write config ini files to")
    args = parser.parse_args()
    return args


def main():
    args = options()
    log.info(args)

    workbook = xlrd.open_workbook(args.input)
    cgg = ControlGroupGenerator(workbook)
    cgg.generate_ini_file(args.directory+"/ControlGroups.ini")

    mgg = MonitorGroupGenerator(workbook)
    mgg.generate_ini_file(args.directory+"/MonitorGroups.ini")

    sgg = SetpointGroupGenerator(workbook)
    sgg.generate_ini_file(args.directory+"/SetpointGroups.ini")


if __name__ == '__main__':
    main()
