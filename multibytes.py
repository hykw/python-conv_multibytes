#!/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (division, print_function, absolute_import, unicode_literals)

import unicodedata
import zenhan

import jctconv

class BaseBytes(object):
    @staticmethod
    def convert2unicode(strings):
        """ 引数を unicode にする。unicode だったら何もしない """
        if isinstance(strings, str):
            strings = strings.decode('utf-8')

        return strings

    @staticmethod
    def normalize(strings, unistr = 'NFKC'):
        """ 引数を normalize する。"""
        strings = BaseBytes.convert2unicode(strings)
        return unicodedata.normalize(unistr, strings)


class MultiBytes(BaseBytes):

    """
    マルチバイト系の変換メソッド

        c.f.
          http://atasatamatara.hatenablog.jp/entry/2013/04/15/201955
    """

    @staticmethod
    def zenNum2hanNum(strings):
        """
        全角数字を半角数字に変換する
        その他の文字はそのまま
        """
        strings = MultiBytes.convert2unicode(strings)
        return zenhan.z2h(strings, mode=2)


    @staticmethod
    def zenAlphaNum2hanAlphaNum(strings):
        """
        全角英数字を半角英数字に変換する
        """
        strings = MultiBytes.convert2unicode(strings)
        return zenhan.z2h(strings, mode=3)


    @staticmethod
    def hanKana2zenKana(strings):
        """
        半角カナを全角カナに変換する
        その他の文字はそのまま
        """

        strings = MultiBytes.convert2unicode(strings)
        return jctconv.h2z(strings)


    @staticmethod
    def hira2kana(strings):
        """
        全角ひらがなを全角カタカナに変換する
        その他の文字はそのまま

        http://d.hatena.ne.jp/mohayonao/20101213/1292237816
        """
        strings = MultiBytes.convert2unicode(strings)
        return jctconv.hira2kata(strings)


    @staticmethod
    def kana2hira(strings):
        """
        全角カタカナを全角ひらがなに変換する
        その他の文字はそのまま
        """
        strings = MultiBytes.convert2unicode(strings)
        return jctconv.kata2hira(strings)


##################################################

if __name__ == '__main__':
    import unittest

    class MultiByteTest(unittest.TestCase):
        def test_zenNum2hanNum(self):
            self.assertEqual('123', MultiBytes.zenNum2hanNum('１２３'))
            self.assertEqual('123', MultiBytes.zenNum2hanNum('１２３'))

            self.assertEqual('あいうえお123かきくけこ', MultiBytes.zenNum2hanNum('あいうえお１２３かきくけこ'))
            self.assertEqual('あいうえお123かきくけこ', MultiBytes.zenNum2hanNum('あいうえお１２３かきくけこ'))
            self.assertEqual('あい1うえ2お1か', MultiBytes.zenNum2hanNum('あい1うえ２お１か'))

            self.assertEqual('1aAａＡ23', MultiBytes.zenNum2hanNum('1aAａＡ２3'))
            self.assertEqual('1aAａＡ23', MultiBytes.zenNum2hanNum('1aAａＡ23'))

            self.assertEqual('123ー4567', MultiBytes.zenNum2hanNum('１２３ー４５６７'))

        def test_zenAlphaNum2hanAlphaNum(self):
            self.assertEqual('foo', MultiBytes.zenAlphaNum2hanAlphaNum('ｆｏｏ'))
            self.assertEqual('foo+123@example.jp',
                             MultiBytes.zenAlphaNum2hanAlphaNum('ｆｏｏ＋１２３＠ｅｘａｍｐｌｅ．ｊｐ'))

        def test_hanKana2zenKana(self):
            self.assertEqual('アアア', MultiBytes.hanKana2zenKana('ｱｱｱ'))
            self.assertEqual('アアア', MultiBytes.hanKana2zenKana('ｱｱｱ'))
            self.assertEqual('アアア', MultiBytes.hanKana2zenKana('アアア'))
            self.assertEqual('アアア', MultiBytes.hanKana2zenKana('アアア'))

            self.assertEqual('あああ', MultiBytes.hanKana2zenKana('あああ'))
            self.assertEqual('1２3', MultiBytes.hanKana2zenKana('1２3'))
            self.assertEqual('1２3', MultiBytes.hanKana2zenKana('1２3'))
            self.assertEqual('オオ１ａaAＡ漢！”＃＄％', MultiBytes.hanKana2zenKana('ｵオ１ａaAＡ漢！”＃＄％'))

        def test_hira2kana(self):
            self.assertEqual('アアア', MultiBytes.hira2kana('あああ'))
            self.assertEqual('アアア', MultiBytes.hira2kana('アアア'))
            self.assertEqual('1２ｱ', MultiBytes.hira2kana('1２ｱ'))

        def test_kana2hira(self):
            self.assertEqual('あああ', MultiBytes.kana2hira('アアア'))
            self.assertEqual('あああ', MultiBytes.kana2hira('あああ'))
            self.assertEqual('1２ｱ', MultiBytes.hira2kana('1２ｱ'))


    unittest.main()
