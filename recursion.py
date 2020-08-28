from urm import Zero, Successor, Transfer, Jump, parse_program, dump_program
from urm.utils import (
    total_memory_used,
    inject_argument_copy,
    inject_memory_zeroing,
    rewrite_jumps_into_end,
    shift,
)


def create_recursion(f, g, arg_count):
    recursion = []
    extra_memory_length = arg_count + 3  # args, register with the result, y, counter
    max_memory_length = max(total_memory_used(f), total_memory_used(g))
    
    inject_argument_copy(recursion, arg_count, extra_memory_length)
    
    rewrite_jumps_into_end(f)
    shift(f, extra_memory_length, len(recursion))
    
    recursion += f
    loop_line = len(recursion) + 1

    result_register = extra_memory_length
    y_register = arg_count + 1
    counter_register = arg_count + 2

    recursion.extend([
        Transfer(result_register, 0),
        Jump(y_register, counter_register, 0),
        Successor(counter_register),
        Zero(result_register),
    ])

    inject_memory_zeroing(
        recursion,
        extra_memory_length + arg_count + 3,
        extra_memory_length + max_memory_length
    )
    inject_argument_copy(recursion, arg_count, extra_memory_length)

    recursion.extend([
        Transfer(counter_register, extra_memory_length + arg_count + 1),  # transfer counter into g-y register
        Transfer(0, extra_memory_length + arg_count + 2),  # transfer the result of the previous loop into g-h register
    ])

    rewrite_jumps_into_end(g)
    shift(g, extra_memory_length, len(recursion))
    
    recursion += g
    recursion.append(Jump(0, 0, loop_line))
    
    return recursion


if __name__ == '__main__':
    f = parse_program('input/f.urm')
    g = parse_program('input/g.urm')
    arg_count = 1

    recursion = create_recursion(f, g, arg_count)
    dump_program(recursion, 'output/recursion.urm')
