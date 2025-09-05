# crypto_files.py
from pathlib import Path
import json
import os

def _shift_alpha(c: str, k: int) -> str:
    """Shift alphabetic c by k (mod 26), preserve case. Non-letters returned unchanged."""
    if 'a' <= c <= 'z':
        base = ord('a'); return chr((ord(c) - base + (k % 26)) % 26 + base)
    if 'A' <= c <= 'Z':
        base = ord('A'); return chr((ord(c) - base + (k % 26)) % 26 + base)
    return c

def _class_code(c: str) -> str:
    """
    Returns one of:
      'l1' (lowercase a-m), 'l2' (lowercase n-z),
      'u1' (uppercase A-M), 'u2' (uppercase N-Z),
      '.'  (non-letter)
    """
    if 'a' <= c <= 'z':
        return 'l1' if c <= 'm' else 'l2'
    if 'A' <= c <= 'Z':
        return 'u1' if c <= 'M' else 'u2'
    return '.'

# ------------------ core transforms (using metadata for perfect invertibility) ------------------

def encrypt_text_with_meta(text: str, shift1: int, shift2: int):
    """
    Returns (encrypted_text, meta_list), where meta_list has one code per char
    to identify which rule was applied so decryption is unambiguous.
    """
    s1 = shift1 % 26
    s2 = shift2 % 26
    out_chars = []
    meta = []

    for ch in text:
        code = _class_code(ch)
        meta.append(code)

        if code == 'l1':          # a-m: forward by shift1 * shift2
            out_chars.append(_shift_alpha(ch, (s1 * s2) % 26))
        elif code == 'l2':        # n-z: backward by shift1 + shift2
            out_chars.append(_shift_alpha(ch, -(s1 + s2) % 26))
        elif code == 'u1':        # A-M: backward by shift1
            out_chars.append(_shift_alpha(ch, -s1))
        elif code == 'u2':        # N-Z: forward by shift2^2
            out_chars.append(_shift_alpha(ch, (s2 * s2) % 26))
        else:                     # other characters unchanged
            out_chars.append(ch)

    return ''.join(out_chars), meta

def decrypt_text_with_meta(enc_text: str, shift1: int, shift2: int, meta):
    """Lossless decryption using the stored meta per character."""
    s1 = shift1 % 26
    s2 = shift2 % 26
    out_chars = []

    for ch, code in zip(enc_text, meta):
        if code == 'l1':          # undo forward by s1*s2
            out_chars.append(_shift_alpha(ch, -(s1 * s2) % 26))
        elif code == 'l2':        # undo backward by s1+s2
            out_chars.append(_shift_alpha(ch, +(s1 + s2) % 26))
        elif code == 'u1':        # undo backward by s1
            out_chars.append(_shift_alpha(ch, +s1))
        elif code == 'u2':        # undo forward by s2^2
            out_chars.append(_shift_alpha(ch, -(s2 * s2) % 26))
        else:
            out_chars.append(ch)

    return ''.join(out_chars)

# ------------------ file ops ------------------

def encrypt_file(shift1: int, shift2: int,
                 src="raw_text.txt",
                 enc_dst="encrypted_text.txt",
                 meta_dst="encrypted_text.meta"):
    raw_p = Path(src)
    if not raw_p.exists():
        raise FileNotFoundError(f"Input file not found: {raw_p.resolve()}")

    text = raw_p.read_text(encoding="utf-8")
    enc, meta = encrypt_text_with_meta(text, shift1, shift2)

    Path(enc_dst).write_text(enc, encoding="utf-8")
    # store the metadata as JSON (one code per character)
    Path(meta_dst).write_text(json.dumps(meta), encoding="utf-8")

def decrypt_file(shift1: int, shift2: int,
                 enc_src="encrypted_text.txt",
                 dec_dst="decrypted_text.txt",
                 meta_src="encrypted_text.meta"):
    enc_p = Path(enc_src)
    meta_p = Path(meta_src)
    if not enc_p.exists():
        raise FileNotFoundError(f"Encrypted file not found: {enc_p.resolve()}")
    if not meta_p.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {meta_p.resolve()}\n"
            "This scheme needs the meta file to decrypt losslessly for all shift choices."
        )

    enc_text = enc_p.read_text(encoding="utf-8")
    meta = json.loads(meta_p.read_text(encoding="utf-8"))

    if len(meta) != len(enc_text):
        raise ValueError("Metadata length does not match encrypted text length.")

    dec = decrypt_text_with_meta(enc_text, shift1, shift2, meta)
    Path(dec_dst).write_text(dec, encoding="utf-8")

    try:
        os.remove(meta_src)
    except FileNotFoundError:
        pass

def verify_decryption(raw="raw_text.txt", dec="decrypted_text.txt") -> bool:
    raw_text = Path(raw).read_text(encoding="utf-8")
    dec_text = Path(dec).read_text(encoding="utf-8")
    ok = (raw_text == dec_text)
    print("Decryption successful! Files match." if ok else "❌ Decryption failed. Files do not match.")
    return ok

# ------------------ main script ------------------

if __name__ == "__main__":
    s1 = int(input("Enter shift1 value: "))
    s2 = int(input("Enter shift2 value: "))
    if s1<0 or s2<0:
      print("invalid shift value") 
    else: 
     encrypt_file(s1, s2)                # raw_text.txt -> encrypted_text.txt (+ encrypted_text.meta)
     decrypt_file(s1, s2)                # encrypted_text.txt (+ .meta) -> decrypted_text.txt
     verify_decryption()
