import hashlib

def get_uw_60hz():
    # 3440x1440 @ 60Hz CVT-RB (Includes 799x334mm dimensions for Windows)
    return bytes.fromhex("F5 7C 70 A0 D0 A0 29 50 30 20 35 00 1F 4E 31 00 00 1A")

def get_uw_30hz():
    # 3440x1440 @ 30Hz Standard (Includes 799x334mm dimensions for Windows)
    return bytes.fromhex("3F 45 70 A0 D0 A0 29 50 30 20 35 00 1F 4E 31 00 00 1A")

def execute_block0_modification(input_file, output_file):
    print(f"--- Processing {input_file} ---")
    
    try:
        with open(input_file, 'rb') as f:
            edid_data = bytearray(f.read())
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{input_file}'.")
        return

    # 1. Secure the fallback: Move 1080p @ 60Hz from Slot 1 down to Slot 2
    original_dtd1_1080p = edid_data[54:72]
    edid_data[72:90] = original_dtd1_1080p
    print("✅ Secured 1920x1080 @ 60Hz into Slot 2.")

    # 2. Inject the Dimension-Corrected Target Resolution into Slot 1
    target_resolution = get_uw_60hz() 
    edid_data[54:72] = target_resolution
    print("✅ Injected 3440x1440 @ 60Hz (with physical dimensions) into Slot 1.")

    # 3. Apply the 350MHz Silicon Patch
    for i in range(54, 126, 18):
        if edid_data[i:i+4] == b'\x00\x00\x00\xfd':
            edid_data[i+9] = 0x23
            print("✅ Upgraded Display Range Limits Max Clock to 350 MHz.")
            break

    # 4. Mathematically Seal the Base Block (Block 0 ONLY)
    total_sum = sum(edid_data[:127])
    edid_data[127] = (256 - (total_sum % 256)) % 256
    print(f"✅ Recalculated Base Checksum: {hex(edid_data[127])}")

    # 5. Write out the final binary (Extension block remains 100% untouched)
    with open(output_file, 'wb') as f:
        f.write(edid_data)
    print(f"🚀 Success! Saved to {output_file}\n")

    # 6. Generate the XML integrity hashes
    md5 = hashlib.md5(edid_data).hexdigest()
    sha256 = hashlib.sha256(edid_data).hexdigest()
    size = len(edid_data)

    print("--- NEW XML INTEGRITY VALUES ---")
    print(f"FILE: {output_file}")
    print(f"MD5:  {md5}")
    print(f"SHA256: {sha256}")
    print(f"SIZE: {size}")
    print("--------------------------------")

if __name__ == '__main__':
    # Ensure this points to your clean, original dump
    input_bin = 'Edid-7479I-1.bin' 
    output_bin = 'Edid-7479I-1_MOD_DIMENSIONS.bin'
    
    execute_block0_modification(input_bin, output_bin)