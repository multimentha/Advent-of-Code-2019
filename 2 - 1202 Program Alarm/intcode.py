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

        self.input = list(data)
        self.output = None
        self.valid = None


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
    puzzle_input[1] = 12
    puzzle_input[2] = 2

    # load program and run it
    program = Program(puzzle_input)
    program.run()

    # analyze output
    solution = program.output[0]
    print(f"After running the program, this value is left at position 0:\n{solution}")
