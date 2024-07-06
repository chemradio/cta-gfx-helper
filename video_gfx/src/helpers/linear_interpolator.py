# helper interpolator
def linear_interpolation(d, x):
    """
    Linear interpolation function
    :param d: list of 2 points
    :param x: value to interpolate
    :return: interpolated value
    """

    output = d[0][1] + (x - d[0][0]) * ((d[1][1] - d[0][1]) / (d[1][0] - d[0][0]))
    return output
