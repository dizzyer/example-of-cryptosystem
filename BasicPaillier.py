import math
import random
from gmpy2 import invert


# 生成m以内的素数序列,range前闭后开，该函数包括m
def primes_in_range(m):
    is_prime = [True]*(m+1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, math.isqrt(m)+1):
        if is_prime[i]:
            for j in range(i*i, m+1, i):
                is_prime[j] = False
    prime_list = [i for i in range(2, m+1) if is_prime[i]]
    return prime_list


def encrypt(plainText, g, r, n):
    return int((pow(g, plainText, pow(n, 2)) * pow(r, n, pow(n, 2))) % pow(n, 2))


def decrypt(cipher, ld, n, u):
    return ((pow(cipher, ld, pow(n, 2))-1)/n * u) % n


if __name__ == '__main__':
    prime = primes_in_range(50)
    # 得到两个素数p,q
    p = random.choice(prime)
    while 1:
        q = random.choice(prime)
        if p != q:
            if math.gcd(p*q, (p-1)*(q-1)) == 1:
                break
    # n, ld
    n = p * q
    ld = math.lcm(p - 1, q - 1)
    g = n + 1
    v = (pow(g, ld)-1) % pow(n, 2)//n
    u = invert(v, n)
    print("此次的随机数p = {}, q = {}".format(p, q))
    print("可求得公钥为({}, {}), 私钥为({}, {})".format(n, g, ld, u))

    # 测试, 输入明文
    plaintext1 = random.randint(1, n - 1)
    plaintext2 = random.randint(1, n - 1)
    print("plaintext1 :", plaintext1)
    print("plaintext2 :", plaintext2)

    r1 = random.randint(1, n - 1)
    gcd1 = math.gcd(r1, n)
    while gcd1 != 1:  # 循环直到r1与n互素
        r1 = random.randint(1, n - 1)
        gcd1 = math.gcd(r1, n)
    print("随机数r1为：", r1)
    r2 = random.randint(1, n - 1)
    gcd2 = math.gcd(r2, n)
    while gcd2 != 1:  # 循环直到r1与n互素
        r2 = random.randint(1, n - 1)
        gcd2 = math.gcd(r2, n)
    print("随机数r2为：", r2)

    # 求密文
    cipher1 = encrypt(plaintext1, g, r1, n)
    cipher2 = encrypt(plaintext2, g, r2, n)
    print('plaintext1 加密得 cipher1 :', cipher1)
    print('plaintext2 加密得 cipher2 :', cipher2)

    # 求明文
    M1 = decrypt(cipher1, ld, n, u)
    M2 = decrypt(cipher2, ld, n, u)
    print('cipher1解密结果为 :', M1)
    print('cipher2解密结果为 :', M2)

    print("----------------------同态加法----------------------")
    cipher3 = (cipher1 * cipher2) % pow(n, 2)
    print('cipher1 * cipher2 =', cipher3)
    print('plaintext1 + plaintext2 加密得 :', encrypt((plaintext1 + plaintext2) % n, g, r1 * r2, n) % pow(n, 2))

    M3 = decrypt(cipher3, ld, n, u)
    print('cipher1 * cipher2解密结果为 :', M3)
    print('plaintext1 + plaintext2为 :', (plaintext1 + plaintext2) % n)

    print("----------------------同态乘法----------------------")
    cipher4 = pow(cipher1, plaintext2) % pow(n, 2)
    print('cipher1的plaintext次方为 :', cipher4)
    print('plaintext1 * plaintext2 加密得 :',
          encrypt((plaintext1 * plaintext2) % n, g, pow(r1, plaintext2), n) % pow(n, 2))

    M4 = decrypt(cipher4, ld, n, u)
    print('cipher1的plaintext次方的解密结果=', M4)
    print('plaintext1 * plaintext2为 :', (plaintext1 * plaintext2) % n)
