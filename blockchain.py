import hashlib, json, time, os

class Blockchain:
    def __init__(self, filename="blockchain_data.json"):
        self.chain = []
        self.filename = filename
        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    self.chain = json.load(f)
                except:
                    self.chain = []
        if not self.chain:
            self.create_block(previous_hash="0", data="Genesis Block")

    def create_block(self, data, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.ctime(),
            "data": data,
            "previous_hash": previous_hash,
            "hash": self.hash_block(len(self.chain)+1, data, previous_hash)
        }
        self.chain.append(block)
        self.save_chain()
        return block

    def hash_block(self, index, data, previous_hash):
        block_string = str(index) + str(data) + previous_hash
        return hashlib.sha256(block_string.encode()).hexdigest()

    def get_last_block(self):
        return self.chain[-1]

    def save_chain(self):
        with open(self.filename, "w") as f:
            json.dump(self.chain, f, indent=4)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i-1]
            curr = self.chain[i]
            if curr["previous_hash"] != prev["hash"]:
                return False
            check_hash = self.hash_block(curr["index"], curr["data"], curr["previous_hash"])
            if check_hash != curr["hash"]:
                return False
        return True
