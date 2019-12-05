# keep track of answers that were submitted but rejected
previous_incorrects = [1, ]

class Program():
    """Loads, stores and executes an intcode program."""
    

    @classmethod
    def format_for_display(self, data: list, pos: int = 0) -> str:
        """Return a human readable representation of an intcode program.
        
        Displays from beginning to end by default, but can start from a specific position if pos is specified."""

        rep = ""
        last = len(data)
        while pos <= last:
            rep += str(pos) + "\n"
            tup = data[pos:min(pos+4, last)]
            rep += ", ".join((str(c) for c in tup)) + "\n"
            pos += 4

        return rep


    def __init__(self, data: list or tuple or str, pointer = 0):
        """Initializes a new intcode program from an iterable that holds integers."""

        self.input_original = list(data)
        self.input = self.input_original[:]
        self.output = None
        self.valid = None


    def reset(self):
        self.input = self.input_original[:]


    def run(self, pointer: int = 0) -> list:
        """Run the program. If no starting intruction is specified, start from intcode 0.

        Returns the altered program (all the intcodes) as a result."""
        
        # operate on a temporary copy of the input data
        working_data = self.input[:]
        # assume the program works until we encounter an error
        self.valid = True

        def advance(pointer: int, program: list = working_data, steps = 4):
            """Advance the instruction pointer by this much."""
            return min(pointer + 4, len(working_data)-1)

        # evaluate program
        while (instr := working_data[pointer]) != 99:
            if instr not in (1, 2):
                self.valid = False
                raise Exception(f"The execution of the intcode program was halted because an illegal instruction ({instr} @ {pointer}) was encountered.")
            elif instr == 1:
                try:
                    working_data[working_data[pointer+3]] = working_data[working_data[pointer+1]] + working_data[working_data[pointer+2]]
                except IndexError as ie:
                    self.valid = False
                    # raise ie
                    break
                else:
                    pointer = advance(pointer)
            elif instr == 2:
                try:
                    working_data[working_data[pointer+3]] = working_data[working_data[pointer+1]] * working_data[working_data[pointer+2]]
                except IndexError as ie:
                    self.valid = False
                    # raise ie
                    break
                else:
                    pointer = advance(pointer)
        self.output = working_data
        return self.output


    def render_input(self):
        """Display the input to the program."""

        return self.format_for_display(self.input)   


    def render_output(self):
        """Display the output of the program."""

        return self.format_for_display(self.output)


if __name__ == "__main__":
    # adjust input to mimic the program which crashed the ship
    with open(file_path := "input/part-1.txt") as fh:
        content = fh.read()
        puzzle_input = [int(c.strip()) for c in content.split(",")]
    modified = puzzle_input[:]
    modified[1] = 12
    modified[2] = 2

    # load program and run it
    program = Program(modified)
    program.run()

    # analyze output
    solution = program.output[0]
    print("--- Part 1 ---")
    print(f"After running the program, this value is left at position 0:\n{solution}")

    # part 2
    target_value = 19690720  # found in address 0 after the program has run
    addr_target = 0
    addr_noun = 1
    addr_verb = 2
    lower, upper = 0, 99  # range for inputs, inclusive
    machine = Program(puzzle_input)
    # brute force inputs until we find the desired target value
    found = False
    for n in range(lower, upper+1):
        for v in range(lower, upper+1):
            machine.reset()
            machine.input[addr_noun] = n
            machine.input[addr_verb] = v
            machine.run()
            if machine.output[addr_target] == target_value:
                found = True
                answer = 100 * n + v
            if found: break
        if found: break
    # concatenate noun and verb into single number
    print("\n--- Part 2 ---")
    if found:
        print(f"This combination of noun, verb produced the undesirable outcome of {target_value} at address {addr_target}:\n{answer}")
    else:
        print(f"Could not find any combination of noun and verb to produce {target_value} at address {addr_target}.")
