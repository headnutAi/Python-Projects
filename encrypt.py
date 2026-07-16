import os
import sys
import argparse
import getpass
import base64
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

SALT_SIZE = 16
KDF_ITERS = 390_000


def derive_key(password: bytes, salt: bytes) -> bytes:
    """Derive a 32-byte key from password+salt via PBKDF2-HMAC-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt_file(src: Path, dst: Path, password: bytes) -> None:
    """Encrypt a single file: write salt||ciphertext to dst."""
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    f = Fernet(key)
    data = src.read_bytes()
    token = f.encrypt(data)
    dst.write_bytes(salt + token)
    print(f"[+] Encrypted: {src} → {dst}")


def decrypt_file(src: Path, dst: Path, password: bytes) -> None:

    data = src.read_bytes()
    salt, token = data[:SALT_SIZE], data[SALT_SIZE:]
    key = derive_key(password, salt)
    f = Fernet(key)
    try:
        plain = f.decrypt(token)
    except Exception as e:
        print(f"[!] Failed decrypt {src}: {e}")
        return
    dst.write_bytes(plain)
    print(f"[+] Decrypted: {src} → {dst}")


def process_path(
    mode: str, inp: Path, outp: Path, password: bytes
) -> None:

    if inp.is_file():
        # Determine destination file name
        if outp.is_dir():
            stem = inp.stem
            suffix = inp.suffix
            if mode == "encrypt":
                suffix += ".enc"
            elif mode == "decrypt" and suffix == ".enc":
                suffix = ""
            dst = outp / (stem + suffix)
        else:
            dst = outp
        dst.parent.mkdir(parents=True, exist_ok=True)
        if mode == "encrypt":
            encrypt_file(inp, dst, password)
        else:
            decrypt_file(inp, dst, password)
    elif inp.is_dir():
        # Must have directory output
        for child in inp.rglob("*"):
            rel = child.relative_to(inp)
            process_path(mode, child, outp / rel.parent, password)
    else:
        print(f"[!] Skipping unknown path: {inp}")


def main():
    p = argparse.ArgumentParser(
        description="Secure file/directory encryptor/decryptor"
    )
    sub = p.add_subparsers(dest="mode", required=True)
    for cmd in ("encrypt", "decrypt"):
        sp = sub.add_parser(cmd)
        sp.add_argument(
            "-i", "--input", required=True,
            help="Input file or directory"
        )
        sp.add_argument(
            "-o", "--output", required=True,
            help="Output file or directory"
        )
    args = p.parse_args()
    inp = Path(args.input).expanduser()
    outp = Path(args.output).expanduser()

    if not inp.exists():
        print(f"[!] Input not found: {inp}")
        sys.exit(1)
    if inp.is_dir() and (outp.exists() and outp.is_file()):
        print("[!] Cannot write directory into a file")
        sys.exit(1)
    if inp.is_file() and outp.exists() and outp.is_file() and outp.samefile(inp):
        print("[!] Input and output paths must differ")
        sys.exit(1)

    pw = getpass.getpass("Password: ").encode()
    if not pw:
        print("[!] Empty password")
        sys.exit(1)

    process_path(args.mode, inp, outp, pw)


if __name__ == "__main__":
    main()