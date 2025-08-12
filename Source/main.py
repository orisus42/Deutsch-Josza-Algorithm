from platform import python_version
import qiskit
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
    eval_count = 0

    def __init__(self, n, split_seed=None, const_seed=None, bb_seed=None):
        self.bits = n
        self.split_rng = np.random.default_rng(split_seed)
        self.const_rng = np.random.default_rng(const_seed).integers(low=0, high=2, dtype=np.uint8)
        self.bb_rng = 0 # np.random.default_rng(bb_seed).integers(low=0, high=2, dtype=np.uint8)
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

        self.eval_count+=1
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
    
    def test(self, guess):
        if "constant" in guess.lower() and self.bb_rng == 1:
            return "correct"
        elif "balanced" in guess.lower() and self.bb_rng == 0:
            return "correct"
        else:
            return "incorrect"
        
    def reset(self):
        self.eval_count = 0
        
    def reveal_function(self):
        if self.bb_rng:
            return "constant"
        else:
            return "balanced"
        
def classical_rng_solver(black_box, seed=None):
    outputs = []
    balanced = 0
    for i in range(np.pow(2, black_box.bits-1)+1):
        guess = np.random.default_rng(seed).integers(low=0, high=np.power(2, black_box.bits), dtype=np.uint64)
        string = format(guess, 'b')
        if len(string) != black_box.bits:
            string = "0"*(black_box.bits - len(string))+string
        out = black_box.invoke(string)
        outputs.append(out)
        if 1 in outputs and 0 in outputs:
            balanced = 1
            break
    
    if balanced:
        score = black_box.test("balanced")
    else:
        score = black_box.test("constant")

    # print(f"The tests were {score}! Invocations of the black box required: {black_box.eval_count}")
    invocations = black_box.eval_count
    black_box.reset()
    return black_box.reveal_function(), invocations

counts = []

for i in range(10000):
    black_box = BlackBox(10)
    func, count = classical_rng_solver(black_box)
    counts.append(count)

print(f"Maximum counts required for balanced function: {max(counts)}")