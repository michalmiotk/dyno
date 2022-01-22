def get_torque_on_wheel(shaft_torque, wheel_diameter_in_cm):
    #moment obrotowy wału * (średnica koła/22cm)
    return shaft_torque*wheel_diameter_in_cm/22

def get_power_in_KM(shaft_rotspeed, shaft_torque):
    #wykres mocy mechanicznej w KM (1,36*prędkość obrotowa wału * moment obrotowy wału* 0,105)
    return 1.36*shaft_rotspeed*shaft_torque*0.105

def get_engine_rot_speed(shaft_speed, wheel_diameter_in_cm, gear_ratio):
    # prędkość obrotowa silnika (całkowite przełożenie * prędkość wału /(średnica koła/22cm))
    return gear_ratio*shaft_speed*(wheel_diameter_in_cm/22)
