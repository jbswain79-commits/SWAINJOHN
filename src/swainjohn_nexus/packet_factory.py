import struct


def create_valid_packet() -> bytes:
    return struct.pack(
        ">12s16s32s32s",
        b"usg-ai-node".ljust(12, b"\x00"),
        b"A" * 16,
        b"B" * 32,
        b"C" * 32,
    )
