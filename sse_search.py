import pandas as pd
from Crypto.Cipher import AES
from Crypto.Hash import MD5
# import time

def build_codeword(ID, trapdoor):
    ID_bytes = str(ID).encode('utf-8')  # Convert ID to bytes
    ID_index = MD5.new()
    ID_index.update(ID_bytes)
    ECB_cipher = AES.new(trapdoor, AES.MODE_ECB)
    return ECB_cipher.encrypt(ID_index.digest()).hex()


def search_index(document, trapdoor):
    search_result = []
    data_index = pd.read_csv(document)
    data_index = data_index.values
    # start_time = time.time()
    for row in range(data_index.shape[0]):
        if build_codeword(row, trapdoor) in data_index[row]:
            search_result.append(row)

    # print time.time() - start_time
    return search_result

if __name__ == "__main__":
    index_file_name = input("Please input the index file you want to search:  ")
    keyword_trapdoor = input("Please input the file storing the trapdoor you want to search:  ")
    with open(keyword_trapdoor, 'rb') as f:
        trapdoor = f.read()

    search_result = search_index(index_file_name, trapdoor)
    print ("The identifiers of files that contain the keyword are: \n", search_result)




