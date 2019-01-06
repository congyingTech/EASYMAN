# coding=utf-8
"""
@author: congying
@email: wangcongyinga@gmail.com 
"""


from EASYBLOG import EasyManApp


if __name__ == "__main__":
    kwargs = {"conf_name": 'default', "project_path": '/Users/wangcongying/PycharmProjects/'}
    EasyManApp(**kwargs).run(debug=True)
