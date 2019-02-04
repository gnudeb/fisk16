
def sign_extend(value, initial_size, desired_size):
    if not (value & (1 << initial_size-1)):
        return value

    mask =\
        ((0xFFFF >> initial_size) << initial_size) \
        & (0xFFFF >> (16 - desired_size))

    return value | mask


def bit_mask(start, stop):
    """
    Return a number with all it's bits from `start` to `stop` set to 1.

    `stop` must not exceed 31.
    """
    # TODO: Make this function able to receive any `stop` value
    left = (0xFFFFFFFF >> (31 - stop))
    right = (0xFFFFFFFF << start)
    return left & right
