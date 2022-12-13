'''
Created on 17 May 2016

@author: gnx91527
'''


from percival_detector.log import log

from percival_detector.carrier.registers import ChipReadoutSettingsMap
from percival_detector.carrier.configuration import ChipReadoutSettingsParameters
from percival_detector.carrier.chip import ChipReadoutSettings
from percival_detector.carrier.txrx import TxRxContext


def main():
    test_map = ChipReadoutSettingsMap()

    #log.info(test_map.generate_map())

    params = ChipReadoutSettingsParameters("./config/ChipReadoutSettings.ini")
    params.load_ini()
    map = params.value_map
    log.info(map)
    for item in map:
        if isinstance(map[item], str):
            if 'FALSE' in map[item]:
                map[item] = 0
            elif 'TRUE' in map[item]:
                map[item] = 1

    for item in map:
        try:
            if hasattr(test_map, item):
                test_map.__setattr__(item, int(map[item]))
            else:
                log.info("Did not find %s", item)
        except:
            log.info("Failed %s", item)

    test_map.UNUSED_1 = 0
    test_map.UNUSED_2 = 0
    test_map.UNUSED_3 = 0
    test_map.UNUSED_4 = 0
    test_map.UNUSED_5 = 0

    log.info(test_map.generate_map())

    with TxRxContext("127.0.0.1") as trx:
        sys_settings = ChipReadoutSettings(trx, params)
        sys_settings.download_settings()

if __name__ == '__main__':
    main()
