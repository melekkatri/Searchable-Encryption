import pandas as pd
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Random import get_random_bytes
import numpy as np
import time


def build_trapdoor(MK, keyword):
    keyword_index = MD5.new()
    keyword_index.update(str(keyword).encode('utf-8'))  # Convert to string and encode to bytes
    ECB_cipher = AES.new(MK, AES.MODE_ECB)
    return ECB_cipher.encrypt(keyword_index.digest())


def build_codeword(ID, trapdoor):
    ID_index = MD5.new()
    ID_index.update(str(ID).encode('utf-8'))  # Convert to string and encode to bytes
    ECB_cipher = AES.new(trapdoor, AES.MODE_ECB)
    return ECB_cipher.encrypt(ID_index.digest()).hex()  # Use hex() to get hex representation



def build_codeword(ID, trapdoor):
    ID_index = MD5.new()
    ID_index.update(str(ID).encode('utf-8'))  # Encode ID to bytes
    ECB_cipher = AES.new(trapdoor, AES.MODE_ECB)
    return ECB_cipher.encrypt(ID_index.digest()).hex()  # Use hex() to get hex representation


def build_index(MK, ID, keyword_list):
    secure_index = [0] * len(keyword_list)
    for i, keyword in enumerate(keyword_list):
        codeword = build_codeword(ID, build_trapdoor(MK, keyword))
        secure_index[i] = codeword
    np.random.shuffle(secure_index)  # Use numpy random.shuffle
    return secure_index


def searchable_encryption(raw_data_file_name, master_key, keyword_type_list):
    raw_data = pd.read_csv(raw_data_file_name)
    features = list(raw_data)
    raw_data = raw_data.values

    keyword_number = [i for i in range(0, len(features)) if features[i] in keyword_type_list]

    index_header = ["index_" + str(i) for i in range(1, len(keyword_type_list) + 1)]

    document_index = []
    start_time = time.time()
    for row in range(raw_data.shape[0]):
        record = raw_data[row]
        record_keyword_list = [record[i] for i in keyword_number]
        record_index = build_index(master_key, row, record_keyword_list)
        document_index.append(record_index)

    time_cost = time.time() - start_time
    print(time_cost)
    document_index_dataframe = pd.DataFrame(np.array(document_index), columns=index_header)
    document_index_dataframe.to_csv(raw_data_file_name.split(".")[0] + "_index.csv")


if __name__ == "__main__":
    document_name = input("Please input the file to be encrypted:  ")

    master_key_file_name = input("Please input the file stored the master key:  ")
    with open(master_key_file_name, 'rb') as f:
        master_key = f.read(16)  # Read 16 bytes of the master key

    keyword_list_file_name = input("please input the file stores keyword type:  ")
    with open(keyword_list_file_name, 'r') as f:
        keyword_type_list = f.read().split(",")  # Split into a list of keywords

    searchable_encryption(document_name, master_key, keyword_type_list)

    print("Finished")
