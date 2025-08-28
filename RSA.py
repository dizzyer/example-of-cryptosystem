# 拓展的欧几里得求最大公因数,以及求逆元.根据gcd(a,b)=gcd(b,a%b),要求ax+by=gcd(a,b)的(x,y),若已知bx'+(a%b)y'=gcd(b,a%b)的x',y',
# 因为a%b=a-(a//b)*b,带入后得到x=y',y=x'-(a//b)*y',返回的是x、y、最大公因数,若r=1则x为a在模b下的逆元,y为b在模a下的逆元
def ext_gcd(a, b):
    if a % b == 0:
        return 0, 1, b
    else:
        x, y, r = ext_gcd(b, a % b)
        return y, x - (a // b) * y, r


def gen_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # e取小于phi且与之互素的值，常取下面的素数
    e = 65537
    x, y, r = ext_gcd(e, phi)

    # 若e无逆元
    if r != 1:
        return 0

    if x < 0:
        x = x + phi
    d = x
    return (n, e), (n, d)


# 加密 m是被加密的信息 加密成为c
def encrypt(m, pubkey):
    n = pubkey[0]
    e = pubkey[1]

    c = pow(m, e, n)
    return c


# 解密 c是密文，解密为明文m
def decrypt(c, selfkey):
    n = selfkey[0]
    d = selfkey[1]

    m = pow(c, d, n)
    return m


if __name__ == "__main__":
    p = 73
    q = 101
    pk, sk = gen_key(p, q)
    m = 67
    c = encrypt(m, pk)
    print("加密后为%s" % c)
    d = decrypt(c, sk)
    print("解密后为%s" % d)

# 上述参考了https://zhuanlan.zhihu.com/p/35614163