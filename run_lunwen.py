# -*- coding:utf8 -*-

import time

from cmd import js_cmd
from lxml import etree

from util.util import str_to_datetime, get_end_time
from util.util import write2csv, csv2xls
from util.util import parse_article_by_tds, write_header

import settings
from chrome_spider import ChromeSpider

chrome_spider = ChromeSpider(**settings.CONF)


def get_date_list_by_params():
    """
    由于最多显示600条 因此分批取数据
    :return:
    """
    date_list = []
    start_time = settings.crawl_start_time
    end_time = settings.crawl_end_time

    if start_time > end_time:
        print("结束时间必须大于开始时间...")
        return date_list

    from_time = start_time
    while True:
        to_time = get_end_time(from_time, settings.max_day_delay)
        if str_to_datetime(to_time, '%m/%d/%Y') > str_to_datetime(end_time, '%m/%d/%Y'):
            # 说明分区到终点了
            to_time = end_time
            date_list.append((from_time, to_time))
            break

        date_list.append((from_time, to_time))
        # 要往后算一天
        from_time = get_end_time(to_time, 1)

    return date_list


def wait_tab_finish(tab):
    while True:
        if not chrome_spider.is_page_loading_finished(tab):
            time.sleep(settings.action_time_delay)
            continue
        return


def fill_form(tab, input_params, tip):
    wait_tab_finish(tab)

    print("{tip} 正在自动填写表单,参数:{param}".format(tip=tip, param=input_params))

    for k, v in input_params.items():
        # 填一个验证一个
        while True:
            try:
                chrome_spider.exec_js_cmd(tab, js_cmd.FILL_VALUE_IN_FORM % (k, v))
                # 填完之后去获取输入框中的值
                result = chrome_spider.exec_js_cmd(tab, js_cmd.GET_VALUE_IN_FORM % k)
                print result
                value = result.get("result", dict()).get("value", "")
                if not value:
                    print("表单没有填写成功，正在重试")
                    time.sleep(settings.action_time_delay)
                    continue
                if value == v:
                    break
            except Exception as e:
                print("表单填写出错:%s" % str(e))
                time.sleep(2)
    time.sleep(settings.action_time_delay)

    print("{tip} 自动填写表单完成，等到返回结果中...".format(tip=tip))

    wait_tab_finish(tab)

    chrome_spider.exec_js_cmd(tab, js_cmd.CLICK_BY_ID % settings.submit_id)


def get_html_by_date(url, start_time, end_time):
    tab = chrome_spider.create_new_tab(url=url)
    chrome_spider.start_tab(tab)

    retry = settings.default_retry

    while retry > 0:
        try:
            # 时间段提示
            tip = "时间段({start_time}-{end_time})".format(start_time=start_time, end_time=end_time)
            print("{tip} 主页加载中...".format(tip=tip))

            wait_tab_finish(tab)

            print("{tip} 主页加载成功...".format(tip=tip))

            # 填写表单
            input_params = {settings.from_input_id: start_time, settings.end_input_id: end_time}

            fill_form(tab, input_params, tip)

            wait_tab_finish(tab)

            html = chrome_spider.download_html(tab=tab, close_tab=settings.is_tab_close)

            dom = etree.HTML(html)

            trs = dom.xpath('.//tbody//tr[@class="mainrow"]')

            print("{tip} 获取文章数量: {num}\n".format(tip=tip, num=len(trs)))

            # 有可能确实没有
            isEmptyDom = dom.xpath('.//span[@id="lblError"]/text()')
            if isEmptyDom:
                # chrome_spider.close_tab(tab)
                print("{tip} 该时间段没有文章，准备进入下一个时间段...\n".format(tip=tip, num=len(trs)))
                return "", 0

            if not trs or len(trs) == 0:
                print("{tip} 数量不太对 正在重试中(2s)".format(tip=tip))
                time.sleep(settings.retry_wait_time)
                retry -= 1
                continue

            #chrome_spider.close_tab(tab)
        except Exception as e:
            # 有问题说明tab启动失败了
            print("tab start failed: %s" % str(e))
            tab = chrome_spider.create_new_tab(url=url)
            chrome_spider.start_tab(tab)
            retry -= 1
            continue
        break

    return html, len(trs)


def deal_html(html):
    dom = etree.HTML(html)
    trs = dom.xpath('.//tbody//tr[@class="mainrow"]')
    if not trs:
        # 说明这个时间段没有数据 或者 ip被封禁了
        print("该时间段没有数据或者ip被封禁了，请检查")
        return

    for tr in trs:
        tds = tr.xpath('.//td')
        data_list = parse_article_by_tds(tds)

        write2csv(data_list=data_list, file_path=settings.file_path)


def deal_file():
    """
    支持xls文件转换
    :return:
    """
    print("正在进行文件格式转换...")

    csv_file_path = settings.file_path.replace(".xls", ".csv")
    xls_file_path = settings.file_path.replace(".csv", ".xls")
    csv2xls(csv_file_path=csv_file_path, xls_file_path=xls_file_path)

    print("处理完成...")


def do_report(report_data):
    print("===============抓取结果=================")
    print("抓取结果如下所示:")
    if not report_data:
        print("暂无抓取数据")
        return
    crawl_sum = 0
    for data in report_data:
        start_time, end_time, count = data
        crawl_sum += count
        print(
            "时间段:{start_time} - {end_time}, 抓取数量:{count}".format(start_time=start_time, end_time=end_time, count=count))

    print("时间段:{start_time} - {end_time}, 总计: {sum}".format(start_time=settings.crawl_start_time,
                                                            end_time=settings.crawl_end_time, sum=crawl_sum))
    print("===============抓取结果=================")


def process(url=None):
    if not url:
        return
    report = []

    date_patitions = get_date_list_by_params()
    if not date_patitions:
        return
    # 初始化excel文件
    write_header()
    # 按照时间分区进行抓取
    for patition in date_patitions:
        start_time, end_time = patition
        html, count = get_html_by_date(url=url, start_time=start_time, end_time=end_time)
        if not html:
            continue
        report.append((start_time, end_time, count))
        deal_html(html)

    deal_file()

    do_report(report)


if __name__ == "__main__":
    url = "http://retractiondatabase.org/(X(1)S(f2za2eaupe1oi1ged5cpbiik))/RetractionSearch.aspx?AspxAutoDetectCookieSupport=1"
    process(url)
