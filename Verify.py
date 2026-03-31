from intelhex import IntelHex

def verify_modifications(filename):
    print(f"--- Verifying {filename} ---\n")
    try:
        ih = IntelHex(filename)
        # Convert to a list of integers for easy slicing
        edid = ih.tobinarray()
        
        # Pull out the 18 bytes for Slot 1 and Slot 2
        # .tobytes().hex(" ") formats it nicely with spaces like "7E 8B 70..."
        slot1_actual = edid[54:72].tobytes().hex(" ").upper()
        slot2_actual = edid[72:90].tobytes().hex(" ").upper()
        
        # 1. Check Slot 1 (60Hz)
        print("Slot 1 Target: 7E 8B 70 A0 D0 A0 29 40 30 20 35 00 55 50 21 00 00 1E")
        print(f"Slot 1 Actual: {slot1_actual}")
        if slot1_actual.replace(" ", "") == "7E8B70A0D0A029403020350055502100001E":
            print("✅ CONFIRMED: 3440x1440 @ 60Hz is correctly installed in Slot 1.\n")
        else:
            print("❌ ERROR: Slot 1 does not match the 60Hz target.\n")

        # 2. Check Slot 2 (30Hz)
        print("Slot 2 Target: 3F 45 70 A0 D0 A0 29 40 30 20 35 00 55 50 21 00 00 1E")
        print(f"Slot 2 Actual: {slot2_actual}")
        if slot2_actual.replace(" ", "") == "3F4570A0D0A029403020350055502100001E":
            print("✅ CONFIRMED: 3440x1440 @ 30Hz is correctly installed in Slot 2.\n")
        else:
            print("❌ ERROR: Slot 2 does not match the 30Hz target.\n")

        # 3. Verify the Checksum
        print(f"Final Checksum Byte (Byte 127): {hex(edid[127])}")
        if sum(edid[:128]) % 256 == 0:
            print("✅ CONFIRMED: The EDID checksum is mathematically valid!")
        else:
            print("❌ ERROR: The checksum is broken. Do not flash this file.")

    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Is it in the same folder?")

if __name__ == '__main__':
    # Make sure this matches the file you just generated
    file_to_check = '7479_EDID_uC_MOD.hex'
    verify_modifications(file_to_check)