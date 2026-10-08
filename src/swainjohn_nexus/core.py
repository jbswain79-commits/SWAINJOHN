import struct


def parse_soggy011_header(binary_packet_data):
    """Validate and decode a SWAINJOHN SOGGY-011 packet header."""
    if not isinstance(binary_packet_data, (bytes, bytearray, memoryview)):
        return False

    data = bytes(binary_packet_data)
    format_string = ">12s16s32s32s"
    expected_core_size = struct.calcsize(format_string)
    if len(data) < expected_core_size:
        return False

    raw_tag, raw_uuid, raw_hash, raw_signature = struct.unpack(
        format_string,
        data[:expected_core_size],
    )
    decoded_tag = raw_tag.decode("utf-8", errors="ignore").strip("\x00")
    if decoded_tag != "usg-ai-node":
        return False

    return {
        "security_tag": decoded_tag,
        "uuid": raw_uuid.decode("utf-8", errors="ignore").strip("\x00"),
        "hash": raw_hash.decode("utf-8", errors="ignore").strip("\x00"),
        "signature": raw_signature.decode("utf-8", errors="ignore").strip("\x00"),
    }


def verify_spatial_drift_compliance(measured_area, baseline_area=100.00):
    variance = ((measured_area - baseline_area) / baseline_area) * 100.0
    if abs(variance) > 1.5:
        print("!! GAO-15-593SP REFLEX TRIGGER TRIPPED: Variance Exceeds Strict +-1.5% Fence !!")
        return False
    print(" -> Status: COMPLIANT. Coordinate boundary stable.")
    return True


def generate_security_report(measured_area, baseline_area=100.00):
    variance = ((measured_area - baseline_area) / baseline_area) * 100.0
    return {
        "baseline_area": baseline_area,
        "measured_area": measured_area,
        "variance_percent": variance,
        "within_threshold": abs(variance) <= 1.5,
        "security_tag": "usg-ai-node",
    }
