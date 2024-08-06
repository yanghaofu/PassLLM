from gmssl import sm2, func


def generate_sm2_keypair():
    # SM2私钥长度为32字节（256位）
    private_key_length = 32
    private_key = func.random_hex(private_key_length)
    sm2_crypt = sm2.CryptSM2(private_key=private_key)
    public_key = sm2_crypt.get_public_key()

    return private_key, public_key


private_key, public_key = generate_sm2_keypair()

print("Private Key:", private_key)
print("Public Key:", public_key)
