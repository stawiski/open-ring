from typing import List
import math

# Assume all resistance is in kOhm


def calculate_vout(r1: float, r2: float) -> float:
    return ((r1 + r2) / r2) * 1.23


def calculate_vout_dac(r1: float, r2: float, r3: float, dac_resistors_enabled: List[float]) -> float:
    r_dac_parallel = math.inf

    if len(dac_resistors_enabled) > 0:
        denominator = 0

        for r in dac_resistors_enabled:
            if r < 0.001:
                r = 0.001
            denominator += 1.0/r

        r_dac_parallel = 1.0/denominator

    return calculate_vout(r1, 1 / ((1/r2) + 1/(r3 + r_dac_parallel)))


print("R1 = 117 kOhm, R2 = 17 kOhm, Vout =",
      round(calculate_vout(117, 15), 2), "V")
print("R1 = 117 kOhm, R2 = 8 kOhm, Vout =",
      round(calculate_vout(117, 8), 2), "V")

print("DAC at", round(calculate_vout_dac(117, 15, 20, []), 2), "V")
print("DAC at", round(calculate_vout_dac(117, 15, 20, [8, 10]), 2), "V")
print("DAC at", round(calculate_vout_dac(117, 15, 15, [0]), 2), "V")
print("DAC at", round(calculate_vout_dac(117, 15, 15, [1]), 2), "V")
