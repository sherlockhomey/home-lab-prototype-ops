import hashlib

def get_uw_60hz():
    # 3440x1440 @ 60Hz CVT-RB (Pixel Clock: ~319 MHz)
    return bytes.fromhex("F5 7C 70 A0 D0 A0 29 50 30 20 35 00 1F 4E 31 00 00 1A")

def get_uw_30hz():
    # 3440x1440 @ 30Hz Standard (Pixel Clock: ~177 MHz)
    return bytes.fromhex("3F 45 70 A0 D0 A0 29 50 30 20 35 00 1F 4E 31 00 00 1A")

def execute_minimal_reboot_fix(input_file, output_file):
    print(f"--- Processing {input_file} ---")
    
    try:
        with open(input_file, 'rb') as f:
            edid = bytearray(f.read())
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{input_file}'.")
        return

    # ==========================================
    # BLOCK 0: BASE EDID MODIFICATIONS
    # ==========================================
    edid[54:72] = get_uw_60hz() # Set 60Hz as the absolute Preferred Timing
    edid[72:90] = get_uw_30hz() # Set 30Hz as the secondary Timing
    print("✅ BLOCK 0: Injected 3440x1440 at 60Hz & 30Hz.")
    
    # Patch Block 0 Max Dot Clock to 340 MHz (Legal HDMI 1.4 limit)
    for i in range(54, 126, 18):
        if edid[i:i+4] == b'\x00\x00\x00\xfd':
            edid[i+9] = 0x22 # 340 MHz
            print("✅ BLOCK 0: Patched Max Dot Clock to 340 MHz.")
            break

    edid[127] = (256 - (sum(edid[:127]) % 256)) % 256

    # ==========================================
    # BLOCK 1: SURGICAL EXTENSION MODIFICATIONS
    # ==========================================
    if len(edid) >= 256 and edid[128] == 0x02:
        data_block_end = 128 + edid[130] 
        i = 132 
        
        while i < data_block_end:
            tag = edid[i] >> 5
            length = edid[i] & 0x1F
            
            # 1. Strip the "Native" priority flag from 1080p (VIC 16)
            if tag == 2:
                for j in range(i+1, i+1+length):
                    if edid[j] == 0x90: # 0x90 = Native Flag (128) + VIC 16
                        edid[j] = 0x10  # 0x10 = Just VIC 16
                        print("✅ BLOCK 1: Stripped 'Native' priority from 1080p.")
            
            # 2. Patch HDMI Max TMDS Clock to 340 MHz
            elif tag == 3 and edid[i+1:i+4] == b'\x03\x0c\x00':
                edid[i+7] = 0x44 # 68 * 5 = 340 MHz
                print("✅ BLOCK 1: Patched HDMI Max TMDS Clock to 340 MHz.")
            
            i += length + 1
        
        edid[255] = (256 - (sum(edid[128:255]) % 256)) % 256

    # ==========================================
    # SAVE & HASH
    # ==========================================
    with open(output_file, 'wb') as f:
        f.write(edid)
    print(f"\n🚀 Success! Saved to {output_file}\n")

    print("--- NEW XML INTEGRITY VALUES ---")
    print(f"MD5:    {hashlib.md5(edid).hexdigest()}")
    print(f"SHA256: {hashlib.sha256(edid).hexdigest()}")
    print(f"SIZE:   {len(edid)}")

if __name__ == '__main__':
    # Make sure to run this against the clean, original EDID file
    input_bin = 'Edid-7479I-1.bin' 
    output_bin = 'Edid-7479I-1_MINIMAL_REBOOT_FIX.bin'
    execute_minimal_reboot_fix(input_bin, output_bin)