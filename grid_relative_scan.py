import bluesky.plans as bp

# define your motor and detector here
area_det = glbl.area_det
motor_x = glbl.motor_x
motor_y = glbl.motor_y
grid_scan_det_list = [area_det, motor_x, motor_y]
for el in grid_scan_det_list:
    if el is None:
        raise RuntimeError('Required detector is not defined yet')

x0 = motor_x.position
y0 = motor_y.position

# outer_product_scan
def grid_scan(dx, dy, x_f, y_f, num_x, num_y):
    """ grid scan over different wells

    inside each of well, a relative scan will be run. scan starts from 
    current motor position, so be sure you have aligned correctly.

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

    Example:
    --------
    prun(<sample_index>, grid_scan_v2(0.1, 0.1, 3.5, 3.5, 4, 4))
    # a 4 by 4 grid, with dimension 3.5 x 3.5 units in x- and y-
    # direction respectively, and diameter is 0.1*2 unit in each well
    """
    # inside a well, relative scan
    # x direction
    x_scan = bp.relative_list_scan(grid_scan_det_list, motor_x, [dx, 0, -dx])
    # y direction
    y_scan = bp.relative_list_scan(grid_scan_det_list, motor_y, [dy, 0, -dy])
    total_relative_scan = bp.pchain(x_scan, y_scan)
    yield from bp.outer_product_scan(grid_scan_det_list, (motor_x, x0, x_f,
                                     num_x, motor_y, y0, y_f, num_y,
                                     False), per_step=total_relative_scan)
