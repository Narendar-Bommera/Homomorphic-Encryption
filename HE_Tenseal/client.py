import tenseal as ts
import base64
import pickle
import os

# ========== PATH FIX (Absolute paths work anywhere) ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # HE_Tenseal folder
CONTEXT_DIR = os.path.join(BASE_DIR, "context")
CIPHER_DIR = os.path.join(BASE_DIR, "cipher_store")

PUBLIC_CTX = os.path.join(CONTEXT_DIR, "public.ctx")
SECRET_CTX = os.path.join(CONTEXT_DIR, "secret.ctx")
ENCRYPTED_PKL = os.path.join(CIPHER_DIR, "encrypted_b64.pkl")

# Ensure cipher store folder exists
os.makedirs(CIPHER_DIR, exist_ok=True)

# ========== CREATE CONTEXT IF NOT EXISTS ==========
def create_context():
    if not os.path.exists(PUBLIC_CTX) or not os.path.exists(SECRET_CTX):
        print("🔑 Generating new CKKS context...")
        context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60]
        )
        context.generate_galois_keys()
        context.global_scale = 2 ** 40

        # Save public context
        with open(PUBLIC_CTX, "wb") as f:
            f.write(context.serialize(save_secret_key=False))

        # Save secret context
        with open(SECRET_CTX, "wb") as f:
            f.write(context.serialize())

        print("Context generated and stored successfully! 🔥")

# ========== ENCRYPT FUNCTION ==========
def encrypt_numbers(numbers):
    create_context()  # ensure context exists

    with open(PUBLIC_CTX, "rb") as f:
        public_ctx_bytes = f.read()

    ctx = ts.context_from(public_ctx_bytes)
    ctx.global_scale = 2 ** 40

    vec = ts.ckks_vector(ctx, numbers)
    encrypted_bytes = vec.serialize()
    encrypted_b64 = base64.b64encode(encrypted_bytes).decode("utf-8")

    # store ciphertext locally for multi_client.py
    with open(ENCRYPTED_PKL, "wb") as f:
        pickle.dump([encrypted_b64], f)

    return encrypted_b64

# ========== EXPORT FUNCTION CALLED FROM FRONTEND ==========
def send_to_cloud(numbers):
    print(f"🔐 Encrypting values: {numbers}")
    ciphertext_b64 = encrypt_numbers(numbers)
    print("📦 Encryption complete, written to cipher_store/encrypted_b64.pkl")
    return ciphertext_b64
