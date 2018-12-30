import random

BASE = [0, 376]
PUBLIC_KEY = [256, 342]
PRIVATE_KEY = 705
ELLIPTIC_COEFFICIENTS = [-1, 188]
N = 751
K = 20


def elliptic_curve_power(d, p):
    if d == 1:
        return p
    result = elliptic_curve_power(int(d / 2), p)
    result = add(result, result)
    if d % 2:
        result = add(result, p)
    return result


def power_modulo(x, n):
    if n <= 0:
        return 1
    return (power_modulo(x, n - 1) * (x % N)) % N


def is_quadratic_residue(x):
    return power_modulo(x, int((N - 1) / 2)) == 1


def xgcd(a, b):
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def get_opposite(x):
    _, res, _ = xgcd(x, N)
    return res


def get_lambda(p, q):
    try:
        if (p[0] == q[0]) and (p[1] == q[1]):
            return ((3 * p[0] * p[0] + int(ELLIPTIC_COEFFICIENTS[0])) * (get_opposite(2 * p[1]))) % N
        else:
            return (int(q[1] - p[1]) * get_opposite((q[0] - p[0]) % N)) % N
    except Exception as e:
        exit(1)


def add(p: list, q: list) -> list:
    lamda = get_lambda(p, q)
    res = []
    res.append(((lamda ** 2) - (p[0] + q[0])) % N)
    res.append((lamda * (p[0] - res[0]) - p[1]) % N)
    return res


def elliptic_func(x):
    return ((x ** 3) + ELLIPTIC_COEFFICIENTS[0] * x + ELLIPTIC_COEFFICIENTS[1]) % N


def get_not_quadratic():
    for i in range(2, N):
        if not is_quadratic_residue(i):
            return i
    return 0


def compute_quadratic(a):
    alpha = 1
    s = (N - 1) / (power_modulo(2, alpha))
    n = get_not_quadratic()
    r = power_modulo(a, int((s + 1) / 2))
    b = power_modulo(n, s)
    jey = 1
    return (power_modulo(b, jey) * r) % N


def p_m(m):
    for i in range(1, K):
        if is_quadratic_residue(elliptic_func(m * K + i)):
            return [m * K + i, compute_quadratic(elliptic_func(m * K + i))]


def encrypt_character(c):
    k = random.randint(2, N - 1)
    return elliptic_curve_power(k, BASE), add(p_m(c), elliptic_curve_power(k, PUBLIC_KEY))


def encrypt_message(msg):
    msg = msg.replace(' ', '')
    encrypted_message = []
    for c in msg:
        encrypted_message.append(encrypt_character((ord(c) - ord('a') + 1)))

    return encrypted_message


def decrypt_character(cipher):
    x = elliptic_curve_power(PRIVATE_KEY, cipher[0])
    res = add(cipher[1], [x[0], -x[1]])
    return chr(ord('a') + int((res[0] - 1) / K) - 1)


def decrypt_message(cipher_message):
    msg = ""
    for pair in cipher_message:
        msg += decrypt_character(pair)

    return msg


msg = "your_private_key_is_seven_hundred_and_five"

for pair in encrypt_message(msg):
    for s in pair:
        print(s[0], s[1], end=' ', file=open("cipher_text.txt", "a"))
    print(file=open("cipher_text.txt", "a"))

print(decrypt_message(encrypt_message(msg)))
