from physics import get_torque_on_wheel, get_power_in_KM, get_engine_rot_speed


def test_get_torque_on_wheel():
    assert get_torque_on_wheel(shaft_torque=1, wheel_diameter_in_cm=22) == 1


def test_get_power_in_KM():
    assert get_power_in_KM(shaft_rotspeed=1, shaft_torque=1) == 0.1428


def test_get_engine_rot_speed():
    assert get_engine_rot_speed(1, gear_ratio=1, wheel_diameter_in_cm=22) == 1
