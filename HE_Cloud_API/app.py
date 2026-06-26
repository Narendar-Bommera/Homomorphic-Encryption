
from flask import Flask, request, jsonify
from flask_cors import CORS
import tenseal as ts
import os
import base64


app = Flask(__name__)
CORS(app)

# context path
CONTEXT_DIR = os.path.join(os.path.dirname(__file__), "context")
os.makedirs(CONTEXT_DIR, exist_ok=True)
PUBLIC_CTX_FILE = os.path.join(CONTEXT_DIR, "public.ctx")
SECRET_CTX_FILE = os.path.join(CONTEXT_DIR, "secret.ctx")

# generate CKKS context if not exists
if not os.path.exists(PUBLIC_CTX_FILE) or not os.path.exists(SECRET_CTX_FILE):
    print("🔑 Generating new CKKS context...")
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2**40
    context.generate_galois_keys()
    context.generate_relin_keys()
    # save contexts
    with open(PUBLIC_CTX_FILE, "wb") as f:
        f.write(context.serialize(save_secret_key=False))
    with open(SECRET_CTX_FILE, "wb") as f:
        f.write(context.serialize(save_secret_key=True))
else:
    print("🔑 Loading existing CKKS context...")
    context = ts.context_from(open(PUBLIC_CTX_FILE, "rb").read())

def encrypt_number(number, ctx):
    vec = ts.ckks_vector(ctx, [number])
    return base64.b64encode(vec.serialize()).decode("utf-8")

def decrypt_number(encrypted_b64):
    with open(SECRET_CTX_FILE, "rb") as f:
        secret_ctx = ts.context_from(f.read())
    enc = ts.ckks_vector_from(secret_ctx, base64.b64decode(encrypted_b64.encode()))
    return enc.decrypt()[0]

@app.route("/process", methods=["POST"])
def process_numbers():
    try:
        data = request.get_json()
        numbers = data.get("numbers", [])
        if len(numbers) != 3:
            return jsonify({"error": "Please send exactly 3 numbers"}), 400

        print("Received numbers:", numbers)

        # Encrypt each number
        encrypted_list = [encrypt_number(float(x), context) for x in numbers]
        print("Encrypted values:", encrypted_list)

        # Homomorphic sum
        enc_vecs = [ts.ckks_vector_from(context, base64.b64decode(e.encode())) for e in encrypted_list]
        enc_sum = enc_vecs[0] + enc_vecs[1] + enc_vecs[2]
        encrypted_sum_b64 = base64.b64encode(enc_sum.serialize()).decode("utf-8")

        # Decrypt locally for demo
        decrypted_sum = decrypt_number(encrypted_sum_b64)

        return jsonify({
            "encrypted_numbers": encrypted_list,
            "encrypted_sum": encrypted_sum_b64,
            "decrypted_sum": decrypted_sum
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
