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


# Message Decrypt Algorithm
# 消息加解密接入指引
#   See: https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1419318479&lang=zh_CN


class PKCS7Encoder():
    """提供基于PKCS7算法的加解密接口"""

    def __init__(self):
        self.block_size = 32

    def encode(self, text):
        """ 对需要加密的明文进行填充补位
        @param text: 需要进行填充补位操作的明文
        @return: 补齐明文字符串
        """
        # 计算需要填充的位数
        amount_to_pad = self.block_size - (len(text) % self.block_size) or self.block_size
        # 获得补位所用的字符
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def decode(self, decrypted):
        """ 删除解密后明文的补位字符
        @param decrypted: 解密后的明文
        @return: 删除补位字符后的明文
        """
        pad = ord(decrypted[-1])
        if pad < 1 or pad > 32:
            pad = 0
        return decrypted[:-pad]


class Prpcrypt(object):
    """ 提供接收和推送给公众平台消息的加解密接口 """

    def __init__(self, key):
        self.key = key
        # 设置加解密模式为 AES 的 CBC 模式
        self.mode = AES.MODE_CBC

    def encrypt(self, appid, text, random_str=None):
        """ 对明文进行加密
        @param text: 需要加密的明文
        @return: 加密得到的字符串
        """
        # If Not Convert
        # Will raise ``UnicodeEncodeError: 'ascii' codec can't encode characters``
        text = to_binary(text)
        # 16 位随机字符串添加到明文开头
        text = '{0}{1}{2}{3}'.format(random_str if random_str else random_string(16), struct.pack('I', socket.htonl(len(text))), text, appid)
        # 使用自定义的填充方式对明文进行补位填充
        text = PKCS7Encoder().encode(text)
        # 加密
        ciphertext = AES.new(self.key, self.mode, self.key[:16]).encrypt(text)
        # 使用 BASE64 对加密后的字符串进行编码
        return base64.b64encode(ciphertext)

    def decrypt(self, text, appid):
        """ 对解密后的明文进行补位删除
        @param text: 密文
        @return: 删除填充补位后的明文
        """
        # 使用 BASE64 对密文进行解码，然后 AES-CBC 解密
        plain_text = AES.new(self.key, self.mode, self.key[:16]).decrypt(base64.b64decode(text))

        pad = ord(plain_text[-1])
        # 去除 16 位随机字符串
        content = plain_text[16:-pad]
        xml_len = socket.ntohl(struct.unpack('I', content[:4])[0])
        xml_content = content[4:xml_len + 4]
        from_appid = content[xml_len + 4:]

        if from_appid != appid:
            return None

        return xml_content


class WXBizMsgCrypt(object):
    # 构造函数
    # @param token: 公众平台上，开发者设置的 Token
    # @param encodingaeskey: 公众平台上，开发者设置的 EncodingAESKey
    # @param appid: 企业号的 AppId
    def __init__(self, appid, token, encodingaeskey):
        self.key = base64.b64decode(to_binary(encodingaeskey + '='))
        assert len(self.key) == 32
        self.appid = appid
        self.token = token

    def encrypt(self, resp_xml, nonce, timestamp=None, random_str=None):
        # 将公众号回复用户的消息加密打包
        # @param resp_xml: 企业号待回复用户的消息，xml 格式的字符串
        # @param timestamp: 时间戳，可以自己生成，也可以用 URL 参数的 timestamp, 如为 None 则自动用当前时间
        # @param nonce: 随机串，可以自己生成，也可以用 URL 参数的 nonce
        # return： EncryptMsg, 加密后的可以直接回复用户的密文，包括 msg_signature，timestamp, nonce, encrypt 的 xml 格式的字符串
        encrypt = Prpcrypt(self.key).encrypt(self.appid, resp_xml, random_str)
        if timestamp is None:
            timestamp = int(time.time())
        # 生成安全签名
        signature = calculate_msg_signature(self.token, str(timestamp), nonce, encrypt)
        return dict_to_xml(collections.OrderedDict([('Encrypt', encrypt), ('MsgSignature', signature), ('TimeStamp', int(timestamp)), ('Nonce', nonce)]), isdigit=False)

    def decrypt(self, encrypt, msg_signature, timestamp, nonce):
        # 检验消息的真实性，并且获取解密后的明文
        # @param data: 密文，对应 POST 请求的数据
        # @param msg_signature: 签名串，对应URL参数的 msg_signature
        # @param timestamp: 时间戳，对应URL参数的 timestamp
        # @param nonce: 随机串，对应 URL 参数的 nonce
        # @return: xml_content: 解密后的原文
        # 验证安全签名
        if not check_msg_signature(self.token, msg_signature, str(timestamp), nonce, encrypt):
            return None
        return Prpcrypt(self.key).decrypt(encrypt, self.appid)


def encrypt(appid, token=None, encodingaeskey=None, resp_xml=None, nonce=None, timestamp=None, random_str=None):
    if not encodingaeskey:
        return resp_xml
    return WXBizMsgCrypt(appid, token, encodingaeskey).encrypt(resp_xml, nonce, timestamp, random_str)


def decrypt(appid, token=None, encodingaeskey=None, post_data=None, encrypt=None, msg_signature=None, timestamp=None, nonce=None, xmltodict=False):
    if not encodingaeskey:
        return post_data
    if post_data and not encrypt:
        encrypt = xml_to_dict(post_data).get('Encrypt', '')
    xml = WXBizMsgCrypt(appid, token, encodingaeskey).decrypt(encrypt, msg_signature, timestamp, nonce)
    return xml_to_dict(xml) if xmltodict and xml else xml
