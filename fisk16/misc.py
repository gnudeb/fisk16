from itertools import islice


def hexdump(data):
    it = iter(data)
    result = ""
    address = 0
    while True:
        # Retrieves next 16 bytes
        chunk = tuple(islice(it, 16))
        if not chunk:
            # Iterator has been depleted
            return result

        hex_part = ' '.join(map(lambda b: format(b, "02x"), chunk))
        ascii_part = ''.join((chr(b) if chr(b).isprintable() else '.') for b in chunk)

        result += "{:04x}  {:47}  |{}|\n".format(address, hex_part, ascii_part)

        address += 16
