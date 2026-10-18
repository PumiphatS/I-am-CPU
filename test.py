"""
    Register: [R1, R2, R3, R4, PC]

    Instruction:

        Add dst scr1 scr2
        LD dst src
        LDI dst imm
        SYSCALL

    Calling convention

    R1: function number
    R2: return value
    R3: parameter

    System call:

        0: print
"""

import numpy as np

#Declare storage
REGISTER = np.zeros(5, dtype = np.uint64)

REGISTER_LOOKUP = {
    "R1": 0,
    "R2": 1,
    "R3": 2,
    "R4": 3,
    "PC": 4
}

#check if it is a valid register label or not
def valid_register(word: str) -> bool:
    return word in REGISTER_LOOKUP

def parse_register(word: str) -> int:
    return REGISTER_LOOKUP[word]

def valid_integer(word: str) -> bool:
    return (word.isdigit()) \
        or (word[0] == "-" and word[1:].isdigit())

def parse_integer(word: str) -> int:
    return int(word)

def add(argument: list[int]) -> None:
    dst = argument[0]
    src1 = argument[1]
    src2 = argument[2]
    REGISTER[dst] = REGISTER[src1] + REGISTER[src2]

def valid_add(words: list[str]) -> bool:
    if len(words) < 4:
        return False

    if not valid_register(words[1]):
        return False

    if not valid_register(words[2]):
        return False

    if not valid_register(words[3]):
        return False
    
    return True

def parse_add(words: list[str]) -> list[int]:
    return [parse_register(words[1]),
            parse_register(words[2]),
            parse_register(words[3])]

def load(argument: list[int]) -> None:
    dst = argument[0]
    src = argument[1]
    REGISTER[dst] = REGISTER[src]

def valid_load(words: list[str]) -> bool:
    if len(words) < 3:
        return False

    if not valid_register(words[1]):
        return False

    if not valid_register(words[2]):
        return False

    return True

def parse_load(words: list[str]) -> list[int]:
    return [parse_register(words[1]),
            parse_register(words[2])]

def load_immediate(argument: list[int]) -> None:
    dst = argument[0]
    imm = argument[1]
    REGISTER[dst] = imm

def valid_load_immediate(words: list[str]) -> bool:
    if len(words) < 3:
        return False

    if not valid_register(words[1]):
        return False

    if not valid_integer(words[2]):
        return False

    return True

def parse_load_immediate(words: list[str]) -> list[int]:
    return [parse_register(words[1]),
            parse_integer(words[2])]

SYSCALL_LOOKUP = [print, ]

def syscall(argument: list[int]) -> None:
    result = SYSCALL_LOOKUP[REGISTER[0]](REGISTER[2])
    if result is None:
        return
    REGISTER[1] = result

def valid_syscall(words: list[str]) -> bool:
    if len(words) < 1:
        return False
    
    return True

def parse_syscall(words: list[str]) -> list[int]:
    return []

OPCODE_LOOKUP = {
    "ADD": {
        "fn_ptr": add,
        "valid": valid_add,
        "parse": parse_add,
    },
    "LD": {
        "fn_ptr": load,
        "valid": valid_load,
        "parse": parse_load,
    },
    "LDI": {
        "fn_ptr": load_immediate,
        "valid": valid_load_immediate,
        "parse": parse_load_immediate,
    },
    "SYSCALL": {
        "fn_ptr": syscall,
        "valid": valid_syscall,
        "parse": parse_syscall,
    }
}

def load_program(instructions: list,
                  data: list,
                 filename: str):
    instructions.clear()
    data.clear()

    with open(filename, "r") as file:
        line_number = 0
        for line in file:
            line_number += 1
            words = line.strip().split()
            opcode = words[0]
            if opcode not in OPCODE_LOOKUP:
                continue

            if not valid_opcode(opcode, words):
                print(f"Compile error on line {line_number}: {words}")

            instructions.append(OPCODE_LOOKUP[opcode]["fn_ptr"])
            data.append(OPCODE_LOOKUP[opcode]["parse"](words))

def valid_opcode(opcode: str, words: str) -> bool:
    return OPCODE_LOOKUP[opcode]["valid"](words)

def binary_dump(instructions: list, data: list[list[int]]):

    for i, instruction in enumerate(instructions):
        arguments = data[i]
        print(f"[{i + 1}]: {instruction} {arguments}")

instructions = []
data = []

load_program(instructions, data, "program.asm")
binary_dump(instructions, data)

while REGISTER[4] < len(instructions):
    instructions[REGISTER[4]](data[REGISTER[4]])
    REGISTER[4] += 1