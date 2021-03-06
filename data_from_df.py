import pandas as pd
from physics import get_torque_on_wheel, get_power_in_KM, get_engine_rot_speed


def add_to_df_with_wheel_torque(df: pd.DataFrame, wheel_diameter_cm):
    df["torque_on_wheel"] = df.apply(
        lambda row: get_torque_on_wheel(row.shaft_torque, wheel_diameter_cm),
        axis=1,
    )


def add_to_df_power_in_KM(df: pd.DataFrame):
    df["power_in_KM"] = df.apply(
        lambda row: get_power_in_KM(row.shaft_rpm, row.shaft_torque), axis=1
    )


def add_to_df_engine_rot_speed(df: pd.DataFrame, wheel_diam_cm, gear_ratio):
    df["engine_rot_speed"] = df.apply(
        lambda row: get_engine_rot_speed(row.shaft_rpm, wheel_diam_cm, gear_ratio),
        axis=1,
    )


def get_max_power_in_KM(df: pd.DataFrame):
    return df["power_in_KM"].max()
