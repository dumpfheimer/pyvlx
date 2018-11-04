"""Helper for Frames."""
from .exception import PyVLXException
from .const import Command


def calc_crc(raw):
    """Calculate cyclic redundancy check (CRC)."""
    crc = 0
    for sym in raw:
        crc = crc ^ int(sym)
    return crc


def extract_from_frame(data):
    """Extract payload and command from frame."""
    if len(data) <= 4:
        raise PyVLXException("could_not_extract_from_frame_too_short")
    length = data[0] * 256 + data[1] - 1
    if len(data) != length + 3:
        raise PyVLXException("could_not_extract_from_frame_invalid_length")
    if calc_crc(data[:-1]) != data[-1]:
        raise PyVLXException("could_not_extract_from_frame_invalid_crc")
    payload = data[4:-1]
    try:
        command = Command(data[2] * 256 + data[3])
    except ValueError:
        raise PyVLXException("could_not_extract_from_frame_command", payload=data)
    return command, payload