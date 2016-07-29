import bluesky.plans as bp

# define your motor and detector here
area_det = None
motor_x = None
motor_y = None
grid_scan_det_list = [area_det, motor_x, motor_y]
for el in grid_scan_det_list:
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
        optional. starting position in y-direction of grid scan.
        usually it is at the center of a well. default is current
        position (assume you align first)

    Example:
    --------
    prun(<sample_index>, grid_scan_v1(0.1, 0.1, 1, 1, 4, 4))
    # scan oever 4 by 4 grid, with well separated in 1 unit, 1 unit in
    # x- and y- direction respectively, and diameter of each well is
    # 0.1*2 unit
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
            x_scan = bp.relative_list_scan(grid_scan_det_list, motor_x,
                                           [dx, -dx])
            # y direction
            y_scan = bp.relative_list_scan(grid_scan_det_list, motor_y,
                                           [dy, -dy])
            yield from bp.pchian(x_scan, y_scan)

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
        optional. starting position in y-direction of grid scan.
        usually it is at the center of a well. default is current
        position (assume you align first)

    Example:
    --------
    prun(<sample_index>, grid_scan_v2(0.1, 0.1, 3.5, 3.5, 4, 4))
    # a 4 by 4 grid, with dimension 3.5 x 3.5 units in x- and y-
    # direction respectively, and diameter is 0.1*2 unit in each well
    """
    if x0 is None:
        x0 = motor_x.get() #FIXME: syntax
    if y0 is None:
        y0 = motor_y.get()
    # inside a well, relative scan
    # x direction
    x_scan = bp.relative_list_scan(grid_scan_det_list, motor_x, [dx, -dx])
    # y direction
    y_scan = bp.relative_list_scan(grid_scan_det_list, motor_y, [dy, -dy])
    total_relative_scan = bp.pchian(x_scan, y_scan)
    yield from bp.outer_product_scan(detector_list, (motor_x, x0, xf,
                                     num_x, motor_y, y0, y_f, num_y,
                                     False), per_step=total_relative_scan)
