"""Run the diagnostic test interactively, so that you can see every single instruction at work."""

import itertools

VERBOSE = False # display details on how instructions are processed
INTERACTIVE = False # set to true to step through the program instruction by instruction

# keep track of previous guesses
guesses = [
    ("5440230", (0, 4, 1, 2, 3)), # too high
    ("04123", (None)), # too low
]
# these integers represent the different phase modes
PHASE_MODES = [0, 1, 2, 3, 4]

def evaluate(program: list or tuple, inputs = []) -> list:
    program = list(program)
    instruction_pointer = 0
    input_pointer = 0
    instructions_processed = 0
    output = []
    if INTERACTIVE:
        print("======== evaluating program ========")
        print("INTERACTIVE mode enabled, will step through instruction by instruction.")
    elif VERBOSE:
        print("INTERACTIVE mode disabled, will pause only where user input is required.")
    while True:
        instructions_processed += 1
        if INTERACTIVE: input(">>> Enter to evaluate next instruction...")
        opcode = str(program[instruction_pointer])
        if VERBOSE: print(f"next {opcode = }")
        if opcode == "99":
            # halt program
            if VERBOSE: print("Program has ended (opcode 99).")
            break
        elif opcode[-1] == "1": # add and store
            parameter_modes = list(reversed(opcode.zfill(5)[0:3]))
            if VERBOSE: print(f"{parameter_modes = }")
            parameters = program[instruction_pointer+1:instruction_pointer+4]
            if VERBOSE: print(f"{parameters = }")
            if parameter_modes[0] == "0":
                summand1 = program[program[instruction_pointer+1]]
            else:
                summand1 = program[instruction_pointer+1]
            if parameter_modes[1] == "0":
                summand2 = program[program[instruction_pointer+2]]
            else:
                summand2 = program[instruction_pointer+2]
            program[program[instruction_pointer+3]] = summand1 + summand2
            instruction_pointer += 4
        elif opcode[-1] == "2": # multiply and store
            parameter_modes = list(reversed(opcode.zfill(5)[0:3]))
            if VERBOSE: print(f"{parameter_modes = }")
            parameters = program[instruction_pointer+1:instruction_pointer+4]
            if VERBOSE: print(f"{parameters = }")
            if parameter_modes[0] == "0":
                factor1 = program[program[instruction_pointer+1]]
            else:
                factor1 = program[instruction_pointer+1]
            if parameter_modes[1] == "0":
                factor2 = program[program[instruction_pointer+2]]
            else:
                factor2 = program[instruction_pointer+2]
            program[program[instruction_pointer+3]] = factor1 * factor2
            instruction_pointer += 4
        elif opcode[-1] == "3": # store input at address            
            store_at = program[instruction_pointer+1]
            if VERBOSE: print(f"{store_at = }")
            # look whether the supplied input is exhaused yet
            exhausted = input_pointer >= len(inputs)
            if not exhausted:
                integer = inputs[input_pointer]
                input_pointer += 1
            else:
                while True:
                    print(f"Please input parameter to store at adress {store_at}...")
                    integer = input()
                    try:
                        integer = int(integer)
                    except ValueError as ve:
                        print("That's not an integer!")
                    else:
                        break
            program[store_at] = integer
            instruction_pointer += 2
        elif opcode[-1] == "4": # output argument
            parameter_mode = opcode.zfill(3)[0]
            if VERBOSE: print(f"{parameter_mode = }")
            if parameter_mode == "0":
                value = program[program[instruction_pointer+1]]
            else:
                value = program[instruction_pointer+1]
            output.append(value)
            if VERBOSE: print(f"output: {value}")
            instruction_pointer += 2
        elif opcode[-1] == "5": # jump if true
            parameter_modes = list(reversed(opcode.zfill(4)[0:2]))
            if VERBOSE: print(f"{parameter_modes = }")
            # dereference if necessary
            if parameter_modes[0] == "0":
                condition = program[program[instruction_pointer+1]]
            else:
                condition = program[instruction_pointer+1]
            if parameter_modes[1] == "0":
                new_instruction_pointer = program[program[instruction_pointer+2]]
            else:
                new_instruction_pointer = program[instruction_pointer+2]
            if condition != 0:
                # set new instruction pointer
                instruction_pointer = new_instruction_pointer
            else:
                instruction_pointer += 3
        elif opcode[-1] == "6": # jump if false
            parameter_modes = list(reversed(opcode.zfill(4)[0:2]))
            if VERBOSE: print(f"{parameter_modes = }")
            # dereference if necessary
            if parameter_modes[0] == "0":
                condition = program[program[instruction_pointer+1]]
            else:
                condition = program[instruction_pointer+1]
            if parameter_modes[1] == "0":
                new_instruction_pointer = program[program[instruction_pointer+2]]
            else:
                new_instruction_pointer = program[instruction_pointer+2]
            if condition == 0:
                # set new instruction pointer
                instruction_pointer = new_instruction_pointer
            else:
                instruction_pointer += 3
        elif opcode[-1] == "7": # less than comparison
            parameter_modes = tuple(reversed(opcode.zfill(5)[0:3]))
            if VERBOSE: print(f"{parameter_modes}")
            # dereference if necessary
            if parameter_modes[0] == "0":
                c1 = program[program[instruction_pointer+1]]
            else:
                c1 = program[instruction_pointer+1]
            if parameter_modes[1] == "0":
                c2 = program[program[instruction_pointer+2]]
            else:
                c2 = program[instruction_pointer+2]
            if c1 < c2:
                result = 1
            else:
                result = 0
            program[program[instruction_pointer+3]] = result
            instruction_pointer += 4
        elif opcode[-1] == "8": # equality comparison
            parameter_modes = tuple(reversed(opcode.zfill(5)[0:3]))
            if VERBOSE: print(f"{parameter_modes}")
            # dereference if necessary
            if parameter_modes[0] == "0":
                c1 = program[program[instruction_pointer+1]]
            else:
                c1 = program[instruction_pointer+1]
            if parameter_modes[1] == "0":
                c2 = program[program[instruction_pointer+2]]
            else:
                c2 = program[instruction_pointer+2]
            if c1 == c2:
                result = 1
            else:
                result = 0
            program[program[instruction_pointer+3]] = result
            instruction_pointer += 4
        else:
            print(f"Encountered illegal opcode ({opcode}: exiting!)")
            break
    if VERBOSE: print(f"instructions processed = {instructions_processed}")
    return output

def find_max_thrust(phases:list, initial_input:int, program:list) -> tuple:
    phase_permutations = [p for p in itertools.permutations(phases)]
    if VERBOSE:
        for phase in phase_permutations: print(phase)

    max_thrust = 0; best_permutation = phase_permutations[0]
    for phases in phase_permutations:
        output = []
        for phase in phases:
            thrust = evaluate(program, [phase, initial_input])[0]
            output.append(thrust)

        # convert a series of output numbers into a single number
        output = int("".join(str(o) for o in output))
        if output > max_thrust:
            # max_thrust = thrust
            max_thrust = output
            best_permutation = phases
    max_thrust = str(max_thrust)
    best_permutation = "".join(str(p) for p in best_permutation)
    return (max_thrust, best_permutation)

# evaluate part 1
if __name__ == "__main__":
    # load program from text file into Python data structure
    with open("input/amplifier_controller_software.txt") as f:
        acs = [int(s) for s in f.readlines()[0].split(",")]
    max_thrust, best_permutation = find_max_thrust(PHASE_MODES, 0, acs)
    print(f"{max_thrust = }\n{best_permutation = }")
