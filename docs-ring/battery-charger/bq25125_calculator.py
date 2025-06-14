from curses.ascii import isdigit
from pprint import pprint
from typing import Any

vhot = {'min': 0.145, 'typ': 0.15, 'max': 0.152}
vwarm = {'min': 0.201, 'typ': 0.205, 'max': 0.208}
vcool = {'min': 0.354, 'typ': 0.36, 'max': 0.364}
vcold = {'min': 0.393, 'typ': 0.398, 'max': 0.402}


def calculate_rlo(vin, rcold, rhot, vcold, vhot):
    return (vin * rcold * rhot * ((1 / vcold) - (1 / vhot)))/(rhot * ((vin / vhot) - 1) - rcold * ((vin / vcold) - 1))


def calculate_rhi(vin, rcold, vcold, rlo):
    return ((vin / vcold) - 1)/((1 / rlo) + (1 / rcold))


def calculate_rcool(rlo, rhi, vcool):
    return (rlo * rhi * vcool)/(rlo - ((rlo * vcool) - (rhi * vcool)))


def calculate_rwarm(rlo, rhi, vwarm):
    return (rlo * rhi * vwarm)/(rlo - ((rlo * vwarm) - (rhi * vwarm)))


def ohm_to_string(r):
    decades = ['Ohm', 'kOhm', 'MOhm']
    d = None

    for dec in decades:
        d = dec
        if r > 1000:
            r = round(r) / 1000
        else:
            break

    if (r > 100):
        return "{:.0f} {:s}".format(r, d)
    elif (r > 10):
        return "{:.1f} {:s}".format(r, d)
    else:
        return "{:.2f} {:s}".format(r, d)


def calculate_ts_voltage(vin, rhi, rlo, rntc):
    rlo_rntc_parallel = 1.0 / ((1.0 / rlo) + (1.0 / rntc))
    return vin * rlo_rntc_parallel / (rhi + rlo_rntc_parallel)


