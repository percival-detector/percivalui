'''
Created on 20 May 2016

@author: Alan Greer
'''


import xlrd

from percival.log import logger;

splog = logger("percival.spreadsheet_parser");

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
                splog.debug("Cell: %s", value)
                if '#' in value[0]:
                    splog.debug("Comment so ignore this cell")
                else:
                    found_field = False
                    for field_name in field_names:
                        if field_name in value:
                            splog.debug("Found %s tag in row %d", field_name, row)
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
                    splog.debug("Adding channel [%s] to group", channel)
            groups.append(group)

        return groups


class ControlGroupGenerator(object):
    def __init__(self, workbook):
        self._workbook = workbook

    def generate_ini(self):
        ini_str = ""
        if "control_groups" in self._workbook.sheet_names():
            parser = WorksheetParser(self._workbook.sheet_by_name("control_groups"))
            groups = parser.parse(['Group_ID', 'Description'])

            # Now produce an ini file with the group information stored
            group_no = 0
            for group in groups:
                ini_str +=  "[Control_Group<{:04d}>]\n".format(group_no)
                ini_str += "Group_name = \"{}\"\n".format(group['Group_ID'])
                ini_str += "Group_description = \"{}\"\n".format(group['Description'])
                channel_no = 0
                for channel in group["channels"]:
                    if group["channels"][channel] == 1:
                        ini_str += "Channel_name<{:04d}> = \"{}\"\n".format(channel_no, channel)
                        channel_no += 1

                ini_str += "\n"
                group_no += 1
        return ini_str


class MonitorGroupGenerator(object):
    def __init__(self, workbook):
        self._workbook = workbook

    def generate_ini(self):
        ini_str = ""
        if "monitor_groups" in self._workbook.sheet_names():
            parser = WorksheetParser(self._workbook.sheet_by_name("monitor_groups"))
            groups = parser.parse(['Group_ID', 'Description'])

            # Now produce an ini file with the group information stored
            group_no = 0
            for group in groups:
                ini_str += "[Monitor_Group<{:04d}>]\n".format(group_no)
                ini_str += "Group_name = \"{}\"\n".format(group['Group_ID'])
                ini_str += "Group_description = \"{}\"\n".format(group['Description'])
                channel_no = 0
                for channel in group["channels"]:
                    if group["channels"][channel] == 1:
                        ini_str += "Channel_name<{:04d}> = \"{}\"\n".format(channel_no, channel)
                        channel_no += 1

                ini_str += "\n"
                group_no += 1
        return ini_str


class SetpointGroupGenerator(object):
    def __init__(self):
        pass;

    def generate_ini(self, workbook):
        ini_str = ""
        if "setpoint_groups" in workbook.sheet_names():
            parser = WorksheetParser(workbook.sheet_by_name("setpoint_groups"))
            groups = parser.parse(['Setpoint_ID', 'Description'])

            # Now produce an ini file with the group information stored
            allsps = [];
            for group in groups:
                setpoint_id = group['Setpoint_ID'];
                if setpoint_id and setpoint_id not in allsps:
                  ini_str += "[Setpoint_Group<{0}>]\n".format(setpoint_id)
                  ini_str += "Setpoint_name = \"{}\"\n".format(setpoint_id)
                  ini_str += "Setpoint_description = \"{}\"\n".format(group['Description'])
                  for channel in group["channels"]:
                      ini_str += "{} = {}\n".format(channel, group["channels"][channel])

                  ini_str += "\n"
                  allsps.append(setpoint_id);
                else:
                  # check for duplicate and null setpoint_ids in a single spreadsheet
                  raise RuntimeError("Bad setpoint: {0}".format(setpoint_id));

        return ini_str
