from flask import Flask, request, jsonify
import tenseal as ts
import base64
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    return jsonify({"status": "HE Cloud API running"})

@app.route("/process_encrypted", methods=["POST"])
def process_encrypted():
    try:
        payload = request.get_json()
        context_b64 = payload.get("context_public")
        ciphertexts_b64 = payload.get("ciphertexts", [])

        if not context_b64 or not ciphertexts_b64:
            return jsonify({"error": "context_public and ciphertexts required"}), 400

        context_bytes = base64.b64decode(context_b64.encode("utf-8"))
        ctx = ts.context_from(context_bytes)

        enc_vectors = [ts.ckks_vector_from(ctx, base64.b64decode(cb64.encode("utf-8"))) for cb64 in ciphertexts_b64]

        res = enc_vectors[0]
        for e in enc_vectors[1:]:
            res += e

        res_bytes = res.serialize()
        res_b64 = base64.b64encode(res_bytes).decode("utf-8")

        return jsonify({"result_ciphertext": res_b64}), 200

    except Exception as e:
        app.logger.exception("Error in processing encrypted request")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Replit requires host="0.0.0.0" and port=3000
    app.run(host="0.0.0.0", port=3000)
