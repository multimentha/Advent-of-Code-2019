from collections import namedtuple

from intcode import *


# define test cases
Intcode_test_case = namedtuple("intcode_test_case", "input output")
test_cases = (
    Intcode_test_case((1,0,0,0,99,), (2,0,0,0,99)),
    Intcode_test_case((2,3,0,3,99,), (2,3,0,6,99)),
    Intcode_test_case((2,4,4,5,99,0,), (2,4,4,5,99,9801,)),
    Intcode_test_case((1,1,1,4,99,5,6,0,99,), (30,1,1,4,2,5,6,0,99,)),
    # Intcode_test_case((4000,1,1,4,99,5,6,0,99,), (30,1,1,4,2,5,6,0,99,)),  ## illegal opcode
)

# run tests
run = 0; passed = 0; failed = 0; crashed = 0
for tcase in test_cases[0:len(test_cases)]:  # adjust number of test cases here
    program = Program(tcase.input)
    assert program.input == list(tcase.input), "program did not load test data correctly"
    try:
        program.run()
    except Exception as e:
        crashed += 1
        failed += 1
        raise e
    if program.output == list(tcase.output):
        passed += 1
    else:
        failed += 1
        print("*"*80)
        print(f"in:\n{program.render_input()}")
        print(f"out:\n{program.render_output()}")
        print(f"expected:\n{Program.format_for_display(tcase.output)}")
    run += 1

# print summary
summary = f"""summary:
  tests run: {run}
  passed: {passed}
  failed: {failed}
  crashed: {crashed}"""
print(summary)
