import hashlib

def get_uw_60hz():
    # 3440x1440 @ 60Hz CVT-RB (Includes 799x334mm dimensions)
    return bytes.fromhex("F5 7C 70 A0 D0 A0 29 50 30 20 35 00 1F 4E 31 00 00 1A")

def execute_surgical_modification(input_file, output_file):
    print(f"--- Processing {input_file} ---")
    
    try:
        with open(input_file, 'rb') as f:
            edid = bytearray(f.read())
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{input_file}'.")
        return

    # ==========================================
    # BLOCK 0 MODIFICATIONS
    # ==========================================
    # 1. Secure 1080p to Slot 2
    edid[72:90] = edid[54:72]
    # 2. Inject Target Resolution
    edid[54:72] = get_uw_60hz()
    
    # 3. Patch Display Range Limits (Block 0)
    for i in range(54, 126, 18):
        if edid[i:i+4] == b'\x00\x00\x00\xfd':
            edid[i+9] = 0x23 # 350 MHz
            break

    # 4. Seal Block 0 Checksum
    edid[127] = (256 - (sum(edid[:127]) % 256)) % 256
    print("✅ BLOCK 0: Injected timings and patched 350MHz limit.")

    # ==========================================
    # BLOCK 1 MODIFICATIONS (The Missing Link)
    # ==========================================
    if len(edid) >= 256 and edid[128] == 0x02:
        # Data blocks start at byte 132 (Offset 4 inside Block 1)
        # They end where the Detailed Timing Descriptors begin (edid[130])
        data_block_end = 128 + edid[130]
        i = 132 
        
        while i < data_block_end:
            tag = edid[i] >> 5
            length = edid[i] & 0x1F
            
            # Tag 3 = Vendor-Specific Data Block
            if tag == 3:
                # Check for HDMI IEEE OUI (03-0C-00)
                if edid[i+1:i+4] == b'\x03\x0c\x00':
                    # Byte 7 of this block is the Max TMDS clock in 5MHz increments.
                    # Original is 0x3C (60 * 5 = 300MHz). We need 0x46 (70 * 5 = 350MHz).
                    edid[i+7] = 0x46
                    print("✅ BLOCK 1: Surgically patched HDMI VSDB Max TMDS Clock to 350MHz.")
                    break
            i += length + 1 # Jump to the next data block
        
        # 5. Seal Block 1 Checksum
        edid[255] = (256 - (sum(edid[128:255]) % 256)) % 256
        print("✅ BLOCK 1: Recalculated Extension Checksum.")

    # ==========================================
    # FINAL FILE & HASH GENERATION
    # ==========================================
    with open(output_file, 'wb') as f:
        f.write(edid)
    print(f"\n🚀 Success! Saved to {output_file}\n")

    md5 = hashlib.md5(edid).hexdigest()
    sha256 = hashlib.sha256(edid).hexdigest()
    size = len(edid)

    print("--- NEW XML INTEGRITY VALUES ---")
    print(f"FILE: {output_file}")
    print(f"MD5:  {md5}")
    print(f"SHA256: {sha256}")
    print(f"SIZE: {size}")
    print("--------------------------------")

if __name__ == '__main__':
    input_bin = 'Edid-7479I-1.bin' # Ensure this is your ORIGINAL, clean dump
    output_bin = 'Edid-7479I-1_MOD_SURGICAL.bin'
    
    execute_surgical_modification(input_bin, output_bin)