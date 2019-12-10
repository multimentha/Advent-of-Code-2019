# - Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
test_1 = 3,9,8,9,10,9,4,9,99,-1,8
test_1_inputs = [
    # input, expected output
    ((7, ), [0, ]),
    ((8, ), [1, ]),
    ((9, ), [0, ]),
]

# Using immediate mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
test_2 = 3,3,1108,-1,8,3,4,3,99
test_2_inputs = [
    # input, expected output
    ((7, ), [0, ]),
    ((8, ), [1, ]),
    ((9, ), [0, ]),
]

# Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
test_3 = 3,9,7,9,10,9,4,9,99,-1,8
test_3_inputs = [
    # input, expected output
    ((7, ), [1, ]),
    ((8, ), [0, ]),
    ((9, ), [0, ]),
]

# Using immediate mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
test_4 = 3,3,1107,-1,8,3,4,3,99
test_4_inputs = [
    # input, expected output
    ((7, ), [1, ]),
    ((8, ), [0, ]),
    ((9, ), [0, ]),
]

# Here are some jump tests that take an input, then output 0 if the input was zero or 1 if the input was non-zero
test_5 = 3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 # (using position mode)
test_5_inputs = [
    ((0, ), [0, ]),
    ((1, ), [1, ]),
    ((-1, ), [1, ]),
    ((800, ), [1, ]),
]
test_6 = 3,3,1105,-1,9,1101,0,0,12,4,12,99,1 # (using immediate mode)
test_6_inputs = [
    ((0, ), [0, ]),
    ((1, ), [1, ]),
    ((-1, ), [1, ]),
    ((800, ), [1, ]),
]

# This example program uses an input instruction to ask for a single number. The program will then
# - output 999 if the input value is below 8,
# - output 1000 if the input value is equal to 8 or
# - output 1001 if the input value is greater than 8.
test_7 = 3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
test_7_inputs = [
    ((7, ), [999, ]),
    ((8, ), [1000, ]),
    ((9, ), [1001, ]),
]
