import pandas as pd


def get_df_from_file(filename: str):
    df = pd.read_csv(filename, header=None, names=["shaft_rpm", "shaft_torque"])
    return df


def is_valid_csv(filename: str):
    try:
        get_df_from_file(filename)
    except pd.errors.ParserError as e:
        print(e)
        print("not valid_csv")
    else:
        return True

    return False
