# pywe-decrypt

Wechat Decrypt Module for Python.

# Installation

```shell
pip install pywe-decrypt
```

# Usage

```python
from pywe_decrypt.data import decrypt
from pywe_decrypt.msg import decrypt, encrypt
```

# Method

```python
def decrypt(appId, sessionKey=None, encryptedData=None, iv=None):

def encrypt(appid, token=None, encodingaeskey=None, resp_xml=None, nonce=None, timestamp=None, random_str=None):

def decrypt(appid, token=None, encodingaeskey=None, post_data=None, encrypt=None, msg_signature=None, timestamp=None, nonce=None):
```
