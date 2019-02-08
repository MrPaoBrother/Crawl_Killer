# 数据库撤稿爬虫系统使用手册

## 简介

* 该系统主要针对```撤稿网站```进行抓取, 网站属于极其难爬的一种，多层加密嵌套以及严格的cookie验证机制使得数据安全性很高，但是还是有办法把他抓下来的
* 网站链接: http://retractiondatabase.org/(X(1)S(f2za2eaupe1oi1ged5cpbiik))/RetractionSearch.aspx?AspxAutoDetectCookieSupport=1

> 该文章主要讲下win系统的使用流程

## 功能

* 支持任意日期之间数据获取
* 支持xls,csv文件格式
* 支持自定义分隔符
* 支持自定义分区抓取
* 支持Mac,Win双系统

## 环境

* Mac OS (10.14.2)
* Python 2.7
* Vim 8.0

## 安装

* 安装chrome浏览器,保证版本是v60以上

  > ps. 查看chrome浏览器的方法是: chrome://version/

* 安装```pychrome```模块

* ```bash
  $ pip install pychrome
  ```

* 安装 csv 模块

* ```bash
  $ pip install csv
  ```

* 安装 xlwt 模块

* ```bash
  $ pip install xlwt
  ```

## 运行

* win系统通过命令行启动chrome

* ```bash
  $ xxx/xxx/chrome.exe--headless --remote-debugging-port=9222 --disable-gpu https://chromium.org
  ```

* 这个时候会看到出现了浏览器,运行如下命令确认启动成功

* ```bash
  $ http://localhost:9222/
  ```

* 程序进入到```run_lunwen.py```同级目录下

* ```bash
  $ python run_lunwen.py
  ```

> 程序开始运行了