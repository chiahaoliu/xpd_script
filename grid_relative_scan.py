import bluesky.plans as bp

# step0: align with first well
x_0 = motor_x.get()
y_0 = motor_y.get()

# define your motor and detector here
area_det = None
motor_x = None
motor_y = None
detector_list = [area_det, motor_x, motor_y] # append whatever you want
for el in detector_list:
    if el is None:
        raise RuntimeError('Required detector is not defined yet')


# for loop
def grid_scan_v1(dx, dy, x, y, num_x, num_y, x0=None, y0=None):
    """ grid scan over different wells

    inside each of well, a relative scan will be run

    Parameters:
    -----------
    dx : float
        dimension of each well in x-direction. unit depends on motor
    dy : float
        dimension of each well in y-direction. unit depends on motor
    x : float
        separation of wells in x-direction. unit depends on motor
    y : float
        separation of wells in y-direction. unit depends on motor
    num_x : int
        number of wells you have in x-direction
    num_y : int
        number of wells you have in y-direction
    x0 : float
        optional. starting position in x-direction of grid scan.
        usually it is at the center of a well. default is current
        position (assume you align first) 
    y0 : float
        optional. starting position of grid scan. usually it is at the
        center of a well
        position (assume you align first)

    Example:
    --------
    prun(<sample_index>, grid_scan(0.1, 0.1, 1, 1))
    """
    if x0 is None:
        x0 = motor_x.get() #FIXME: syntax
    if y0 is None:
        y0 = motor_y.get()
    for i in range(num_x):
        _x = x0 + num_x*x
        mov(motor_x, _x)
        for j in range(num_y):
            _y = y0 + num_y*y
            mov(motor_y, _y)
            # inside a well, relative scan
            # x direction
            x_scan = bp.relative_list_scan(detector_list, motor_x, [dx, -dx], 2)
            # y direction
            y_scan = bp.relative_list_scan(detector_list, motor_y, [dy, -dy], 2)


# outer_product_scan
def grid_scan_v2(dx, dy, x_f, y_f, num_x, num_y, x0=None, y0=None):
    """ grid scan over different wells

    inside each of well, a relative scan will be run

    Parameters:
    -----------
    dx : float
        dimension of each well in x-direction. unit depends on motor
    dy : float
        dimension of each well in y-direction. unit depends on motor
    x_f : float
        end position of your gird scan in x-direction. it should be the
        center of your well. unit depends on motor
    y_f : float
        end position of your gird scan in y-direction. it should be the
        center of your well. unit depends on motor
    num_x : int
        number of wells you have in x-direction
    num_y : int
        number of wells you have in y-direction
    x0 : float
        optional. starting position in x-direction of grid scan.
        usually it is at the center of a well. default is current
        position (assume you align first)
    y0 : float
        optional. starting position of grid scan. usually it is at the
        center of a well
        position (assume you align first)

    Example:
    --------
    prun(<sample_index>, grid_scan(0.1, 0.1, 3.5, 3.5))
    """
    if x0 is None:
        x0 = motor_x.get() #FIXME: syntax
    if y0 is None:
        y0 = motor_y.get()
    # inside a well, relative scan
    # x direction
    x_scan = bp.relative_list_scan(detector_list, motor_x, [dx, -dx], 2)
    # y direction
    y_scan = bp.relative_list_scan(detector_list, motor_y, [dy, -dy], 2)
    total_relative_scan = bp.pchian(x_scan, y_scan)
    yield from bp.outer_product_scan(detector_list, motor_x, x0, xf,
                                     num_x, motor_y, y0, y_f, num_y, False)
