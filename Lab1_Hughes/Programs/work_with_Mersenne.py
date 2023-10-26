import random
import math
import time

class MyMersenneTwister:
    def __init__(self, seed=None):
        if seed is None:
            seed = int(time.time()) & 0xFFFFFFFF
        self.MT = [0] * 624
        self.index = 0
        self.initialize(seed)

    def initialize(self, seed):
        self.MT[0] = seed
        for i in range(1, 624):
            prev_value = self.MT[i - 1]
            next_value = 0x6C078965 * (prev_value ^ (prev_value >> 30)) + i
            self.MT[i] = next_value & 0xFFFFFFFF

    def generate_bits(self, bits):
        result = 0
        for _ in range(math.ceil(bits / 32)):
            if self.index == 0:
                self.generate_numbers()
            word = self.MT[self.index]
            self.index = (self.index + 1) % 624

            result = (result << 32) | word

        return result >> (32 - (bits % 32))

    def generate_numbers(self):
        for i in range(624):
            y = (self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7FFFFFFF)
            self.MT[i] = self.MT[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.MT[i] = self.MT[i] ^ 0x9908B0DF

def generate_large_random(bits, rng):
    num = 0
    num_bits = 0
    while num_bits < bits:
        next_bits = rng.generate_bits(min(bits - num_bits, 32))
        num = (num << min(bits - num_bits, 32)) | next_bits
        num_bits += min(bits - num_bits, 32)
    return num



def generate_prime(bits, rng):
    while True:
        num = generate_large_random(bits, rng)
        num |= 1  # Ensure it's odd
        if is_prime(num):
            return num


def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True

    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False

    return True

def generate_keys(bits, rng):
    p = generate_prime(bits, rng)
    q = generate_prime(bits, rng)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537  # Common choice for the public exponent

    d = mod_inverse(e, phi_n)

    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def encrypt(message, public_key):
    n, e = public_key
    return pow(message, e, n)

def decrypt(ciphertext, private_key):
    n, d = private_key
    return pow(ciphertext, d, n)

def main():
    rng = MyMersenneTwister()

    bits = int(input("Введите количество бит для генерации ключей (не более 1024 бит): "))
    if bits <= 0 or bits > 1024:
        print("Некорректное количество бит.")
        return

    # Генерация ключей для Алисы и Боба
    alice_public_key, alice_private_key = generate_keys(bits, rng)
    bob_public_key, bob_private_key = generate_keys(bits, rng)

    print("Публичный ключ Алисы (n, e):", alice_public_key)
    print("Приватный ключ Алисы (n, d):", alice_private_key)
    print("Публичный ключ Боба (n, e):", bob_public_key)
    print("Приватный ключ Боба (n, d):", bob_private_key)

    # Алиса шифрует сообщение
    message = int(input("Введите сообщение, которое Алиса хочет отправить: "))
    encrypted_message = encrypt(message, bob_public_key)

    # Боб дешифрует сообщение
    decrypted_message = decrypt(encrypted_message, bob_private_key)

    print("Зашифрованное сообщение, отправленное от Алисы к Бобу:", encrypted_message)
    print("Расшифрованное сообщение Боба:", decrypted_message)

    if message == decrypted_message:
        print("Сообщение было успешно зашифровано и расшифровано.")
    else:
        print("Ошибка при шифровании и/или расшифровании сообщения.")

if __name__ == "__main__":
    main()
