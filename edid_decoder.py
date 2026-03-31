def decode_edid_bin(filename):
    try:
        with open(filename, 'rb') as f:
            edid = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'")
        return

    if len(edid) < 128:
        print("Error: Not a valid EDID. File is smaller than 128 bytes.")
        return

    print(f"--- Decoded Resolutions for {filename} ---\n")

    # 1. Decode Standard Timings (Bytes 38 to 53)
    print("Supported Standard Timings (Fallbacks):")
    found_standard = False
    
    # EDID stores standard timings in 2-byte pairs
    for i in range(38, 54, 2):
        b1, b2 = edid[i], edid[i+1]
        
        # 0x01 0x01 means the slot is empty/unused
        if b1 != 0x01 and b1 != 0x00: 
            # EDID formula for X resolution
            x_res = (b1 + 31) * 8 
            
            # Bitwise operations to extract the aspect ratio and refresh rate
            ratio_code = (b2 >> 6) & 0x03
            refresh = (b2 & 0x3F) + 60
            
            # Calculate Y resolution based on the aspect ratio code
            if ratio_code == 0: y_res = (x_res * 10) // 16    # 16:10
            elif ratio_code == 1: y_res = (x_res * 3) // 4    # 4:3
            elif ratio_code == 2: y_res = (x_res * 4) // 5    # 5:4
            elif ratio_code == 3: y_res = (x_res * 9) // 16   # 16:9
            
            print(f"  - {x_res}x{y_res} @ {refresh}Hz")
            found_standard = True
            
    if not found_standard:
        print("  - No standard timings populated.")

    # 2. Decode Preferred Timing (DTD Slot 1 - Bytes 54 to 71)
    print("\nPreferred Resolution (DTD Slot 1):")
    
    # Check the pixel clock to ensure it's a valid timing block
    pixel_clock = (edid[55] << 8) | edid[54]
    
    if pixel_clock != 0:
        # Bitwise shifting to stitch the resolution halves back together
        h_active = ((edid[58] & 0xF0) << 4) | edid[56]
        v_active = ((edid[61] & 0xF0) << 4) | edid[59]
        print(f"  - {h_active}x{v_active}")
    else:
        print("  - No preferred timing found in Slot 1.")
        
    print("-" * 40)

if __name__ == '__main__':
    # Replace this with the actual name of your .bin file
    decode_edid_bin('Edid-7479I-1.bin')