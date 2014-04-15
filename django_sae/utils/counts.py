# coding=utf-8


def count_pages(page_length, total_number):
    """ 计算页数
    """
    quotient, remainder = divmod(total_number, page_length)
    return quotient + int(remainder != 0)


def count_length(string):
    """ 计算字符数，1个中文算一个字符，1个英文算半个字符。应用场景：如微博字符计算。
    """
    length = len(string)
    utf_length = len(string.encode('utf-8'))
    cn_length = (utf_length - length) / 2
    en_length = length - cn_length
    return cn_length + count_pages(2, en_length)