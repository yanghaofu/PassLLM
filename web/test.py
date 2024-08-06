from gmssl import sm3, func

def sm3_hash(data):
    data_bytes = data.encode('utf-8')
    hash_value = sm3.sm3_hash(func.bytes_to_list(data_bytes))
    return hash_value

data = "Hello, World!"
hash_value = sm3_hash(data)
print(f"SM3 hash of '{data}': {hash_value}")
