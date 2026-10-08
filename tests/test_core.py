import struct

from swainjohn_nexus.core import parse_soggy011_header


def packet(tag=b"usg-ai-node"):
    return struct.pack(
        ">12s16s32s32s",
        tag.ljust(12, b"\x00"),
        b"A" * 16,
        b"B" * 32,
        b"C" * 32,
    )


def test_parser_accepts_expected_tag_and_returns_opaque_fields():
    result = parse_soggy011_header(packet())

    assert result == {
        "security_tag": "usg-ai-node",
        "uuid": "A" * 16,
        "hash": "B" * 32,
        "signature": "C" * 32,
    }


def test_parser_rejects_short_packet_and_wrong_tag():
    assert parse_soggy011_header(b"short") is False
    assert parse_soggy011_header(packet(tag=b"not-a-node")) is False


def test_parser_accepts_bytes_like_inputs_and_ignores_trailing_bytes():
    valid_packet = packet()

    assert parse_soggy011_header(bytearray(valid_packet)) == parse_soggy011_header(valid_packet)
    assert parse_soggy011_header(memoryview(valid_packet)) == parse_soggy011_header(valid_packet)
    assert parse_soggy011_header(valid_packet + b"ignored") == parse_soggy011_header(valid_packet)


def test_parser_rejects_non_bytes_input():
    assert parse_soggy011_header("not bytes") is False
