# Part 1: Find the number of legal combinations for the password, given the known restrictions.

# use these parameters to control for which parts of the exercise the solution should be computed
BRUTE_FORCE_PART_1 = True
BRUTE_FORCE_PART_2 = True
PRINT_NUMBERS = False # prints all the numbers that mach the criteria, rather than just counting them

lower = 284639
upper = 748759  # inclusive?

test_numbers = [
    111111,
    223450,
    123789,
    20332,
    444444, # this one meets all criteria
    123099,
    987654321,
    9999999,
    9999989,
]

test_cases = [
    # number, expected evaluation
    (111111, True),
    (223450, False),
    (123789, False),
]

# record guesses for part 1
previous_answers_P1 = [
    1014, # too high
    1013, # too high
    895, # correct!
]

# record guesses for part 2
previous_answers_P2 = [
    591, # ??
]

# build functions that restrict a number based on a criterium
# a) digit length
def has_exact_digits(num: int, n: int = 6) -> bool:
    return len(str(num)) == n

print("### digit count ###")
for num in (lower, upper): print(f"{num} has 6 digits: {has_exact_digits(num)}")

# b) is in range of puzzle input
def is_in_range(num: int, lower: int = lower, upper: int = upper) -> bool:
    return lower <= num <= upper

print("\n### range test ###")
for num in (lower-1, lower, upper, upper+1): print(f"{num} is in range: {is_in_range(num)}")

# c) 2 adjacent digits are the same
def has_2_repeating_digits(num: int) -> bool:
    repeating = False
    if (digits:= len(as_string := str(num))) > 1:
        index = 0
        while index < digits - 1:
            if as_string[index] == as_string[index+1]:
                repeating = True
                break
            index += 1
    return repeating

print("\n### repeating digits ###")
for num in test_numbers: print(f"{num} has 2 repeating digits: {has_2_repeating_digits(num)}")

# d) from left to right, the digits never decrease
def adjacent_digits_never_decrease(num: int) -> bool:
    as_string = str(num)
    if len(as_string) <= 1:
        return False
    decreasing = all(int(as_string[i]) <= int(as_string[i+1]) for i in range(0, len(as_string)-1))
    return decreasing

print("\n### successively decreasing digits ###")
for num in test_numbers: print(f"{num}'s digits never increase from left to right: {adjacent_digits_never_decrease(num)}")

# e) evaluate all criteria at once
criteria = (
    has_exact_digits,
    is_in_range,
    has_2_repeating_digits,
    adjacent_digits_never_decrease
)

def passes_all(num: int, checks) -> bool:
    met = all(check(num) for check in checks)
    return met

print("\n### evaluate all criteria at once ###")
for t in test_numbers:
    print(f"\n{t}:")
    for criterium in criteria:
        print(f"{criterium.__name__}: {criterium(t)}")
    print(f"accepted: {passes_all(t, criteria)}")

# f) brute force puzzle input range
if BRUTE_FORCE_PART_1:
    print("\n### numbers that meet all criteria for part 1###")
    matches = [candidate for candidate in range(lower, upper+1) if passes_all(candidate, criteria)]
    if PRINT_NUMBERS:
        for match in matches: print(match)
    print(f"Matches for criteria of part 1: {len(matches)}")

# g) there's at least 1 group of exactly 2 repeating digits
part_2_tests = [
    112233,
    123444,
    111122,
]

def has_isolated_twin_digit(num: int) -> bool:
    # string must have at least 2 characters
    if not len(as_string := str(num)) > 1:
        return False

    isolated_repeat = False
    index = 0
    while index < len(as_string) - 1:
        before = index-1 < 0 or as_string[index-1] != as_string[index]
        middle = as_string[index] == as_string[index+1]
        after = index+2 == len(as_string) or as_string[index+2] != as_string[index]
        isolated_repeat = before and middle and after
        if isolated_repeat: break
        index += 1
    return isolated_repeat

print("\n### isolated twin digit ###")
for num in part_2_tests + test_numbers:
    print(f"{num} has isolated twin digits: {has_isolated_twin_digit(num)}")

extended_criteria = (
    has_exact_digits,
    is_in_range,
    has_isolated_twin_digit,
    adjacent_digits_never_decrease
)

# h) brute force solution to part 2
if BRUTE_FORCE_PART_2:
    print("\n### numbers that meet all criteria for part 2 ###")
    winners = [candidate for candidate in range(lower, upper+1) if passes_all(candidate, extended_criteria)]
    if PRINT_NUMBERS:
        for w in winners: print(w)
    print(f"Matches for extended criteria of part 2: {len(winners)}")
