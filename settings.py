# -*- coding:utf8 -*-
"""
title: 论文撤稿数据库抓取系统
author: power
datetime: 2019-01-20
"""

"""
用户自定义配置
"""

# 抓取开始日期(格式必须是 mm/dd/yyyy)
crawl_start_time = "05/14/2012"

# 抓取结束日期(格式必须是 mm/dd/yyyy)
crawl_end_time = "05/24/2012"

# 保存的文件地址(支持csv, xls)
file_path = "./data/happy1.xls"

# 抓取最大间隔天数(有可能最多只有600条数据 例: 比如我想抓2000-2010年的数据 那么设置100代表每100天为一个单位) (单位:天)
max_day_delay = 60

# 数据分隔符 (例: 表示多个学校  浙江大学+北京大学)
default_separator = "+"

# excel的标题
default_excel_header = [u"标题", u"关键词", u"期刊", u"学校", u"链接", u"原因", u"作者", u"Original Paper",
                        u"Retraction or Other Notices Date/PubMedID/DOI", u"Article Type(s) Nature of Notice",
                        u"Countries Paywalled? Notes"]

"""
抓取性能配置
"""

# 爬完之后网页是否关闭(节省资源)
is_tab_close = False

# 如果不成功重试次数(网速较卡的时候可以配置)
default_retry = 5

# 重试等待时间(s)
retry_wait_time = 2

# 不同动作之间的时间间隔(s)
action_time_delay = 1

"""
网页参数配置
"""

# 起始日期输入框id
from_input_id = "txtOriginalDateFrom"

# 结束日期输入框id
end_input_id = "txtOriginalDateTo"

# 提交按钮的id
submit_id = "btnSearch"

"""
chrome 内核相关
"""

# chrome的ip和端口
CONF = {
    'url': 'http://127.0.0.1:9222'
}

# 默认下载延迟
DEFAULT_DOWNLOAD_DELAY = 2
