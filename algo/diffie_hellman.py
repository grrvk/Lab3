import random
import sympy


class User:

    def __init__(self, id, name, private_key=None, public_key=None, temporary_public_key=None):
        self.id = id
        self.name = name
        self.private_key = private_key
        self.public_key = public_key
        self.temporary_public_key = temporary_public_key


def generate_random_prime(start=2, end=100):
    candidate = random.randint(start, end)
    prime = sympy.nextprime(candidate)
    return prime


def get_keys(users):
    prime_mod = generate_random_prime(1000, 10000)
    generator = random.randint(100000, 1000000)

    for u in users:
        u.private_key = random.randint(1000, 10000)
        u.public_key = pow(prime_mod, u.private_key, generator)

    for _ in range(len(users) - 2):
        for i, u in enumerate(users):
            index = (i + 1) % len(users)
            next_user = users[index]
            u.temporary_public_key = pow(next_user.public_key, u.private_key, generator)

        for u in users:
            u.public_key = u.temporary_public_key

    for i, u in enumerate(users):
        index = (i + 1) % len(users)
        next_user = users[index]
        u.private_key = pow(next_user.public_key, u.private_key, generator)

    return users
