# -*- coding: utf-8 -*-

import base64
import json

from Crypto.Cipher import AES


# Decrypt Algorithm
#   See: https://mp.weixin.qq.com/debug/wxadoc/dev/api/signature.html


class WXBizDataCrypt:
    def __init__(self, appid, sessionKey):
        self.appid = appid
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appid:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


def decrypt(appid, sessionKey=None, encryptedData=None, iv=None):
    return WXBizDataCrypt(appid, sessionKey).decrypt(encryptedData, iv)
