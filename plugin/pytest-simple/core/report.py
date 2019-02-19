# @Author  : lgb
# @Email   : liguobin@wanshare.com
# @Time    : 2018/11/19 17:12

from jinja2 import Environment, FileSystemLoader
import os


class Report:
    def __init__(self, report_file='report.html'):
        root = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(root, 'templates')
        env = Environment(loader=FileSystemLoader(templates_dir))
        self.template = env.get_template(report_file)
        self.filename = os.path.join(root, 'html', report_file)

    def gen_report(self, data):
        html = self.template.render(**data)
        with open(self.filename, 'w', encoding='utf-8') as fh:
            fh.write(html)


if __name__ == '__main__':
    report = Report()
    report.gen_report()
