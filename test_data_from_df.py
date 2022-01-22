import pandas as pd

from data_from_df import add_to_df_with_wheel_torque, add_to_df_power_in_KM, add_to_df_engine_rot_speed, get_max_power_in_KM


def test_add_to_df_with_wheel_torque():
    df = pd.DataFrame({'shaft_rpm': [1], 'shaft_torque_Nm': [1]})
    add_to_df_with_wheel_torque(df, wheel_diameter_in_cm=22)
    assert list(df.columns) == ['shaft_rpm', 'shaft_torque_Nm', 'torque_on_wheel']

def test_create_df_with_power_in_KM():
    df = pd.DataFrame({'shaft_rpm': [1], 'shaft_torque_Nm': [1]})
    add_to_df_power_in_KM(df)
    assert list(df.columns) == ['shaft_rpm', 'shaft_torque_Nm', 'power_in_KM']

def test_add_to_df_engine_rot_speed():
    df = pd.DataFrame({'shaft_rpm': [1], 'shaft_torque_Nm': [1]})
    add_to_df_engine_rot_speed(df, 22, 1)
    assert list(df.columns) == ['shaft_rpm', 'shaft_torque_Nm', 'engine_rot_speed']

def test_get_max_power_in_KM():
    df = pd.DataFrame({'power_in_KM': [1, 23, 100, 1]})
    assert get_max_power_in_KM(df) == 100