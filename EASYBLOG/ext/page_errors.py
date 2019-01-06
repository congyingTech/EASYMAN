# coding=utf-8
"""
@author: congying
@email: wangcongyinga@gmail.com 
"""


class PageNotExistError(Exception):
    def __init__(self, message):
        super(PageNotExistError, self).__init__(message)

