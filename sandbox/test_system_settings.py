'''
Created on 17 May 2016

@author: gnx91527
'''


from percival.log import log

from percival.carrier.registers import SystemSettingsMap
from percival.carrier.configuration import SystemSettingsParameters
from percival.carrier.system import SystemSettings
from percival.carrier.txrx import TxRxContext

def main():
    test_map = SystemSettingsMap()
    test_map.REGION_OF_INTEREST_ROI_mode = 0
    test_map.REGION_OF_INTEREST_Illumination = 0
    test_map.REGION_OF_INTEREST_Sensor_type = 0
    test_map.REGION_OF_INTEREST_Vertical_ROI_start_row_group = 0
    test_map.REGION_OF_INTEREST_Vertical_ROI_start_block = 0
    test_map.REGION_OF_INTEREST_Vertical_ROI_stop_row_group = 0
    test_map.REGION_OF_INTEREST_Vertical_ROI_stop_block = 2
    test_map.REGION_OF_INTEREST_Horizontal_ROI_start_column = 0
    test_map.REGION_OF_INTEREST_Horizontal_ROI_start_block = 0
    test_map.REGION_OF_INTEREST_Horizontal_ROI_stop_column = 0
    test_map.REGION_OF_INTEREST_Horizontal_ROI_stop_block = 1
    test_map.ACQUISITION_Continuous_acquisition = 0
    test_map.ACQUISITION_Acquisition_mode = 0
    test_map.ACQUISITION_Number_of_frames = 100
    test_map.INTEGRATION_Integration_mode = 0
    test_map.INTEGRATION_Integration_window_width = 0
    test_map.TRIGGERING_Gate_polarity = 1
    test_map.TRIGGERING_External_gate_signal = 0
    test_map.TRIGGERING_Gating = 0
    test_map.TRIGGERING_Trigger_mode = 1
    test_map.TRIGGERING_Trigger_edge_selection = 0
    test_map.TRIGGERING_External_trigger_signal = 0
    test_map.TRIGGERING_Trigger_source = 0
    test_map.TRIGGERING_Repetition_rate = 0
    test_map.TRIGGERING_Number_of_frames_per_trigger = 0
    test_map.TRIGGERING_Trigger_acquisition_delay = 0
    test_map.ADVANCED_Custom_global_disable_duration = 1
    test_map.ADVANCED_Custom_global_disable_before_each_new_frame = 0
    test_map.SAMPLING_SR_phase_Resampling_mode = 0
    test_map.SAMPLING_S3_phase_Resampling_mode = 0
    test_map.SAMPLING_S2_phase_Resampling_mode = 0
    test_map.SAMPLING_S1_phase_Resampling_mode = 0
    test_map.SAMPLING_S0_phase_Resampling_mode = 1
    test_map.SAMPLING_Sampling_mode = 0
    test_map.SAMPLING_SR_phase_n_factor = 0
    test_map.SAMPLING_S3_phase_n_factor = 0
    test_map.SAMPLING_S2_phase_n_factor = 0
    test_map.SAMPLING_S1_phase_n_factor = 0
    test_map.SAMPLING_S0_phase_n_factor = 1
    test_map.SAMPLING_SR_phase_number_of_repeats = 0
    test_map.SAMPLING_S3_phase_number_of_repeats = 0
    test_map.SAMPLING_S2_phase_number_of_repeats = 0
    test_map.SAMPLING_S1_phase_number_of_repeats = 0
    test_map.SAMPLING_S0_phase_number_of_repeats = 1
    test_map.ADVANCED_dmuxSEL_EXT_options = 0
    test_map.ADVANCED_SC_EXT_options = 0
    test_map.ADVANCED_sr7SC_EXT_options = 0
    test_map.ADVANCED_CPNI_EXT_options = 0
    test_map.ADVANCED_adcCPN_EXT_options = 0
    test_map.ADVANCED_PLLClk_EXT_options = 0
    test_map.ADVANCED_Enable_dmuxSEL_EXT = 0
    test_map.ADVANCED_Enable_SC_EXT = 0
    test_map.ADVANCED_Enable_sr7SC_EXT = 0
    test_map.ADVANCED_Enable_CPNI_EXT = 0
    test_map.ADVANCED_Enable_adcCPN_EXT = 0
    test_map.ADVANCED_Enable_PLLClk_EXT = 0
    test_map.ADVANCED_Calibration_options = 0
    test_map.MONITORING_Monitoring_time_value_s = 0
    test_map.MONITORING_I2C_idle_time_us = 0
    test_map.SAFETY_Priority_7_Action_select = 0
    test_map.SAFETY_Priority_6_Action_select = 0
    test_map.SAFETY_Priority_5_Action_select = 0
    test_map.SAFETY_Priority_4_Action_select = 0
    test_map.SAFETY_Priority_3_Action_select = 0
    test_map.SAFETY_Priority_2_Action_select = 0
    test_map.SAFETY_Priority_1_Action_select = 0
    test_map.SAFETY_Priority_0_Action_select = 1
    test_map.SAFETY_Priority_7_Action_global_enable = 0
    test_map.SAFETY_Priority_6_Action_global_enable = 0
    test_map.SAFETY_Priority_5_Action_global_enable = 0
    test_map.SAFETY_Priority_4_Action_global_enable = 0
    test_map.SAFETY_Priority_3_Action_global_enable = 0
    test_map.SAFETY_Priority_2_Action_global_enable = 0
    test_map.SAFETY_Priority_1_Action_global_enable = 0
    test_map.SAFETY_Priority_0_Action_global_enable = 0
    test_map.MARKER_BOARD_marker_in_3_ENABLE = 0
    test_map.MARKER_BOARD_marker_in_2_ENABLE = 0
    test_map.MARKER_BOARD_marker_in_1_ENABLE = 0
    test_map.MARKER_BOARD_marker_in_0_ENABLE = 0
    test_map.PLUGIN_BOARD_Post_trigger_train_number_capture_delay = 0
    test_map.PLUGIN_BOARD_Include_train_number_in_status_record = 0
    test_map.UNUSED_1 = 0
    test_map.UNUSED_2 = 0

    log.info(test_map.generate_map())

    params = SystemSettingsParameters("./config/SystemSettings.ini")
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

    log.info(test_map.generate_map())

    with TxRxContext("127.0.0.1") as trx:
        sys_settings = SystemSettings(trx, params)
        sys_settings.download_settings()
        sys_settings.set_number_of_frames(1)
        sys_settings.set_number_of_frames(10000)

if __name__ == '__main__':
    main()
