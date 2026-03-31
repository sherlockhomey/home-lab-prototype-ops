def verify_dtd_hex(hex_string):
    print("--- DTD Hex Verifier ---")
    data = bytes.fromhex(hex_string)
    
    # Reconstruct the Active Resolution
    h_active = ((data[4] & 0xF0) << 4) | data[2]
    v_active = ((data[7] & 0xF0) << 4) | data[5]
    
    # Reconstruct the Physical Dimensions (Bytes 12, 13, 14)
    h_size = ((data[14] & 0xF0) << 4) | data[12]
    v_size = ((data[14] & 0x0F) << 8) | data[13]
    
    print(f"Target Resolution: {h_active}x{v_active}")
    print(f"Physical Screen Size: {h_size} mm x {v_size} mm")
    
    # Calculate aspect ratio
    if v_size > 0:
        ratio = h_size / v_size
        print(f"Calculated Aspect Ratio: {ratio:.2f}:1 (Target is ~2.39:1 for UltraWide)")
    else:
        print("❌ Warning: Physical dimensions are zero.")

if __name__ == '__main__':
    # Our new string with the 799x334mm dimensions
    test_string = "F5 7C 70 A0 D0 A0 29 50 30 20 35 00 1F 4E 31 00 00 1A"
    verify_dtd_hex(test_string)