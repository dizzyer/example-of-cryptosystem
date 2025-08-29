# 循环群的阶是群中元素的个数，生成元g需要满足与模数q互素且对于任意小于群阶的值x有g^x!=1modq.判断方法是将群阶素数分解为q=p_1^k_1...p_tk_t,遍历g^{\phi(q)/p_i}看是否为1,若全不为1则说明是生成元
# 反证法可证，若全不为1但有g^d=1,d可整除q的某个最大因式,定有某个g^{\phi(q)/p_i}=1,矛盾
# 自己生成大素数并获得一个生成元太繁琐了，所以学习使用密码学库
import hashlib
from Cryptodome.Hash import MD5
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Signature import pkcs1_15


def md5_test():
    # md5_obj是计算MD5消息摘要的对象，可以调用update分块得哈希与得到摘要的字符串表示
    data = "abc"
    md5_obj = MD5.new(data.encode())
    md5_obj.update("def".encode())
    digest = md5_obj.hexdigest()
    print(digest)
    # e80b5017098950fc58aad83c8c14978e

    md5_obj = MD5.new("abcdef".encode())
    print(md5_obj.hexdigest())
    # e80b5017098950fc58aad83c8c14978e


# SHA256安全性比MD5更高，相应地，耗时也更长
def sha256_test():
    data = "abc"
    sha256_obj = SHA256.new(data.encode())
    sha256_obj.update("def".encode())
    digest = sha256_obj.hexdigest()
    print(digest)
    # bef57ec7f53a6d40beb640a780a639c83bc29ac8a9816f1fc6c5c6dcd93c4721

    sha256_obj = SHA256.new("abcdef".encode())
    print(sha256_obj.hexdigest())
    # bef57ec7f53a6d40beb640a780a639c83bc29ac8a9816f1fc6c5c6dcd93c4721

def rsa_test():
    # 先生成私钥key
    key = RSA.generate(1048)

    # 可以导出储存
    # sk = key.export_key()
    # with open("sk.pem", "wb") as fp:
    #     fp.write(sk)
    # pk = key.public_key().export_key()
    # with open("pk.pem", "wb") as fp:
    #     fp.write(pk)
    with open("sk.pem") as fp:
        sk = RSA.import_key(fp.read())
    with open("pk.pem") as fp:
        pk = RSA.import_key(fp.read())

    # 下述是加密测试
    cipher_rsa = PKCS1_OAEP.new(pk)
    data = "待加密数据"
    encrypted_data = cipher_rsa.encrypt(data.encode())

    cipher_rsa = PKCS1_OAEP.new(sk)
    decrypted_data = cipher_rsa.decrypt(encrypted_data)
    print(decrypted_data.decode())

    # 下述为签名测试，可以使用上面的私钥
    data = "待签名数据"
    signer = pkcs1_15.new(sk)
    hs = SHA256.new(data.encode())
    signature = signer.sign(hs)
    # 可以保存签名
    with open("signature", "wb") as fp:
        fp.write(signature)
    # 读取签名
    with open("signature", "rb") as fp:
        signature = fp.read()

    # 验证签名
    verifier = pkcs1_15.new(pk)
    print(verifier.verify(hs, signature))
    return decrypted_data


if __name__ == '__main__':
    rsa_test()
