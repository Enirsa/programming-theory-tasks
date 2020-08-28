from urm import Zero, Successor, Transfer, Jump, parse_program, dump_program
from urm.utils import (
    total_memory_used,
    inject_argument_copy,
    rewrite_jumps_into_end,
    shift,
)

def create_superposition(g, fs, arg_count):
    """
    Computes g(f1(args), f1(args), ..., fn(args)).
    """
    superposition = []
    registers_with_results = []
    memory_length = arg_count + 1
    
    for f in fs:
        registers_with_results.append(memory_length)

        subprogram_memory_length = total_memory_used(f)

        inject_argument_copy(superposition, arg_count, memory_length)
        
        rewrite_jumps_into_end(f)
        shift(f, memory_length, len(superposition))
        
        superposition += f
        memory_length += subprogram_memory_length
    
    superposition += [
        Transfer(r, memory_length + i)
        for i, r
        in enumerate(registers_with_results, start=1)
    ]

    rewrite_jumps_into_end(g)
    shift(g, memory_length, len(superposition))
    superposition += g
    
    superposition.append(Transfer(memory_length, 0))
    
    return superposition


if __name__ == '__main__':
    g = parse_program('input/sum.urm')
    f1 = parse_program('input/sum.urm')
    f2 = parse_program('input/sum.urm')
    arg_count = 2

    superposition = create_superposition(g, (f1, f2), 2)
    dump_program(superposition, 'output/superposition.urm')
