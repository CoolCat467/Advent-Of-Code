#!/usr/bin/env python3  # noqa: EXE001
# Advent of code 2021 day 8 - https://adventofcode.com/2021/day/8

"""Goals:
1) Find special length numbers
2) Find sum of all corrupted numbers.
"""  # noqa: D205

# Programmed by CoolCat467

__title__ = "Advent of Code 2021 - Day 8"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__ver_major__ = 0
__ver_minor__ = 0
__ver_patch__ = 0

SEGMENTS = {
    0: [1, 1, 1, 0, 1, 1, 1],
    1: [0, 0, 1, 0, 0, 1, 0],
    2: [1, 0, 1, 1, 1, 0, 1],
    3: [1, 0, 1, 1, 0, 1, 1],
    4: [0, 1, 1, 1, 0, 1, 0],
    5: [1, 1, 0, 1, 0, 1, 1],
    6: [1, 1, 0, 1, 1, 1, 1],
    7: [1, 0, 1, 0, 0, 1, 0],
    8: [1, 1, 1, 1, 1, 1, 1],
    9: [1, 1, 1, 1, 0, 1, 1],
}
SEG_COUNT_USED = {k: v.count(1) for k, v in SEGMENTS.items()}


def get_sure_conv():
    "Get conversions by length."  # noqa: D300
    data = {}
    for key, value in SEG_COUNT_USED.items():
        if value not in {5, 6}:
            data[value] = key
    return data


SURE_CONV = get_sure_conv()

##def get_seg_patterns():
##    "Get patterns"
##    data = {}
##    for key, value in SEGMENTS.items():
##        pattern = ''
##        for char, there in zip('abcdefg', value):
##            if there:
##                pattern += char
##        data[key] = pattern
##    return data
##
##seg_patterns = get_seg_patterns()


def segment(lettermap, values):
    "Print segment."  # noqa: D300
    lines = []

    def vert(let):
        return " " + let * 4 + " "

    def hori(let1, let2):
        return let1 + " " * 4 + let2

    line_idx = (0, 3, 6)
    last = 0
    lettermap = [lettermap[i] if values[i] else "." for i in range(7)]
    for i in range(7):
        if i in line_idx:
            lines.append(vert(lettermap[i]))
            last = i
        else:
            lines.append(hori(lettermap[last + 1], lettermap[last + 2]))
    print("\n".join(lines))


##def infir_morph(patterns, extra_known=None):
##    "Infir mappings for SEGMENTS"
##    morph = {chr(k+97):[] for k in range(7)}
##    pat_segs = {}
##    for pat in patterns:
##        leng = len(pat)
##        if leng in SURE_CONV:
##            pat_segs[pat] = SURE_CONV[leng]
##        elif pat in extra_known:
##            pat_segs[pat] = extra_known[pat]
####    print(f'{pat_segs=}')
##    rev_k = {v:k for k, v in pat_segs.items()}
####    print(f'{rev_k=}')
##    for k in rev_k:
##        if k == 8:
##            continue
##        for char in rev_k[k]:
##            if morph[char]:
##                morph[char] = [x for x in morph[char] if x in seg_patterns[k] and x != char]
##            else:
##                morph[char] = [x for x in seg_patterns[k] if x != char]
##    for char, values in morph.items():
##        if len(values) < 3:
##            continue
##        ok = values
##        for idx, val in reversed(tuple(enumerate(ok))):
##            if sum(list(morph.values()), []).count(val) > 1:
##                del ok[idx]
##        morph[char] = ok
####    print(morph)
##    return morph
##
def length_conv(digits):
    "Return digits known by length."  # noqa: D300
    know = []
    for digit in digits:
        leng = len(digit)
        if leng in SURE_CONV:
            know.append(SURE_CONV[leng])
        else:
            know.append(digit)
    return know


