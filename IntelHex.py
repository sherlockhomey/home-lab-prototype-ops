import hashlib
import os
from intelhex import IntelHex

def get_dtd_60hz():
    return bytes.fromhex("7E 8B 70 A0 D0 A0 29 40 30 20 35 00 55 50 21 00 00 1E")

def get_dtd_30hz():
    return bytes.fromhex("3F 45 70 A0 D0 A0 29 40 30 20 35 00 55 50 21 00 00 1E")

def generate_hashes(filename):
    """Calculates hashes and size for the XML file."""
    with open(filename, "rb") as f:
        data = f.read()
        md5 = hashlib.md5(data).hexdigest()
        sha256 = hashlib.sha256(data).hexdigest()
        size = os.path.getsize(filename)
    return md5, sha256, size

def inject_and_hash(input_hex, output_hex):
    try:
        ih = IntelHex(input_hex)
        edid_data = bytearray(ih.tobinarray())

        # Slot 1: 60Hz (Preferred)
        edid_data[54:72] = get_dtd_60hz()
        # Slot 2: 30Hz
        edid_data[72:90] = get_dtd_30hz()

        # Recalculate EDID Checksum
        total_sum = sum(edid_data[:127])
        edid_data[127] = (256 - (total_sum % 256)) % 256

        # Save back to HEX
        new_ih = IntelHex()
        new_ih.frombytes(edid_data)
        new_ih.tofile(output_hex, format='hex')
        
        # Generate the values for your XML
        md5, sha256, size = generate_hashes(output_hex)
        
        print(f"--- XML UPDATE VALUES ---")
        print(f"FILE: {output_hex}")
        print(f"MD5:  {md5}")
        print(f"SHA256: {sha256}")
        print(f"SIZE: {size}")
        print(f"-------------------------")

    except FileNotFoundError:
        print(f"Error: Could not find '{input_hex}'. Check your file path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

inject_and_hash('7479_EDID_uC.hex', '7479_EDID_uC_MOD.hex')