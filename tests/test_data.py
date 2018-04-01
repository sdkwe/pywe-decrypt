# -*- coding: utf-8 -*-

from pywe_decrypt.data import decrypt


class TestDataDecryptCommands(object):

    def test_decrypt(self):
        appId = 'wx4f4bc4dec97d474b'
        sessionKey = 'tiihtNczf5v6AKRyjwEUhQ=='
        encryptedData = 'CiyLU1Aw2KjvrjMdj8YKliAjtP4gsMZMQmRzooG2xrDcvSnxIMXFufNstNGTyaGS9uT5geRa0W4oTOb1WT7fJlAC+oNPdbB+3hVbJSRgv+4lGOETKUQz6OYStslQ142dNCuabNPGBzlooOmB231qMM85d2/fV6ChevvXvQP8Hkue1poOFtnEtpyxVLW1zAo6/1Xx1COxFvrc2d7UL/lmHInNlxuacJXwu0fjpXfz/YqYzBIBzD6WUfTIF9GRHpOn/Hz7saL8xz+W//FRAUid1OksQaQx4CMs8LOddcQhULW4ucetDf96JcR3g0gfRK4PC7E/r7Z6xNrXd2UIeorGj5Ef7b1pJAYB6Y5anaHqZ9J6nKEBvB4DnNLIVWSgARns/8wR2SiRS7MNACwTyrGvt9ts8p12PKFdlqYTopNHR1Vf7XjfhQlVsAJdNiKdYmYVoKlaRv85IfVunYzO0IKXsyl7JCUjCpoG20f0a04COwfneQAGGwd5oa+T8yO5hzuyDb/XcxxmK01EpqOyuxINew=='
        iv = 'r7BXXKkLb8qrSNn05n0qiA=='
        result = decrypt(appId, sessionKey=sessionKey, encryptedData=encryptedData, iv=iv)
        # {u'avatarUrl': u'http://wx.qlogo.cn/mmopen/vi_32/aSKcBBPpibyKNicHNTMM0qJVh8Kjgiak2AHWr8MHM4WgMEm7GFhsf8OYrySdbvAMvTsw3mo8ibKicsnfN5pRjl1p8HQ/0',
        #  u'city': u'Guangzhou',
        #  u'country': u'CN',
        #  u'gender': 1,
        #  u'language': u'zh_CN',
        #  u'nickName': u'Band',
        #  u'openId': u'oGZUI0egBJY1zhBYw2KhdUfwVJJE',
        #  u'province': u'Guangdong',
        #  u'unionId': u'ocMvos6NjeKLIBqg5Mr9QjxrP1FA',
        #  u'watermark': {u'appid': u'wx4f4bc4dec97d474b', u'timestamp': 1477314187}}
        assert isinstance(result, dict)
        assert result['unionId'] == 'ocMvos6NjeKLIBqg5Mr9QjxrP1FA'
        assert result['openId'] == 'oGZUI0egBJY1zhBYw2KhdUfwVJJE'
        assert result['watermark']['appid'] == appId
