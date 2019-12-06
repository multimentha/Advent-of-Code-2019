import pprint as pp
from crossed_wires import *

test_file_paths = (
    "input/example_1.txt",
    "input/example_2.txt",
    "input/example_3.txt",
)

tested = 0; passed = 0; failed = 0

print(f"{PatchField.symbols = }")
for t in test_file_paths:
    p = PatchField(t)
    print("="*80)
    print(p.source_file)
    for i, w in enumerate(p.wires):
        print(f"wire {i+1}:\n{w}")
    print(f"{p.expected = }")
    for cchain in p.coordinate_chains:
        x_min, x_max, y_min, y_max = p.find_enclosure((cchain, ))
        print(f"enclosure:\n{x_min = }\n{x_max = }\n{y_min = }\n{y_max = }")
    x_min, x_max, y_min, y_max = p.find_enclosure(p.coordinate_chains)
    print(f"Combined enclosure:\n{x_min = }\n{x_max = }\n{y_min = }\n{y_max = }")
    empty_field = p.prepare_field(x_min, x_max, y_min, y_max, padding = 0)
    height = len(empty_field); width = len(empty_field[0])
    print(f"{height = }, {width = }")
    print("Common bends for 1st and 2nd wire (assuming central port = 0, 0):")
    if not p.common_bends:
        print("No common bends.")
    else:
        for cb in p.common_bends: print(cb)
    
    # lookup map
    # print(f"{p.lookup_map['just_a_test']}") # default value check
    # for k, v in p.lookup_map.items():
    #     print(f"{k}: {v}")

    # crossovers
    print("\ncrossovers:")
    for co in p.crossovers: print(co)

    # only the closest crossovers
    print("\nclosest crossovers:")
    for c in p.closest_crossovers: print(c)

    # check computed closest Manhattan distance against expected result
    if p.expected == p.closest_manhattan:
        print("test case passed")
        passed +=1
    else:
        print("test case failed")
        failed +=1
    tested +=1
