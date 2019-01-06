# coding=utf-8
"""
@author: congying
@email: wangcongyinga@gmail.com 
"""
from flask import Flask, render_template
from ext.load_settings import ConfLoader
from ext.posts_render import PostRender
import json


class EasyManApp(object):
    def __init__(self, **kwargs):
        self.settings = ConfLoader(**kwargs).load_conf()
        self.post_render = PostRender(self.settings)
        self.app = Flask(__name__, template_folder=self.settings['TEMPLATE_DIR'], static_folder=self.settings['STATIC_DIR'])
        self.app.add_url_rule('/', endpoint='index', view_func=self.index, methods=['GET'])
        self.app.add_url_rule('/<file_name>', view_func=self.get_per_page, methods=['GET'])
        self.template = self.settings['DEFAULT_LAYOUT']
        self.title = self.settings['TITLE']

    def index(self):
        all_entries = self.post_render.render_all_posts()
        # all_entries = self.post_render.gen_index_data()
        content = self.post_render.gen_html_page(all_entries)

        return render_template(self.template, title=self.title, content=content)

    def get_history_posts(self):
        """
        获得历史所有文章
        :return:
        """
        self.post_render.render_all_posts()
        all_entries = self.post_render.gen_index_data()
        content = self.post_render.gen_html_page(all_entries)
        return render_template(self.template, title=self.title, content=content)

    def get_per_page(self, file_name):
        content = self.post_render.render_file(file_name)
        if content:
            content = json.loads(content)
            text = content.get('text')
            category = content.get('category')
            return render_template(self.template, title=self.title, content=text, category=category)
        else:
            return self.page_not_found()

    def page_not_found(self):
        md_file = self.post_render.render_file('not_found')
        md_file = json.loads(md_file)
        return render_template(self.template, title=self.title, content=md_file.get('text'))

    def run(self, **kwargs):
        self.app.run(**kwargs)


if __name__ == '__main__':
    kwargs = {"conf_name": 'default', "project_path": '/Users/wangcongying/PycharmProjects/'}
    easyman = EasyManApp(**kwargs)
    easyman.app.run(debug=True)
