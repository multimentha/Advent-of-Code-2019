# Goal 1 : find the total fuel required for take off.
# The total fuel is the sum of fuel required for each module.
#
# previous attempts:
# 9916056 --> too high
# 3305115 --> correct

# Goal 2: find the total fuel, but this time consider that the fuel itself also weighs something and requires further fuel.
# previous attempts:
# 


import math
import pprint as pp

LOG = {
    "input_length": False,
    "input": False,
    "fuel recursive": False,
}


def find_fuel_req(mass: int or float) -> int:
    """Calculates the fuel necessary for a module given its weight. #**Description**
    
    >>> find_fuel_req(12) #**Example**
    2
    >> find_fuel_req(100756)
    33583
    """
    fuel_req = math.floor(mass/3) - 2
    return fuel_req


def find_fuel_req_recur(mass: int or float) -> int:
    """Calculates the fuel necessary for a module, including the weight of the fuel itself. #**Description**

    >>> find_fuel_req_recur(14) #**Example**
    0
    >>> find_fuel_req_recur(1969)
    966
    """
    fuel_req = 0
    while (mass := find_fuel_req(mass)) >= 0:
        if LOG["fuel recursive"]: print(f"{fuel_req = }")
        fuel_req += mass
    return fuel_req


if __name__ == "__main__":
    data_file_path: str = "input/input.txt"
    with open(data_file_path, "r")as f:
        lines = f.readlines()
        module_weights = [float(weight) for weight in lines]

    if LOG["input_length"]: print(f"{len(module_weights) = }")
    if LOG["input"]: pp.pprint(module_weights)

    # compute fuel necessary just for modules (excluding fuel)
    fuel_req_total = sum(find_fuel_req(module_weight) for module_weight in module_weights)
    print(f"simple fuel calculation: {fuel_req_total}")
    
    # compute fuel necessary for modules and fuel itself
    fuel_req_total_recur = sum(tuple(find_fuel_req_recur(module_weight) for module_weight in module_weights))
    assert fuel_req_total_recur >= fuel_req_total, "Fuel necessary to carry modules and fuel must be a greater quantity then the fuel necessary for the modules alone."
    print(f"recursive fuel calculation: {fuel_req_total_recur}")
