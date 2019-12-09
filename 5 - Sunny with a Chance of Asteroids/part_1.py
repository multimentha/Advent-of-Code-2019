"""Run the diagnostic test interactively, so that you can see every single instruction at work."""

from diagnostic_program import program as program

VERBOSE = False # display details on how instructions are processed
INTERACTIVE = False # set to true to step through the program instruction by instruction

# keep track of previous guesses
guesses = [
    15259545, # the correct solution
]

# each time the progams asks you to input a number, provide one of these, in order
inputs = [
    1, # the 1st and only input for part 1
]

instruction_pointer = 0
instructions_processed = 0
output = []
print("======== evaluating program ========")
if INTERACTIVE:
    print("INTERACTIVE mode enabled, will step through instruction by instruction.")
else:
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
    elif opcode[-1] == "1":
        # add and store
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
    elif opcode[-1] == "2":
        # multiply and store
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
    elif opcode[-1] == "3":
        # store input at address
        store_at = program[instruction_pointer+1]
        if VERBOSE: print(f"{store_at = }")
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
    elif opcode[-1] == "4":
        # output argument
        parameter_mode = opcode.zfill(3)[0]
        if VERBOSE: print(f"{parameter_mode = }")
        if parameter_mode == "0":
            value = program[program[instruction_pointer+1]]
        else:
            value = program[instruction_pointer+1]
        output.append(value)
        if VERBOSE: print(f"output: {value}")
        instruction_pointer += 2
    else:
        print(f"Encountered illegal opcode ({opcode}: exiting!)")
        break

print("======== output summary ========")
# If all outputs were zero except the diagnostic code, the diagnostic program ran successfully.
print(f"instructions processed = {instructions_processed}")
print(f"{output = }")
diagnostic_code = output[-1] if len(output) > 0 else None
# ensure that all except the last status number are 0
# (if this is not the case, the evaluation routine is faulty)
if output:
    assert all(status == 0 for status in output[:-1])
print(f"{diagnostic_code = }")
