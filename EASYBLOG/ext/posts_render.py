# coding=utf-8
"""
@author: congying
@email: wangcongyinga@gmail.com 
"""

from markdown import Markdown
from os import path, listdir
from page_errors import PageNotExistError
from load_settings import ConfLoader
from hashlib import md5
import datetime
import pymysql
import json
import logging


logger = logging.getLogger(__name__)


class BlogEntry(object):
    """
    这里做将content转成python可读的md，方便时间，作者名称的读取
    """
    def __init__(self, file_name, md, text):
        self.text = md.convert(text)
        self.file_name = file_name
        meta = md.Meta
        if meta:
            if 'date' in meta.keys():
                self.date = meta.get('date')[0]
            if 'tags' in meta.keys():
                self.tags = meta['tags'][0].split(',')
            if 'template' in meta.keys():
                self.template = meta.get('template')
            if 'categories' in meta.keys():
                self.category = meta.get('categories')[0]
            if 'author' in meta.keys():
                self.author = meta.get('author')
            if 'title' in meta.keys():
                self.title = meta.get('title')[0]
        else:
            self.title = self.file_name

    def __str__(self):
        # string = "['content': {}, 'name': {}, ".format(self.text, self.file_name)
        # string += "'date': {}, 'tags':[{}], ".format(self.date, self.tags)
        # string += "'author': {}, 'category': {}, ".format(self.author,
        #                                                   self.category)
        # string += "'template': {}]".format(self.template)

        return json.dumps(self.__dict__)


class PostRender(object):
    """
    这个函数做markdown的post转换为html展示
    """
    def __init__(self, settings):
        self.settings = settings
        self.post_dir = self.settings['POST_DIR']
        self.mysql_config = self.settings['DB_CONFIG']
        self.db = None
        self.cache = set()
        self.db = pymysql.Connect(**self.mysql_config)
        self.db.autocommit(True)

    def render_file(self, file_name):
        """
        这个函数做file的渲染，内部函数render_content做真正的渲染
        :return:
        """
        file_path = path.join(self.post_dir, file_name+'.md')
        insert_sql = "insert into easyman_posts(post_hash, post_content) values(%s, %s) on duplicate key update post_content=values(post_content)"
        select_sql = "select post_content from easyman_posts where post_hash=%s"
        post_title = file_name
        title_hash = md5(post_title).hexdigest()  # 是文章标题的唯一标识符
        message = "{} does not exists in {} directory.".format(file_name, self.post_dir)
        entry = None

        def render_content(text):
            md = Markdown(extensions=['meta', 'markdown.extensions.codehilite'])
            entry = BlogEntry(file_name, md, text)
            return entry.__str__()

        if title_hash not in self.cache:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    self.cache.add(title_hash)
                    entry = render_content(content)
                    with self.db.cursor() as cur:
                        cur.execute(insert_sql, (title_hash, entry.__str__()))
            except Exception, e:
                logger.info(e)
                print message
                return entry
        else:
            with self.db.cursor() as cur:  # TODO:这里数据库读取有问题
                cur.execute(select_sql, title_hash)
                for row in cur:
                    entry = row[0]
                    print entry
        return entry

    def render_html(self):
        """
        此函数用来渲染公式
        :return:
        """
        pass

    def render_all_posts(self, exclusions=['index.md', '404.md', 'not_found.md']):
        """
        这个函数得到文件夹下所有的posts并对其进行渲染
        :return:
        """

        files = listdir(self.post_dir)
        files = filter(lambda f: f.endswith('.md') and f not in exclusions, files)
        file_names = map(lambda f: path.splitext(f)[0], files)
        entries = map(lambda f: self.render_file(f), file_names)

        return entries

    def gen_html_page(self, posts):
        """
        生成一个展示文章list的html页面
        :return:
        """
        content = '<ul>'
        for post in posts:
            post = json.loads(post)
            entry_content = "<li><a href='/{}' style='font-size:20px; text-decoration: none'>{}</a></li>".format(post.get('file_name'), post.get('title'))
            content += entry_content
        content += '</ul>'
        return content

    def gen_index_data(self):
        """
        从数据库读出所有的list
        :return:
        """
        select_all_sql = "select post_content from easyman_posts"
        all_entries = []
        with self.db.cursor() as cur:
            cur.execute(select_all_sql)
            for row in cur:
                all_entries.append(row[0])

        return all_entries


if __name__ == "__main__":
    pr = PostRender('default', '/Users/wangcongying/PycharmProjects/')
