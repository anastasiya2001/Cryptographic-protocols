import random

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
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

def generate_keys(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537

    d = mod_inverse(e, phi_n)

    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Модульная инверсия не существует')
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
    bits = int(input("Введите количество бит для генерации ключей (не более 1024 бит): "))
    if bits <= 0 or bits > 1024:
        print("Некорректное количество бит.")
        return

    # Генерация ключей для Алисы и Боба
    alice_public_key, alice_private_key = generate_keys(bits)
    bob_public_key, bob_private_key = generate_keys(bits)

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
