# Major_Project/HE_Tenseal/client_decrypt.py
import tenseal as ts
import base64
import os

# Render:"https://he-cloud-api-charan.onrender.com/"
# Replit:"https://2ace41bb-2284-4465-89c6-dc82d39a0862-00-1bpol0xejx2yp.pike.repl.co/"

def decrypt_result_from_b64(result_b64):
    # load secret context
    with open("cipher_store/context_secret.bin", "rb") as f:
        ctx = ts.context_from(f.read())

    res_bytes = base64.b64decode(result_b64.encode("utf-8"))
    enc = ts.ckks_vector_from(ctx, res_bytes)
    dec = enc.decrypt()  # returns list of floats
    return dec

if __name__ == "__main__":
    print("Paste the result_ciphertext base64 string you received from cloud (or type 'file'):")
    b64 = input("result_ciphertext (paste): ").strip()
    if b64.lower() == "file":
        path = input("Enter path to file containing base64: ").strip()
        with open(path, "r") as f:
            b64 = f.read().strip()
    if not b64:
        print("No input provided. Exiting.")
        raise SystemExit(1)
    dec = decrypt_result_from_b64(b64)
    print("Decrypted (approx):", dec)
    if len(dec) == 1:
        print("Final value (rounded):", round(dec[0], 6))
