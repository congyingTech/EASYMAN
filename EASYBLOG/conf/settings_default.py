# coding=utf-8
"""
@author: congying
@email: wangcongyinga@gmail.com 
"""


# give your template absolute path
TEMPLATE_DIR = '/Users/wangcongying/PycharmProjects/EASYMAN/EASYBLOG/templates/'

# give your posts absolute path
POST_DIR = '/Users/wangcongying/PycharmProjects/EASYMAN/EASYPOSTS/'

# give your static absolute path
STATIC_DIR = '/Users/wangcongying/PycharmProjects/EASYMAN/EASYBLOG/static'

# default style
DEFAULT_LAYOUT = 'template.html'

# user define style
DEFINE_LAYOUT = ''

# give your blog name
TITLE = "Congying's BLOG"

# add author name?
AUTHOR_NAME = 'congying'


LOG_FILE = '/Users/wangcongying/PycharmProjects/EASYMAN/easy_man.log'
LOG_LEVEL = 'INFO'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'blog',
    'charset': 'utf8mb4'
}

# 配置自己的redis cache，不配置的话，default下是simple cache
CACHE_CONFIG = {
    'host': 'localhost',
    'port': '6379'
}
