import numpy as np

const_seed = None
split_seed = None
bb_seed = None

class BlackBox:
    bits = 0
    zset = None
    split_rng = None
    const_rng = None
    bb_rng = None

    def __init__(self, n, split_seed=None, const_seed=None, bb_seed=None):
        self.bits = n
        self.split_rng = np.random.default_rng(split_seed)
        self.const_rng = np.random.default_rng(const_seed).integers(low=0, high=2, dtype=np.uint8)
        self.bb_rng = np.random.default_rng(bb_seed).integers(low=0, high=2, dtype=np.uint8)
        self.zset = self._generate_zset(n)

    def invoke(self, bitstring):
        if len(bitstring) != self.bits:
            return "Number of bits in the bitstring does not match the number of bits initialized."
        for bit in bitstring:
            if bit not in ["0", "1"]:
                return "Invalid bitstring provided."

        if self.bb_rng:
            value = self._constant_function(self.const_rng)
        else:
            value = self._balanced_function(bitstring, self.zset)

        return value
    
    def _generate_zset(self, n):
        zset = set(())
        while len(zset) < np.power(2, n-1):
            number = self.split_rng.integers(low=0, high=np.power(2, n), dtype=np.uint64)
            zset.add(number)

        return zset
    
    def _constant_function(self, ret_val):
        return ret_val

    def _balanced_function(self, bitstring, zset):
        num = int(bitstring, 2)
        if np.uint64(num) in zset:
            return 0
        else:
            return 1
        
black_box = BlackBox(5)
answer = black_box.invoke("10101")
print(answer)