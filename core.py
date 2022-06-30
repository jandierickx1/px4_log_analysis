#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 11:45:57 2022

@author: Jan Dierickx
"""

from functools import reduce
import os
import pandas as pd


def read_log_file(filename, parameters):
    """
    Converts a pyulog file to a pandas dataframe.

    Parameters
    ----------
    filename (str): Name of the ulog file to read
    parameters (list): list of PX4 outputs to save in dataframe. 
    Available parameters are:
    system_power_0
    rate_ctrl_status_0
    home_position_0
    estimator_selector_status_0
    estimator_innovation_test_ratios_1
    estimator_states_1
    sensor_gyro_1
    sensor_accel_1
    esc_status_0
    estimator_innovation_test_ratios_2
    estimator_event_flags_1
    mission_0
    radio_status_0
    vehicle_imu_1
    commander_state_0
    px4io_status_0
    estimator_attitude_3
    yaw_estimator_status_3
    esc_telem_uart_0
    adc_report_0
    differential_pressure_0
    estimator_innovation_test_ratios_0
    ekf_gps_drift_3
    vehicle_land_detected_0
    position_setpoint_triplet_0
    vehicle_acceleration_0
    manual_control_setpoint_0
    estimator_attitude_2
    battery_status_0
    mission_result_0
    cpuload_0
    ekf_gps_drift_0
    estimator_event_flags_0
    estimator_status_flags_2
    actuator_armed_0
    estimator_global_position_2
    battery_status_1
    sensor_combined_0
    estimator_status_flags_3
    vehicle_attitude_setpoint_0
    vehicle_imu_status_1
    position_controller_status_0
    estimator_event_flags_3
    estimator_local_position_2
    estimator_innovation_variances_0
    sensor_baro_0
    estimator_status_1
    estimator_innovation_variances_1
    actuator_controls_3_0
    rate_ctrl_status_1
    vehicle_imu_0
    airspeed_wind_0
    test_motor_0
    estimator_local_position_3
    safety_0
    estimator_states_0
    vehicle_imu_status_0
    estimator_innovations_1
    estimator_local_position_1
    sensors_status_imu_0
    telemetry_status_0
    yaw_estimator_status_2
    actuator_outputs_0
    estimator_global_position_1
    airspeed_validated_0
    logger_status_0
    parameter_update_0
    estimator_innovations_2
    estimator_global_position_3
    ekf_gps_drift_1
    sensor_gyro_fft_0
    vehicle_gps_position_0
    estimator_attitude_1
    estimator_sensor_bias_0
    sensor_gyro_0
    estimator_sensor_bias_2
    yaw_estimator_status_0
    estimator_event_flags_2
    estimator_wind_0
    yaw_estimator_status_1
    estimator_states_2
    vehicle_angular_velocity_0
    estimator_innovation_variances_2
    estimator_sensor_bias_3
    vehicle_global_position_0
    vehicle_control_mode_0
    vtol_vehicle_status_0
    actuator_outputs_1
    vehicle_rates_setpoint_0
    vehicle_angular_acceleration_0
    estimator_status_flags_0
    takeoff_status_0
    estimator_status_3
    rtl_flight_time_0
    estimator_wind_2
    airspeed_0
    estimator_wind_3
    estimator_innovation_test_ratios_3
    input_rc_0
    actuator_controls_1_0
    sensor_mag_0
    vehicle_status_flags_0
    vehicle_air_data_0
    estimator_innovation_variances_3
    estimator_sensor_bias_1
    estimator_attitude_0
    estimator_local_position_0
    ekf_gps_drift_2
    airspeed_wind_1
    sensor_mag_1
    vehicle_attitude_0
    estimator_status_2
    vehicle_local_position_0
    vehicle_magnetometer_1
    vehicle_status_0
    sensor_selection_0
    estimator_global_position_0
    actuator_controls_0_0
    estimator_innovations_0
    estimator_innovations_3
    sensor_gps_0
    estimator_status_flags_1
    manual_control_switches_0
    vehicle_magnetometer_0
    sensor_preflight_mag_0
    sensor_accel_0
    estimator_states_3
    multirotor_motor_limits_0
    estimator_wind_1
    estimator_status_0
    wind_0




    Returns
    -------
    df_merged (dataframe): A Pandas dataframe with flight variables as colums
    
    
    Example
    -------
    df = read_log_file('file.ulg', ['battery_status_0', 'esc_telem_uart_0'])

    """
    
    os.system('mkdir temp')
    os.chdir('temp')
    try:
        os.system('cp ../' + filename + ' .')
        os.system('ulog2csv ' + filename)
        data_frames = []
        for ii in range(len(parameters)):
            data_frames.append(pd.read_csv(filename[:-4] + '_' + parameters[ii] + '.csv'))
            data_frames[ii].timestamp = pd.to_datetime(data_frames[ii]['timestamp'], unit='us')
     
    finally:
        os.chdir('..')
        os.system('rm -r temp')
    
    
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['timestamp'],
                                            how='outer'), data_frames)
    df_merged = df_merged.set_index('timestamp')
    
    df_merged.sort_index(inplace=True)
    df_merged.interpolate(inplace=True)
    
    return df_merged
