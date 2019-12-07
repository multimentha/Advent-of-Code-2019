import pprint as pp
from crossed_wires import *

test_file_paths = (
    "input/example_1.txt",
    "input/example_2.txt",
    "input/example_3.txt",
)
tested = 0; passed = 0; failed = 0
# patch field symbol representations (ASCII chars)
print(f"{PatchField.symbols = }")

for t in test_file_paths:
    p = PatchField(t)
    print(f"{p.source_file = }")
    for i, w in enumerate(p.wires):
        print(f"wire {i+1}:\n{w}")
    print(f"{p.expected_closest_manhattan = }")
    print(f"{p.expected_fewest_combined_steps = }")

    # individual enclosures
    print("\nindidividual enclosures")
    for cchain in p.coordinate_chains:
        x_min, x_max, y_min, y_max = p.find_enclosure((cchain, ))
        print(f"enclosure:\n{x_min = }\n{x_max = }\n{y_min = }\n{y_max = }")
    x_min, x_max, y_min, y_max = p.find_enclosure(p.coordinate_chains)
    
    # combined enclosure
    print(f"\nCombined enclosure:\n{x_min = }\n{x_max = }\n{y_min = }\n{y_max = }")
    empty_field = p.prepare_field(x_min, x_max, y_min, y_max, padding = 0)
    height = len(empty_field); width = len(empty_field[0])
    print(f"{height = }, {width = }")

    # common bends
    print("Common bends for 1st and 2nd wire (assuming central port = 0, 0):")
    if not p.common_bends:
        print("No common bends.")
    else:
        for cb in p.common_bends: print(cb)
    
    # lookup map
    print(f"{p.lookup_map['default value check'] =}")
    # for k, v in p.lookup_map.items():
    #     print(f"{k}: {v}")

    # crossovers
    print("\ncrossovers:")
    for co in p.crossovers: print(co)

    # only the closest crossovers
    print("\nclosest crossovers:")
    for c in p.closest_crossovers: print(c)

    # check computed closest Manhattan distance against expected result
    if p.expected_closest_manhattan == p.closest_manhattan:
        print("test case passed")
        passed +=1
    else:
        print("test case failed")
        failed +=1
    tested +=1

    # find crossovers with lowest combined signal delay
    print("\ncrossovers with lowest combined signal delays")
    print(f"{p.lowest_signal_delay_crossovers = }")
    print(f"expected: {p.expected_fewest_combined_steps}")
    if p.lowest_signal_delay_crossovers[0][1] == p.expected_fewest_combined_steps:
        passed += 1
    else:
        failed += 1
    tested += 1

summary = f"""summary:
  {tested = }
  {passed = }
  {failed = }"""
print(summary)
