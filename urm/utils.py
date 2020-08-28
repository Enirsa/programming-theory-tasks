from urm import Zero, Successor, Transfer, Jump


def rewrite_jumps(program, jump_to):
    """
    Rewrites outer jump instructions to a given position.
    """
    length = len(program)

    for instr in program:
        if isinstance(instr, Jump) and (instr.r3 > length or instr.r3 == 0):
            instr.r3 = jump_to

            
def rewrite_jumps_into_end(program):
    rewrite_jumps(program, len(program) + 1)

def rewrite_jumps_into_beginning(program):
    rewrite_jumps(program, 0)

def shift(program, memory_shift, instruction_shift):
    """
    Shifts the whole program into another memory segment and rewrites jump lines.
    """
    for instr in program:
        if isinstance(instr, (Zero, Successor)):
            instr.r += memory_shift
        elif isinstance(instr, Transfer):
            instr.r1 += memory_shift
            instr.r2 += memory_shift
        elif isinstance(instr, Jump):
            instr.r1 += memory_shift
            instr.r2 += memory_shift
            instr.r3 += instruction_shift

def total_memory_used(program):
    """
    Calculates total memory used by a program.
    """
    total_memory = 0
    
    for instr in program:
        if isinstance(instr, (Zero, Successor)):
            total_memory = max(total_memory, instr.r)
        elif isinstance(instr, (Transfer, Jump)):
            total_memory = max(total_memory, instr.r1, instr.r2)
    
    return total_memory + 1

def inject_argument_copy(program, arg_count, memory_shift):
    """
    Injects transfer instructions at the end of a program to copy arguments over a memory shift.
    """
    return program.extend([
        Transfer(r, r + memory_shift)
        for r
        in range(1, arg_count + 1)
    ])

def inject_memory_zeroing(program, _from, _to):
    """
    Injects zeroing instructions at the end of a program to clear registers in range [_from, _to).
    """
    return program.extend([Zero(r) for r in range(_from, _to)])
