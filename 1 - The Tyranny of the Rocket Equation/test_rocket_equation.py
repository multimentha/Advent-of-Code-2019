# test the fuel calculation
# these samples are given as samples of correct input/output on the webpage

from rocket_equation import *

samples = (
    # (module weight, fuel required for module, total fuel required (including fuel itself))
    (12, 2, 2),
    (14, 2, 2),
    (1969, 654, 966),
    (100756, 33583, 50346),
)


total = 2 * len(samples)
current = 0
passed = 0; failed = 0

# test simple fuel requirements
for sample in samples:
    mass = sample[0]
    if (fuel :=  find_fuel_req(mass)) == (expected := sample[1]):
        passed += 1
    else:
        failed += 1
        print(f"failed test {total + 1}.\n  input: {mass}\n  output: {fuel}\n  expected: {expected}")
    current += 1

# test recursive fuel requirements
for sample in samples:
    mass = sample[0]
    expected = sample[2]
    if (recursive_fuel := find_fuel_req_recur(mass)) == expected:
        passed += 1
    else:
        failed += 1
        details = f"""failed test {current}:\n  input: {mass}\n  output: {recursive_fuel}\n  expected: {expected}"""
        print(details)
    current += 1

summary = f"""
test case summary:
  {total = }
  {passed = }
  {failed = }
"""
print(summary)
