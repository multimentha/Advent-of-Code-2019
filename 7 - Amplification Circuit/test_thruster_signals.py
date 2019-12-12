from thruster_signals import *
from tests import thruster_tests as tt
from pprint import pprint as pp

total = 0 ; failed = 0; succeeded = 0

for t in tt.test_cases:
    success = True
    print(t["name"])
    max_thrust, best_permutation = find_max_thrust(PHASE_MODES, 0, t["program"])
    if best_permutation != t["phase setting sequence"]:
        success = False
        print(f"received: {best_permutation = }\nexpected: {t['phase setting sequence']}")
    if max_thrust != t["max thruster signal"]:
        success = False
        print(f"received: {max_thrust = }, expected: {t['max thruster signal']}")
    if success:
        print("OK")
        succeeded +=1
    else:
        print("FAIL")
        failed += 1
    print("="*40)
    total += 1

# summary
print(f"test summary: {succeeded}/{total} passed")
