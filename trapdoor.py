from Crypto.Cipher import AES
from Crypto.Hash import MD5


def build_trapdoor(MK, keyword):
    keyword_bytes = str(keyword).encode('utf-8')
    keyword_index = MD5.new()
    keyword_index.update(keyword_bytes)
    ECB_cipher = AES.new(MK, AES.MODE_ECB)
    return ECB_cipher.encrypt(keyword_index.digest())

if __name__ == "__main__":

    keyword = input("Please input the keyword you want to search:  ")

    master_key_file_name = input("Please input the file storing the master key:  ")
    with open(master_key_file_name, 'rb') as f:
        master_key = f.read(16)  # Read 16 bytes of the master key

    trapdoor_file = open(keyword + "_trapdoor", "wb+")  # Open in binary mode
    trapdoor_of_keyword = build_trapdoor(master_key, keyword)
    trapdoor_file.write(trapdoor_of_keyword)
    trapdoor_file.close()