def is_float(element: Any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


def string_to_resistance(string):
    if is_float(string):
        return float(string)
    elif isinstance(string, str):
        if string[-1] == "k":
            value = string[:-1]
            if is_float(value):
                return float(value)*1000
        elif string[-1] == "M":
            value = string[:-1]
            if is_float(value):
                return float(value)*1000000

    return ValueError("Could not convert string to resistance")


def pretty_calculate(vin, rcold, rhot):
    rlo = calculate_rlo(vin, rcold, rhot, vin*vcold['typ'], vin*vhot['typ'])
    rhi = calculate_rhi(vin, rcold, vin*vcold['typ'], rlo)
    # rcool = calculate_rcool(rlo, rhi, vin*vcool['typ'])
    # rwarm = calculate_rwarm(rlo, rhi, vin*vwarm['typ'])
    print('Vin = {:.2f} V'.format(vin))
    print('Rlo = ' + ohm_to_string(rlo))
    print('Rhi = ' + ohm_to_string(rhi))
    # print('rcool = ' + ohm_to_string(calc['rcool']))
    # print('rwarm = ' + ohm_to_string(calc['rwarm']))
    print('')
    return rlo, rhi


def ntc_get(temperature):
    raw = [
        #     °C   min   nom   max (in kOhms)
        [-40, 4151, 4251, 4353],
        [-39, 3871, 3962, 4056],
        [-38, 3611, 3695, 3781],
        [-37, 3370, 3447, 3526],
        [-36, 3147, 3218, 3290],
        [-35, 2939, 3005, 3072],
        [-34, 2747, 2807, 2869],
        [-33, 2569, 2624, 2681],
        [-32, 2403, 2454, 2506],
        [-31, 2249, 2296, 2344],
        [-30, 2106, 2149, 2193],
        [-29, 1972, 2012, 2053],
        [-28, 1848, 1885, 1923],
        [-27, 1733, 1767, 1801],
        [-26, 1625, 1656, 1688],
        [-25, 1525, 1554, 1583],
        [-24, 1431, 1458, 1485],
        [-23, 1344, 1369, 1394],
        [-22, 1263, 1286, 1309],
        [-21, 1187, 1208, 1229],
        [-20, 1116, 1135, 1155],
        [-19, 1050, 1068, 1086],
        [-18, 987.7, 1004, 1021],
        [-17, 929.7, 945, 960.4],
        [-16, 875.5, 889.6, 903.9],
        [-15, 824.8, 837.8, 851],
        [-14, 777.3, 789.3, 801.5],
        [-13, 732.8, 743.9, 755.1],
        [-12, 691.1, 701.3, 711.7],
        [-11, 652, 661.5, 671.1],
        [-10, 615.3, 624.1, 633],
        [-9, 580.9, 589, 597.3],
        [-8, 548.6, 556.2, 563.7],
        [-7, 518.3, 525.3, 532.3],
        [-6, 489.9, 496.3, 502.8],
        [-5, 463.2, 469.1, 475.1],
        [-4, 438, 443.5, 449.1],
        [-3, 414.4, 419.5, 424.6],
        [-2, 392.2, 396.9, 401.6],
        [-1, 371.3, 375.6, 380],
        [0, 351.6, 355.6, 359.7],
        [1, 333.1, 336.8, 340.6],
        [2, 315.7, 319.1, 322.5],
        [3, 299.2, 302.4, 305.6],
        [4, 283.7, 286.7, 289.6],
        [5, 269.1, 271.8, 274.6],
        [6, 255.3, 257.8, 260.4],
        [7, 242.4, 244.7, 247],
        [8, 230.1, 232.2, 234.4],
        [9, 218.5, 220.5, 222.5],
        [10, 207.6, 209.4, 211.2],
        [11, 197.3, 198.9, 200.6],
        [12, 187.5, 189, 190.6],
        [13, 178.3, 179.7, 181.1],
        [14, 169.6, 170.9, 172.2],
        [15, 161.3, 162.5, 163.7],
        [16, 153.5, 154.6, 155.7],
        [17, 146.1, 147.2, 148.2],
        [18, 139.1, 140.1, 141],
        [19, 132.5, 133.4, 134.2],
        [20, 126.3, 127, 127.8],
        [21, 120.3, 121, 121.8],
        [22, 114.7, 115.4, 116],
        [23, 109.4, 110, 110.6],
        [24, 104.3, 104.8, 105.4],
        [25, 99.5, 100, 100.5],
        [26, 94.9, 95.4, 95.9],
        [27, 90.54, 91.04, 91.54],
        [28, 86.4, 86.9, 87.39],
        [29, 82.47, 82.97, 83.46],
        [30, 78.74, 79.23, 79.72],
        [31, 75.2, 75.69, 76.17],
        [32, 71.84, 72.32, 72.8],
        [33, 68.64, 69.12, 69.59],
        [34, 65.6, 66.07, 66.54],
        [35, 62.72, 63.18, 63.64],
        [36, 59.97, 60.42, 60.88],
        [37, 57.36, 57.81, 58.25],
        [38, 54.87, 55.31, 55.76],
        [39, 52.51, 52.94, 53.38],
        [40, 50.26, 50.68, 51.11],
        [41, 48.12, 48.53, 48.95],
        [42, 46.08, 46.49, 46.9],
        [43, 44.13, 44.53, 44.94],
        [44, 42.28, 42.67, 43.07],
        [45, 40.52, 40.9, 41.29],
        [46, 38.83, 39.21, 39.59],
        [47, 37.23, 37.6, 37.97],
        [48, 35.7, 36.06, 36.43],
        [49, 34.24, 34.6, 34.95],
        [50, 32.85, 33.19, 33.55],
        [51, 31.52, 31.86, 32.2],
        [52, 30.25, 30.58, 30.92],
        [53, 29.04, 29.36, 29.69],
        [54, 27.88, 28.2, 28.52],
        [55, 26.78, 27.09, 27.4],
        [56, 25.72, 26.03, 26.33],
        [57, 24.71, 25.01, 25.31],
        [58, 23.75, 24.04, 24.33],
        [59, 22.83, 23.11, 23.4],
        [60, 21.95, 22.22, 22.5],
        [61, 21.1, 21.37, 21.65],
        [62, 20.3, 20.56, 20.83],
        [63, 19.52, 19.78, 20.04],
        [64, 18.78, 19.04, 19.29],
        [65, 18.08, 18.32, 18.57],
        [66, 17.4, 17.64, 17.88],
        [67, 16.75, 16.99, 17.22],
        [68, 16.13, 16.36, 16.59],
        [69, 15.54, 15.76, 15.99],
        [70, 14.97, 15.18, 15.4],
        [71, 14.42, 14.63, 14.85],
        [72, 13.9, 14.1, 14.31],
        [73, 13.39, 13.6, 13.8],
        [74, 12.91, 13.11, 13.31],
        [75, 12.45, 12.64, 12.84],
        [76, 12.01, 12.19, 12.39],
        [77, 11.58, 11.76, 11.95],
        [78, 11.17, 11.35, 11.53],
        [79, 10.78, 10.96, 11.13],
        [80, 10.41, 10.58, 10.75],
        [81, 10.04, 10.21, 10.38],
        [82, 9.697, 9.859, 10.02],
        [83, 9.364, 9.522, 9.683],
        [84, 9.044, 9.198, 9.355],
        [85, 8.736, 8.887, 9.04],
        [86, 8.44, 8.587, 8.737],
        [87, 8.156, 8.299, 8.445],
        [88, 7.882, 8.022, 8.165],
        [89, 7.619, 7.756, 7.895],
        [90, 7.367, 7.5, 7.636],
        [91, 7.123, 7.254, 7.386],
        [92, 6.889, 7.016, 7.146],
        [93, 6.664, 6.788, 6.914],
        [94, 6.447, 6.568, 6.692],
        [95, 6.238, 6.357, 6.477],
        [96, 6.038, 6.153, 6.271],
        [97, 5.844, 5.957, 6.072],
        [98, 5.658, 5.768, 5.88],
        [99, 5.478, 5.586, 5.695],
        [100, 5.305, 5.41, 5.517],
        [101, 5.138, 5.241, 5.345],
        [102, 4.978, 5.078, 5.18],
        [103, 4.823, 4.921, 5.02],
        [104, 4.674, 4.769, 4.866],
        [105, 4.53, 4.623, 4.718],
        [106, 4.391, 4.482, 4.575],
        [107, 4.257, 4.346, 4.437],
        [108, 4.128, 4.215, 4.303],
        [109, 4.003, 4.088, 4.175],
        [110, 3.883, 3.966, 4.05],
        [111, 3.767, 3.848, 3.931],
        [112, 3.655, 3.734, 3.815],
        [113, 3.546, 3.624, 3.703],
        [114, 3.442, 3.518, 3.595],
        [115, 3.341, 3.415, 3.491],
        [116, 3.244, 3.316, 3.39],
        [117, 3.149, 3.22, 3.292],
        [118, 3.059, 3.128, 3.198],
        [119, 2.971, 3.038, 3.107],
        [120, 2.886, 2.952, 3.019],
        [121, 2.804, 2.868, 2.934],
        [122, 2.724, 2.787, 2.852],
        [123, 2.647, 2.709, 2.772],
        [124, 2.573, 2.634, 2.695],
        [125, 2.501, 2.561, 2.621]
    ]

    for row in raw:
        if row[0] == temperature:
            return row[2]*1000

    raise RuntimeError("Temperature not found")


def pretty_ts_voltage(vin, rhi, rlo, rntc):
    rhi = string_to_resistance(rhi)
    rlo = string_to_resistance(rlo)
    rntc = string_to_resistance(rntc)
    print('Vin = {:.2f} V'.format(vin))
    print('Rlo = ' + ohm_to_string(rlo))
    print('Rhi = ' + ohm_to_string(rhi))
    print('Rntc = ' + ohm_to_string(rntc))
    vts = calculate_ts_voltage(vin, rhi, rlo, rntc)
    vts_string = "normal"
    if vts < vin*vhot['typ']:
        vts_string = "too hot"
    elif vts > vin*vcold['typ']:
        vts_string = "too cold"
    elif vin*vcool['typ'] < vts < vin*vcold['typ']:
        vts_string = "cool, charge current reduced to 50%"
    elif vin*vhot['typ'] < vts < vin*vwarm['typ']:
        vts_string = "warm, charge voltage reduced by 140mV"

    print('Vts = {:.2f} V [{:s}]'.format(vts, vts_string))
    print('')


# GREPOW battery has <10°C, 45°C> charge temperature range

# For our NTC
# At temp 10°C min: 207.6k, nom: 209.4k, max: 211.2k
# At temp 11°C min: 197.3k, nom: 198.9k, max: 200.6k
# At temp 39°C min: 52.51k, nom: 52.94k, max: 53.38k
# At temp 40°C min: 50.26k, nom: 50.68k, max: 51.11k

# Picked NTC values for 11°C and 39°C for safety margin

pretty_calculate(5.1, 200600, 50260)
pretty_calculate(5.0, 200600, 50260)
pretty_calculate(4.9, 200600, 50260)

# Now we need to choose the values of resistors that can be manufacured
# Rlo = 2.2MOhm 1%
# Rhi = 280kOhm 1%

temp = 0
while temp <= 50:
    print(f" === Temperature: {temp}°C ===")
    pretty_ts_voltage(5.0, "280k", "2.2M", ntc_get(temp))
    temp = temp + 1
