
def sign_extend(value, initial_size, desired_size):
    if not (value & (1 << initial_size-1)):
        return value

    mask =\
        ((0xFFFF >> initial_size) << initial_size) \
        & (0xFFFF >> (16 - desired_size))

    return value | mask


def bit_mask(start, stop):
    """Return a number with all it's bits from `start` to `stop` set to 1."""
    number_of_set_bits = stop - start + 1
    return ((1 << number_of_set_bits) - 1) << start
