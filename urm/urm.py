import re


class Instruction:
    pass


class Zero(Instruction):
    def __init__(self, r):
        self.r = r
    
    def __repr__(self):
        return f'Z({self.r})'


class Successor(Instruction):
    def __init__(self, r):
        self.r = r
    
    def __repr__(self):
        return f'S({self.r})'


class Transfer(Instruction):
    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2
    
    def __repr__(self):
        return f'T({self.r1}, {self.r2})'


class Jump(Instruction):
    def __init__(self, r1, r2, r3):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    
    def __repr__(self):
        return f'J({self.r1}, {self.r2}, {self.r3})'


def parse_program(filepath):
    KNOWN_INSTRUCTIONS = {
        'Z': Zero,
        'S': Successor,
        'T': Transfer,
        'J': Jump,
    }

    with open(filepath) as f:
        lines = [re.sub(r'\s+', '', l) for l in f.readlines() if l]
    
    program = []
    
    # TODO: implement error handling
    for line in lines:
        split = line.split('(')
        instruction = split[0]
        argument_str = split[1].split(')')[0]
        arguments = [int(a) for a in argument_str.split(',')]
        program.append(KNOWN_INSTRUCTIONS[instruction](*arguments))
    
    return program

def dump_program(program, output_filepath):
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join([str(instr) for instr in program]))
