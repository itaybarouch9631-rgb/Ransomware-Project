from Crypto.PublicKey import RSA

def generate_rsa_keypair() -> None:
    print(" Generating 2048-bit RSA key pair... This might take a second.")
    
    key = RSA.generate(2048)

    private_key = key.export_key()
    with open("server_RSA_private.pem", "wb") as f:
        f.write(private_key)
    
    public_key = key.publickey().export_key()
    with open("server_RSA_public.pem", "wb") as f:
        f.write(public_key)

    print("Success! Keys have been created and saved to your folder:")
    print("    🔒 server_RSA_private.pem (KEEP SECRET! NEVER SHARE!)")
    print("    🔓 server_RSA_public.pem  (The server uses this to lock AES keys)")

if __name__ == "__main__":
    generate_rsa_keypair()