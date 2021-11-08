

import argparse
import json
import requests

from percival.log import get_exclusive_file_logger


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", action="store", default="http://127.0.0.1:8888", help="Address of Odin server")
    parser.add_argument("-a", "--api", action="store", default="0.1", help="API version")
    args = parser.parse_args()
    return args


def main():
    global log
    log = get_exclusive_file_logger("odin_client.log")
    args = options()
    log.info(args)

    url = args.url + "/api/" + args.api + "/"

    msg = url + "percival/ctrl_test_group/25"
    log.debug("Sending msg: %s", msg)
    try:
        requests.put(msg,
                     headers={
                              'Content-Type': 'application/json',
                              'Accept': 'application/json'
                     }).json()
    except requests.exceptions.RequestException:
        result = {
            "error": "Exception during HTTP request, check address and Odin server instance"
        }
        log.exception(result['error'])


if __name__ == '__main__':
    main()
