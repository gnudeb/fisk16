
def sign_extend(value, initial_size, desired_size):
    if not (value & (1 << initial_size-1)):
        return value

    mask =\
        ((0xFFFF >> initial_size) << initial_size) \
        & (0xFFFF >> (16 - desired_size))

    return value | mask
