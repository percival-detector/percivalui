

import requests
import time
import getpass
from datetime import datetime
import percival_detector.log

slogger = percival_detector.log.logger("percival_scripts")

class PercivalClient(object):
    def __init__(self, address="127.0.0.1:8888", api=0.1):
        self._address = address
        self._api = api
        self._url = "http://" + str(self._address) + "/api/" + str(self._api) + "/percival/"
        self._user = getpass.getuser()

    def send_command(self, command, command_id="python_script", arguments=None, wait=True):
        try:
            url = self._url + command
            slogger.debug("Sending msg to: %s", url)
            result = requests.put(url,
                                  data=arguments,
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Accept': 'application/json',
                                      'User': self._user,
                                      'Creation-Time': str(datetime.now()),
                                      'User-Agent': command_id
                                  }).json()
        except requests.exceptions.RequestException:
            result = {
                "error": "Exception during HTTP request, check address and Odin server instance"
            }
            slogger.exception(result['error'])

        if wait:
            if result['response'] != 'Failed':
                result = self.wait_for_command_completion()

        return result

    def get_status(self, status_item, arguments=None):
        try:
            url = self._url + status_item
            slogger.debug("Sending msg to: %s", url)
            result = requests.get(url,
                                  data=arguments,
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Accept': 'application/json',
                                      'User': self._user,
                                      'Creation-Time': str(datetime.now())
                                  }).json()
        except requests.exceptions.RequestException:
            result = {
                "error": "Exception during HTTP request, check address and Odin server instance"
            }
            slogger.exception(result['error'])

        return result

    def wait_for_command_completion(self, wait_time=0.5):
        response = None
        command_active = True
        while command_active:
            response = self.get_status('action')
            slogger.debug(response)
            if response['response'] == 'Active':
                time.sleep(wait_time)
            else:
                command_active = False
        return response

    def send_configuration(self, config_type, config_contents, command_id="python_script", wait=True):
        arguments = {
            'config_type': config_type,
            'config': config_contents.replace('=', '::')
        }
        return self.send_command('cmd_load_config', command_id, arguments, wait=wait)

    def send_system_command(self, system_command, command_id="python_script", wait=True):
        arguments = {
            'name': system_command.name
        }
        return self.send_command('cmd_system_command', command_id, arguments, wait=wait)

    def set_system_setting(self, setting, value, command_id="python_script", wait=True):
        arguments = {
            'setting': setting,
            'value': value
        };
        return self.send_command('cmd_system_setting',
                                 command_id,
                                 arguments,
                                 wait=wait)

    def apply_setpoint(self, set_point, command_id="python_script", wait=True):
        arguments = {
            'setpoint': set_point
        }
        return self.send_command('cmd_apply_setpoint', command_id, arguments, wait=wait)

class DAQClient(object):
    def __init__(self, address="127.0.0.1:8888", api=0.1):
        self._address = address
        self._api = api
        self._url = "http://" + str(self._address) + "/api/" + str(self._api) + "/fp/"
        self._user = getpass.getuser()

    def send_command(self, command, arguments=None):
        try:
            url = self._url + 'config/' + command
            slogger.debug("Sending msg to: %s", url)
            result = requests.put(url,
                                  data='{}'.format(arguments),
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Accept': 'application/json'
                                  }).json()
        except requests.exceptions.RequestException:
            result = {
                "error": "Exception during HTTP request, check address and Odin server instance"
            }
            slogger.exception(result['error'])

        slogger.debug("{}".format(result))

        return result

    def send_reset(self):
        try:
            url = self._url + 'command/reset_statistics'
            slogger.debug("Sending msg to: %s", url)
            result = requests.put(url,
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Accept': 'application/json'
                                  }).json()
        except requests.exceptions.RequestException:
            result = {
                "error": "Exception during HTTP request, check address and Odin server instance"
            }
            slogger.exception(result['error'])

        slogger.debug("{}".format(result))

        return result

    def get_status(self):
        try:
            url = self._url + 'status'
            slogger.debug("Sending msg to: %s", url)
            result = requests.get(url,
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Accept': 'application/json'
                                  }).json()
        except requests.exceptions.RequestException:
            result = {
                "error": "Exception during HTTP request, check address and Odin server instance"
            }
            slogger.exception(result['error'])

        return result

    def get_config(self, item):
        try:
            url = self._url + 'config/' + '{}'.format(item)
            slogger.debug("Sending msg to: %s", url)
            result = requests.get(url,
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Accept': 'application/json'
                                  }).json()
        except requests.exceptions.RequestException:
            result = {
                "error": "Exception during HTTP request, check address and Odin server instance"
            }
            slogger.exception(result['error'])

        return result

    def set_frames(self, frames):
        return self.send_command('hdf/frames', frames)

    def set_file_path(self, path):
        return self.send_command('hdf/file/path', path)

    def set_file_name(self, filename):
        return self.send_command('hdf/file/name', filename)

    def set_master_dset(self, dset):
        return self.send_command('hdf/master', dset)

    def start_writing(self):
        # Reset the FPs
        response = self.send_reset()
        if 'error' in response:
            return response

        # If no error was returned send the command to start writing
        response = self.send_command('hdf/write', '1')
        if 'error' in response:
            return response

        # Now read the status and wait for the write flag to become true
        read_count = 0
        while read_count < 50:
            time.sleep(0.1)
            response = self.get_status()
            fps = response['value']
            writing = []
            for fp in fps:
                writing.append(fp['hdf']['writing'])
            if all(writing):
                return {}

        return {'error': 'Timed out waiting for HDF to start writing'}

    def stop_writing(self):
        return self.send_command('hdf/write', '0')
