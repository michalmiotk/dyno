import pandas as pd

from data_from_df import (
    add_to_df_with_wheel_torque,
    add_to_df_power_in_KM,
    add_to_df_engine_rot_speed,
    get_max_power_in_KM,
)


def test_add_to_df_with_wheel_torque():
    df = pd.DataFrame({"shaft_rpm": [1], "shaft_torque": [1]})
    add_to_df_with_wheel_torque(df, wheel_diameter_cm=22)
    expected_columns = ["shaft_rpm", "shaft_torque", "torque_on_wheel"]
    assert list(df.columns) == expected_columns


def test_create_df_with_power_in_KM():
    df = pd.DataFrame({"shaft_rpm": [1], "shaft_torque": [1]})
    add_to_df_power_in_KM(df)
    assert list(df.columns) == ["shaft_rpm", "shaft_torque", "power_in_KM"]


def test_add_to_df_engine_rot_speed():
    df = pd.DataFrame({"shaft_rpm": [1], "shaft_torque": [1]})
    add_to_df_engine_rot_speed(df, 22, 1)
    expected_columns = ["shaft_rpm", "shaft_torque", "engine_rot_speed"]
    assert list(df.columns) == expected_columns


def test_get_max_power_in_KM():
    df = pd.DataFrame({"power_in_KM": [1, 23, 100, 1]})
    assert get_max_power_in_KM(df) == 100
