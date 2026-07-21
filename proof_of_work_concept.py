# The purpose of this program is to demonstrate how Proof-of-Work (PoW) algorithms works in Blockchain logic.

from hashlib import sha256

# Let the algorithm be that that hash of x * y ends in 0
# hash(x * y) = ac23dc...0



# Let x be a fixed value that a miner knows
x = 5

# Let y be a fixed value that the miner needs to verify using PoW hashing
y = 0



# This loop will hash for possible values of y until a hash ending in 0 is calculated.
# Note: This assumes that y >= 0 and y is a whole number.
while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0":
    y += 1
    # print(sha256(f'{x*y}'.encode()).hexdigest())

print(f'The solution is y = {y}')

# Prints: The solution is y = 21



'''
The PoW algorithm is designed to be difficult to find, and easy to verify.

Bitcoin uses HashCash PoW algorithm.
Miners race to solve the hash, and receive a transaction as reward.

The network can verify the solution easily, but the solution is still difficult to find.
'''