##
##def find_with_lits(lit_SEGMENTS):
##    lit = []
##    for number, data in SEGMENTS.items():
##        success = True
##        for lit_segment in lit_SEGMENTS:
##            if not data[lit_segment]:
##                success = False
##                break
##        if success and len(lit_SEGMENTS) <= SEG_COUNT_USED[number]:
##            lit.append(number)
##    return lit
##
##def get_possible_from_segments(abs_morphs, patterns):
##    good = {}
##    for key, pos in abs_morphs.items():
##        good[key] = ord(pos)-97
##    possible = {}
##    for pattern in patterns:
##        lit_SEGMENTS = []
##        for char in pattern:
##            if not char in good:
##                continue
##            lit_SEGMENTS.append(good[char])
##        from_lit = find_with_lits(lit_SEGMENTS)
##        pos = []
##        for p in from_lit:
##            if len(pattern) != SEG_COUNT_USED[p]:
##                continue
##            pos.append(p)
##        possible[pattern] = pos
##    return possible
##
##def is_mutation_good(original, new):
##    for key, opos in original.items():
##        npos = new[key]
##        if len(opos) == 1 and len(npos) == 1:
##            if opos[0] == npos[0]:
##                continue
##            return False
##        if len(opos) < len(npos):
##            return False
##        for value in npos:
##            if not value in opos:
##                return False
##    return True
##
##def find_morphs(morphs, patterns, value):
##    """Return:
##0: 1 if value from possible from SEGMENTS
##0: 2 if value from mutation counts
##0: 0 if mutation counts tie, no most possible
##1: If [0] == 1, integer value of `value` pattern
##1: If [0] == 2, most likely integer values of `value` pattern
##1: If [0] == 0,
##
##    """
####    "Return best possible values"
##    good_morphs = {k:v[0] for k, v in morphs.items() if len(v) == 1}
##    possible_morphs = {k:v for k, v in morphs.items() if len(v) > 1}
##
##    possible = get_possible_from_segments(good_morphs, patterns)
##    if len(possible[value]) == 1:
##        return 1, possible[value][0]
##    values_count = {val:0 for val in possible[value]}
##    mutation_values = {}
##
##    for mkey, pos_val in possible_morphs.items():
##        for mutation in pos_val:
##            copy = good_morphs
##            copy[mkey] = mutation
##            mut_pos = get_possible_from_segments(copy, patterns)
##            if is_mutation_good(possible, mut_pos):
##                for val in mut_pos[value]:
##                    values_count[val] += 1
##                    if not val in mutation_values:
##                        mutation_values[val] = []
##                    mutation_values[val].append(mkey+mutation)
##    counts = {v:[] for v in values_count.values()}
##    for val in values_count.values():
##        for num, count in values_count.items():
##            if not num in counts[count]:
##                counts[count].append(num)
##    if not counts:
##        return 0, mutation_values
##    max_count = counts[max(counts)]
####    print(f'{mutation_values=}')
##    if len(max_count) == 1:
##        return 2, max_count[0], mutation_values
##    return 0, mutation_values
##
##def find_value(patterns):
##    "Find value"
##    search = patterns
##    add_pats = {}
##    add_conv = {}
####    print(search)
##    visited = []
##    stop = False
##    while not stop:
##        for idx, value in reversed(tuple(enumerate(search))):
##            morphs = infir_morph(patterns, add_pats)
##            result = find_morphs(morphs, patterns, value)
##            if result[0]:
##                add_pats[value] = result[1]
##                del search[idx]
##                continue
####            else:
####                print(result[1])
##            if not value in visited:
##                visited.append(value)
##                continue
##            stop = True
##        if not search:
##            stop = True
####        if stop and not target in add_pats:
######            print('cannot find target')
######            print(f'{target=}')
######            print(f'{add_pats=}')
####            return add_pats
##    return add_pats
####    return add_pats[target]


# pylint: R0912: Too many branches (18/12)
def get_value(value, patterns):
    "Return value of pattern `value` given all patterns."  # noqa: D300
    numbers = {}
    sixes = []
    fives = []
    for pat in patterns:
        leng = len(pat)
        if leng in SURE_CONV:
            numbers[pat] = SURE_CONV[leng]
        if leng == 6:
            sixes.append(pat)
        if leng == 5:
            fives.append(pat)
    for pat in sixes:
        rev_no = {v: k for k, v in numbers.items()}
        diff = list(set(rev_no[1]).difference(set(pat)))
        if len(diff) == 1 and pat not in numbers:
            numbers[pat] = 6
        diff = list(set(rev_no[4]).difference(set(pat)))
        if len(diff) == 1 and pat not in numbers:
            numbers[pat] = 0
    for pat in sixes:
        if pat not in numbers:
            numbers[pat] = 9
    for pat in fives:
        rev_no = {v: k for k, v in numbers.items()}
        diff = list(set(rev_no[6]).difference(set(pat)))
        if len(diff) == 1 and pat not in numbers:
            numbers[pat] = 5
        diff = list(set(rev_no[9]).difference(set(pat)))
        if len(diff) == 1 and pat not in numbers:
            numbers[pat] = 3
    for pat in fives:
        if pat not in numbers:
            numbers[pat] = 2
    return numbers[value]


def get_values(values, patterns):
    "Return values given patterns."  # noqa: D300
    values = ["".join(sorted(x)) for x in values]
    patterns = ["".join(sorted(x)) for x in patterns]
    all_pats = patterns
    extra_know = {}
    digits = length_conv(values)
    for idx, digit in enumerate(digits):
        if isinstance(digit, str):
            digits[idx] = get_value(digit, all_pats)
            extra_know[digit] = digits[idx]
    return int("".join(map(str, digits)))


def run():
    "Solve problems."  # noqa: D300
    # Read file
    data = []
    with open("adv8.txt", encoding="utf-8") as rfile:
        data = rfile.read().splitlines()
        rfile.close()
        # pylint: C0301: Line too long (866/100)
    ##    data = 'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe\nedbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc\nfgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg\nfbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb\naecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea\nfgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb\ndbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe\nbdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef\negadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb\ngcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce'.splitlines()
    ##    data = ['acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf']
    # Solve 1
    unique = 0
    for value in [line.split(" | ")[1] for line in data]:
        for num in value.split(" "):
            if len(num) in {2, 3, 4, 7}:
                unique += 1
    print(unique)
    # Solve 2
    sum_values = 0
    for line in data:
        patterns, value = line.split(" | ")
        ##        pat_segs = {}
        ##        for pat in patterns.split(' '):
        ##            leng = len(pat)
        ##            if leng in SURE_CONV:
        ##                pat_segs[pat] = SURE_CONV[leng]
        ####        print(pat_segs)
        ##        digits = []
        ##        for pat in value.split(' '):
        ##            if pat in pat_segs:
        ##                digits.append(pat_segs[pat])
        ##            else:
        ##                digits.append(pat)
        ####        pat_map = infir_pats(pat_segs, patterns)
        ####        print(digits)
        ##        print(get_value(value, patterns))
        ####        print(length_conv(patterns.split(' ')))
        ####        print(length_conv(value.split(' ')))
        sum_values += get_values(value.split(" "), patterns.split(" "))
    print(sum_values)


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.")
    run()
