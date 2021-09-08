import requests
import ast
from colorama import init, Fore, Back, Style
from prettytable import PrettyTable as pt, ORGMODE, MARKDOWN, MSWORD_FRIENDLY, PLAIN_COLUMNS, DEFAULT, RANDOM
import msvcrt as m


init(autoreset=False)


class Colored(object):
    #  前景色:红色  背景色:默认
    def red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET
    #  前景色:绿色  背景色:默认

    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET


color = Colored()
table = pt(['Code', 'Name', 'Estimate', 'Growth', 'Time'])  # 表头
table.align['Name'] = 'c'  # 居中对齐
table.align['Estimate'] = 'c'
table.padding_width = 1
# 样式选择可选：ORGMODE, MARKDOWN, MSWORD_FRIENDLY, PLAIN_COLUMNS, DEFAULT, RANDOM
table.set_style(MARKDOWN)

with open('fund.json', 'r', encoding='utf-8') as f:
    fund_data = json.load(f)
    fund_code = fund_data.get('fund_code')  # 基金代码

while True:
    for code in fund_code:
        url = f'http://fundgz.1234567.com.cn/js/{code}.js?rt=1463558676006'
        r = requests.get(url=url)
        fund_dict = ast.literal_eval(r.text[8:-2])  # 不是json，只能字符串截取，转换为字典
        if float(fund_dict['gszzl']) < 0:  # 跌
            table.add_row([fund_dict['fundcode'],
                           fund_dict['name'],
                           fund_dict['gsz'],
                           color.green(fund_dict['gszzl']),
                           fund_dict['gztime']])
        elif 0 < float(fund_dict['gszzl']) < 3:  # 涨
            table.add_row([fund_dict['fundcode'],
                           fund_dict['name'],
                           fund_dict['gsz'],
                           color.yellow(fund_dict['gszzl']),
                           fund_dict['gztime']])
        else:  # 大涨
            table.add_row([fund_dict['fundcode'],
                           fund_dict['name'],
                           fund_dict['gsz'],
                           color.red(fund_dict['gszzl']),
                           fund_dict['gztime']])
    print(table.get_string(sortby='Growth'))
    table.clear_rows()
    input('Press Enter to continue...')

    def wait():
        m.getch(
        )
