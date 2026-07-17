# Oklch originally introduced by Björn Ottosson starting from 2020
# https://bottosson.github.io/posts/oklab/

import math


def byte_val_to_float(val: int):
    return float(val) / 256

def transform_nonlinear(val:float):
    if val >= 0.0031308:
        non_lin = 1.055 * val ** (1.0 / 2.4) - 0.055
    else:
        non_lin =  12.92 * val
    return non_lin

def transform_linear(val: float):
    if val >= 0.04045:
        lin = ((val + 0.055) / 1.055) ** 2.4
    else:
        lin = val / 12.92
    return lin

def srgb_to_linear(srgb: tuple[int, int, int]):
    return (
        transform_linear(byte_val_to_float(srgb[0])),
        transform_linear(byte_val_to_float(srgb[1])),
        transform_linear(byte_val_to_float(srgb[2]))
    )

def linear_srgb_to_oklab(linear_srgb: tuple[float, float, float]):
    r = linear_srgb[0]
    g = linear_srgb[1]
    b = linear_srgb[2]
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_cbrt = l ** (1.0 / 3.0)
    m_cbrt = m ** (1.0 / 3.0)
    s_cbrt = s ** (1.0 / 3.0)
    oklab = (
        0.2104542553 * l_cbrt + 0.7936177850 * m_cbrt - 0.0040720468 * s_cbrt,
        1.9779984951 * l_cbrt - 2.4285922050 * m_cbrt + 0.4505937099 * s_cbrt,
        0.0259040371 * l_cbrt + 0.7827717662 * m_cbrt - 0.8086757660 * s_cbrt,
    )
    return oklab

def lab_to_lch(lab: tuple[float, float, float]):
    l = lab[0]
    a = lab[1]
    b = lab[2]
    c = (a ** 2 + b ** 2) ** 0.5
    h_radian = math.atan2(b, a)
    h = math.degrees(h_radian)
    if h < 0:
        h += 360
    # When testing, found also values with 360. Therefore added, to be truely periodical:
    if h > 359.5:
        h = 0
    return l, c, h

def srgb_to_oklch(srgb: tuple[int, int, int]):
    lin = srgb_to_linear(srgb)
    oklab = linear_srgb_to_oklab(lin)
    oklch = lab_to_lch(oklab)
    return oklch

