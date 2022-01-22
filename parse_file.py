import pandas as pd

def get_df_from_file(filename):
    df = pd.read_csv(filename, header=None, names=['shaft_rpm', 'shaft_torque_Nm'])
    return df
