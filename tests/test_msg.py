# -*- coding: utf-8 -*-

from pywe_decrypt.msg import decrypt, encrypt


class TestMsgDecryptCommands(object):

    def test_msg_encrypt(self):
        appid = 'wx2c2769f8efd9abc2'
        token = 'spamtest'
        encodingaeskey = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG'
        resp_xml = """<xml><ToUserName><![CDATA[oia2TjjewbmiOUlr6X-1crbLOvLw]]></ToUserName><FromUserName><![CDATA[gh_7f083739789a]]></FromUserName><CreateTime>1407743423</CreateTime><MsgType><![CDATA[video]]></MsgType><Video><MediaId><![CDATA[eYJ1MbwPRJtOvIEabaxHs7TX2D-HV71s79GUxqdUkjm6Gs2Ed1KF3ulAOA9H1xG0]]></MediaId><Title><![CDATA[testCallBackReplyVideo]]></Title><Description><![CDATA[testCallBackReplyVideo]]></Description></Video></xml>"""
        nonce = '1320562132'
        timestamp = '1522293145'
        random_str = 'qcN32VnjIO1AyoK6'
        final_xml = """<xml>
<Encrypt><![CDATA[uijfjEoMaaAFUyFtcsb+rDHOQMcG5Nf2m6NamFP45zJvUDePO/SUJDux9pHR8HkXbqC4+RSBJ0UB5PchQgEqwsGTeqlh9L4S1MeBRDdHrPjKUkOd6blj5IB/yvlNnpxFLc/WADBTH0NaEUWCCCg5+hAjlh9L/Gf95t/9IsR3xiMdYEw5uTClx2gp4RxCDxtKDxlEfZ+6Y2EckAwuSzpWUWzFrU7qOkrLsPxErtXXgLfvuzFlrWXkaxJpJBPaUtrtzBkztQx4cRawzItYiWQkdVoEQhK615XPPpnu1VXMQWsktAAjl7WzrQvKBEY0k8/KAMmgGCcY17m68NBL/PprdTiY237JKnIpSEw/Okv15ybB93ZK2OfX16nU0DFxioKYWTYRdtyM7VvBT4GPBAIZ4pRrZqRrwkytBIXjPJZX6vkrPCcyzfGr9cjqahKXwjNhFzhpNq7FLeKYl1XBAdCU/vohYTLs46sYAMxpO/UzY0ysm4fF6umlEuZd9bUWm6F/KYsS5MpzcwrEVEKkb/ZVwzSC8pMEyfbb3Wo5iB4tvJoIbFdSbcT8C5+AEzHM8HT0iiSRJcjwDrpVi45enJf/M+LNGKiLHFfP4k1N2htiQU/GAOnW3k6SgK5YL560JoWb]]></Encrypt>
<MsgSignature><![CDATA[683d0ec2dc7701b598a65341de44aab7e7077346]]></MsgSignature>
<TimeStamp>1522293145</TimeStamp>
<Nonce><![CDATA[1320562132]]></Nonce>
</xml>"""
        result = encrypt(appid, token, encodingaeskey, resp_xml, nonce, timestamp, random_str)
        print result
        assert result == final_xml

    def test_msg_decrypt(self):
        appid = 'wx2c2769f8efd9abc2'
        token = 'spamtest'
        encodingaeskey = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG'
        post_data = """<xml><ToUserName><![CDATA[gh_10f6c3c3ac5a]]></ToUserName><FromUserName><![CDATA[oyORnuP8q7ou2gfYjqLzSIWZf0rs]]></FromUserName><CreateTime>1409735668</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[abcdteT]]></Content><MsgId>6054768590064713728</MsgId><Encrypt><![CDATA[hyzAe4OzmOMbd6TvGdIOO6uBmdJoD0Fk53REIHvxYtJlE2B655HuD0m8KUePWB3+LrPXo87wzQ1QLvbeUgmBM4x6F8PGHQHFVAFmOD2LdJF9FrXpbUAh0B5GIItb52sn896wVsMSHGuPE328HnRGBcrS7C41IzDWyWNlZkyyXwon8T332jisa+h6tEDYsVticbSnyU8dKOIbgU6ux5VTjg3yt+WGzjlpKn6NPhRjpA912xMezR4kw6KWwMrCVKSVCZciVGCgavjIQ6X8tCOp3yZbGpy0VxpAe+77TszTfRd5RJSVO/HTnifJpXgCSUdUue1v6h0EIBYYI1BD1DlD+C0CR8e6OewpusjZ4uBl9FyJvnhvQl+q5rv1ixrcpCumEPo5MJSgM9ehVsNPfUM669WuMyVWQLCzpu9GhglF2PE=]]></Encrypt></xml>"""
        msg_signature = '5d197aaffba7e9b25a30732f161a50dee96bd5fa'
        timestamp = '1409735669'
        nonce = '1320562132'
        final_xml = """<xml><ToUserName><![CDATA[gh_10f6c3c3ac5a]]></ToUserName>
<FromUserName><![CDATA[oyORnuP8q7ou2gfYjqLzSIWZf0rs]]></FromUserName>
<CreateTime>1409735668</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[abcdteT]]></Content>
<MsgId>6054768590064713728</MsgId>
</xml>"""
        result = decrypt(appid, token, encodingaeskey, post_data=post_data, encrypt=None, msg_signature=msg_signature, timestamp=timestamp, nonce=nonce)
        assert result == final_xml
