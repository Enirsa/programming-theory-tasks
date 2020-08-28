from urm import Zero, Successor, Transfer, Jump, parse_program, dump_program
from urm.utils import (
    total_memory_used,
    inject_argument_copy,
    inject_memory_zeroing,
    rewrite_jumps_into_end,
    shift,
)


def create_minimization(f, arg_count):
    """
    Finds y such that f(...args, y) = 0.
    """
    minimization = []
    memory_length = total_memory_used(f)
    extra_memory_length = arg_count + 2  # args, register with the result, counter
    
    inject_memory_zeroing(minimization, extra_memory_length + arg_count + 2, extra_memory_length + memory_length)
    inject_argument_copy(minimization, arg_count + 1, extra_memory_length)
    
    rewrite_jumps_into_end(f)
    shift(f, extra_memory_length, len(minimization))
    
    minimization += f
    
    # Instructions that are responsible for finding the solution
    minimization += [
        Jump(0, extra_memory_length, len(minimization) + 4),
        Successor(arg_count + 1),
        Jump(0, 0, 1),
        Transfer(extra_memory_length - 1, 0),
    ]
    
    return minimization


if __name__ == '__main__':
    f = parse_program('input/ff.urm')
    arg_count = 1

    minimization = create_minimization(f, arg_count)
    dump_program(minimization, 'output/minimization.urm')
