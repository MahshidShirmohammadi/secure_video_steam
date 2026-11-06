"""Small, deliberately insecure LFSR stream cipher for teaching."""

MAX_SEED = 0xFFFF
LFSR_PERIOD_BITS = 0xFFFF


def _validate_seed(seed: int) -> None:
    if not isinstance(seed, int) or not 1 <= seed <= MAX_SEED:
        raise ValueError("seed must be an integer from 1 to 65535")


def _next_bit(state: int) -> tuple[int, int]:
    """Return output bit and next state for x^16 + x^14 + x^13 + x^11 + 1."""

    output_bit = state & 1

    feedback = (
        ((state >> 0) & 1)
        ^ ((state >> 2) & 1)
        ^ ((state >> 3) & 1)
        ^ ((state >> 5) & 1)
    )
    next_state = (state >> 1) | (feedback << 15)

    return output_bit, next_state



def keystream(length: int, seed: int, offset: int = 0) -> bytes:
    """Return length keystream bytes, starting at an absolute byte offset."""
    _validate_seed(seed)
    if not isinstance(length, int) or length < 0:
        raise ValueError("length must be a non-negative integer")
    if not isinstance(offset, int) or offset < 0:
        raise ValueError("offset must be a non-negative integer")

    # TODO
    state = seed
    output = []

    offset = offset % LFSR_PERIOD_BITS

    for _ in range(offset * 8):
        _, state = _next_bit(state)

    for _ in range(length):
        byte_value = 0
        
        for _ in range(8):
            bit, state = _next_bit(state)
            byte_value = (byte_value << 1) | bit

        output.append(byte_value)

    return bytes(output)


def xor_bytes(data: bytes, seed: int, offset: int = 0) -> bytes:
    """Encrypt or decrypt data with the keystream at absolute byte offset."""
    # TODO
    key = keystream(len(data), seed, offset)
    result = []

    for i in range(len(data)):
        result.append(data[i] ^ key[i])

    return bytes(result)
