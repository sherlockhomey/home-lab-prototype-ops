import hashlib

def get_3440_60hz_cvt_rb():
    # 3440x1440 @ 60Hz (CVT-RB)
    return bytes.fromhex("7E 8B 70 A0 D0 A0 29 40 30 20 35 00 55 50 21 00 00 1E")

def inject_and_shift_edid(input_file, output_file):
    print(f"--- Processing {input_file} ---")
    
    try:
        with open(input_file, 'rb') as f:
            edid_data = bytearray(f.read())
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{input_file}'.")
        return

    # 1. Capture the existing 1080p DTD from Slot 1
    original_dtd1_1080p = edid_data[54:72]
    
    # 2. Overwrite Slot 2 (Erasing 1920x1200) with the captured 1080p data
    edid_data[72:90] = original_dtd1_1080p
    print("✅ Moved 1920x1080 @ 60Hz from Slot 1 down to Slot 2.")

    # 3. Inject the new UltraWide timing into Slot 1
    edid_data[54:72] = get_3440_60hz_cvt_rb()
    print("✅ Injected 3440x1440 @ 60Hz (CVT-RB) into Slot 1.")

    # 4. Recalculate Base Block Checksum (Byte 127)
    # The sum of bytes 0-127 must equal 0 mod 256
    total_sum = sum(edid_data[:127])
    edid_data[127] = (256 - (total_sum % 256)) % 256
    print(f"✅ Recalculated Base Checksum: {hex(edid_data[127])}")

    # 5. Save the modified binary file
    with open(output_file, 'wb') as f:
        f.write(edid_data)
    print(f"🚀 Success! Saved to {output_file}\n")

    # 6. Generate the Hashes for the XML
    md5 = hashlib.md5(edid_data).hexdigest()
    sha256 = hashlib.sha256(edid_data).hexdigest()
    size = len(edid_data)

    print("--- XML UPDATE VALUES ---")
    print(f"FILE: {output_file}")
    print(f"MD5:  {md5}")
    print(f"SHA256: {sha256}")
    print(f"SIZE: {size}")
    print("-------------------------")

if __name__ == '__main__':
    input_bin = 'Edid-7479I-1.bin'
    output_bin = 'Edid-7479I-1_MOD.bin'
    
    inject_and_shift_edid(input_bin, output_bin)