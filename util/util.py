# -*- coding:utf8 -*-
import csv
import xlwt
import datetime
import settings
import os


def csv2xls(csv_file_path=None, xls_file_path=None, sheet_name='data'):
    if not csv_file_path or ".csv" not in csv_file_path:
        print "csv文件格式不对或者缺少.csv"
        return

    if not xls_file_path:
        xls_file_path = csv_file_path.replace(".csv", ".xls")

    with open(csv_file_path, 'r') as f:
        read = csv.reader(f)
        workbook = xlwt.Workbook(encoding="utf8")
        sheet = workbook.add_sheet(sheet_name)  # 创建一个sheet表格
        l = 0
        for line in read:
            r = 0
            for i in line:
                sheet.write(l, r, i)  # 一个一个将单元格数据写入
                r = r + 1
            l = l + 1

        workbook.save(xls_file_path)  # 保存Excel


def write2csv(data_list, file_path):
    if not data_list:
        return

    if "." not in file_path:
        file_path += ".csv"
    elif ".xls" in file_path:
        file_path = file_path.replace(".xls", ".csv")
    else:
        return

    with open(file_path, "a+") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_list)


def str_to_datetime(date_str, format):
    return datetime.datetime.strptime(date_str, format)


def write_file(data_list, file_path):
    if not file_path or not data_list:
        return
    if ".csv" in file_path:
        write2csv(data_list, file_path)

    if ".xls" in file_path:
        change_file_name = file_path.replace(".xls", ".csv")
        write2csv(data_list, change_file_name)
        csv2xls(change_file_name)


def get_end_time(start_time, max_day_delay):
    start_datetime = str_to_datetime(start_time, '%m/%d/%Y')
    end_datetime = start_datetime + datetime.timedelta(days=max_day_delay)
    end_time = end_datetime.strftime("%m/%d/%Y")
    return end_time


def parse_title(td):
    title = td.xpath('.//span[@class="rTitleNotIE"]//text()')

    if not title:
        return ""

    return title[0].encode("utf8")


def parse_key_words(td):
    key_words = td.xpath('.//span[@class="rSubject"]//text()')
    if not key_words:
        return ""

    key_words = key_words[0]
    key_words = key_words.replace(";", settings.default_separator)
    if key_words[-1] == " ":
        key_words = key_words[:len(key_words) - 1]
    if key_words[-1] == settings.default_separator:
        key_words = key_words[:len(key_words) - 1]

    return key_words.encode("utf8")


def parse_schools(td):
    return ""


def parse_link(td):
    return ""


def parse_journal(td):
    result_list = td.xpath('.//span[@class="rJournal"]//text()')
    if not result_list or len(result_list) == 0:
        return ""
    return ("".join(result_list)).encode("utf8")


def parse_by_rule(dom, rule):
    result_list = dom.xpath(rule)
    if not result_list or len(result_list) == 0:
        return ""
    return (settings.default_separator.join(result_list)).encode("utf8")


def parse_attrs(attr_list):
    result = ""
    if not attr_list:
        return result
    result_list = []

    for attr in attr_list:
        if not attr.replace(" ", "").replace("\n", ""):
            continue
        result_list.append(attr)
    print "result_list:", result_list
    result = settings.default_separator.join(result_list)

    return result.encode("utf8")


def parse_article_by_tds(tds):
    """
    根据某一行 返回这一行需要的数据
    :param tds:
    :return:
    """
    if not tds:
        return []

    title = parse_title(tds[1])

    key_words = parse_key_words(tds[1])

    journal = parse_journal(tds[1])

    schools = parse_by_rule(tds[1], './/span[@class="rInstitution"]//text()')

    link = parse_by_rule(tds[1], './/a[@class="urls"]//text()')

    reason = parse_attrs(tds[2].xpath('.//text()')).replace("++", "+")
    authors = parse_attrs(tds[3].xpath('.//text()'))
    origin_paper = parse_attrs(tds[4].xpath('.//text()'))
    other_notices = parse_attrs(tds[5].xpath('.//text()'))
    article_type = parse_attrs(tds[6].xpath('.//text()'))
    contry = parse_attrs(tds[7].xpath('.//text()'))

    return [title, key_words, journal, schools, link, reason, authors, origin_paper, other_notices, article_type,
            contry]


def write_header():
    if os.path.exists(settings.file_path):
        return
    excel_header = []

    for item in settings.default_excel_header:
        excel_header.append(item.encode("utf8"))

    write2csv(excel_header, settings.file_path)
