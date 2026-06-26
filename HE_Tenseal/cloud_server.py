import tenseal as ts
import pickle

def compute_encrypted_sum():
    # Load public context
    with open("cipher_store/context_public.bin", "rb") as f:
        ctx = ts.context_from(f.read())

    # Load encrypted vectors
    with open("cipher_store/encrypted_data.pkl", "rb") as f:
        encrypted_vectors = pickle.load(f)

    # Deserialize encrypted numbers
    encrypted_numbers = [ts.ckks_vector_from(ctx, data) for data in encrypted_vectors]

    # Compute encrypted sum
    encrypted_sum = encrypted_numbers[0]
    for enc in encrypted_numbers[1:]:
        encrypted_sum += enc

    # Save result
    with open("cipher_store/result_sum.bin", "wb") as f:
        f.write(encrypted_sum.serialize())

    print("✅ Cloud: Computed encrypted sum and saved to 'cipher_store/result_sum.bin'")

if __name__ == "__main__":
    compute_encrypted_sum()
