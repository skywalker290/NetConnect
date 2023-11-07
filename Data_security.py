from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils

def private_key_decrypt(private_key_pem, ciphertext):
    """
    Decrypt ciphertext using a private key and return the plaintext.

    Args:
        private_key_pem (bytes): The private key in PEM format.
        ciphertext (bytes): The encrypted data.

    Returns:
        bytes: The plaintext.
    """
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None
    )

    # Extract the encrypted symmetric key from the ciphertext
    encrypted_symmetric_key = ciphertext[:256]  # Adjust the size based on your key size

    # Decrypt the symmetric key with the private key
    symmetric_key = private_key.decrypt(
        encrypted_symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(utils.hashes.SHA256()),
            algorithm=utils.hashes.SHA256(),
            label=None
        )
    )

    # Decrypt the data using the symmetric key
    plaintext = symmetric_key.decrypt(
        ciphertext[256:],
        padding.OAEP(
            mgf=padding.MGF1(utils.hashes.SHA256()),
            algorithm=utils.hashes.SHA256(),
            label=None
        )
    )

    return plaintext


def public_key_encrypt(public_key_pem, plaintext):
    """
    Encrypt plaintext using a public key and return the ciphertext.

    Args:
        public_key_pem (bytes): The public key in PEM format.
        plaintext (bytes): The data to be encrypted.

    Returns:
        bytes: The ciphertext.
    """
    public_key = serialization.load_pem_public_key(public_key_pem)

    # Generate a random symmetric key for data encryption
    symmetric_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    symmetric_key_pem = symmetric_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Encrypt the symmetric key with the public key
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key_pem,
        padding.OAEP(
            mgf=padding.MGF1(utils.hashes.SHA256()),
            algorithm=utils.hashes.SHA256(),
            label=None
        )
    )

    # Encrypt the data using the symmetric key
    cipher_text = symmetric_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(utils.hashes.SHA256()),
            algorithm=utils.hashes.SHA256(),
            label=None
        )
    )

    return encrypted_symmetric_key + cipher_text
