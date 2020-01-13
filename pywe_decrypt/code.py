# -*- coding: utf-8 -*-

import base64
import collections
import socket
import struct
import time

from Crypto.Cipher import AES
from pywe_sign import calculate_msg_signature, check_msg_signature
from pywe_utils import random_string, to_binary
from pywe_xml import dict_to_xml, xml_to_dict


# Market Code Decrypt Algorithm
# 二维码包解密说明
#   See: https://developers.weixin.qq.com/doc/offiaccount/Unique_Item_Code/Unique_Item_Code_API_Documentation.html


class Prpcrypt(object):
    def __init__(self, key):
        self.key = key
        # 设置加解密模式为 AES 的 CBC 模式
        self.mode = AES.MODE_CBC

    def decrypt(self, text):
        # 使用 BASE64 对密文进行解码，然后 AES-CBC 解密
        plain_text = AES.new(self.key, self.mode, self.key[:16]).decrypt(base64.b64decode(text))
        # 去除 16 位随机字符串
        return plain_text[16:-ord(plain_text[-1])]


def decrypt(encryptedData=None, iv=None):
    return Prpcrypt(iv).decrypt(encryptedData)
