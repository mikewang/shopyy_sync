import sys
import traceback
import pymysql
import os
import datetime


def sync_data():
    ss = os.system("/root/sync_tab.sh")
    print(ss)


def check_db(source_ip, str_tab, str_col, ago_days):
    try:
        # print("session" + source_ip)
        if source_ip == '192.168.212.8':
            conn = pymysql.connect(host=source_ip, user='csswebmysql', passwd='gzwwzf@189', db='sttrade_hist', port=3306)
        else:
            conn = pymysql.connect(host='localhost', user='csswebmysql', passwd='gzwwzf@189', db='sttrade_212_8', port=3306)
        cur = conn.cursor()
        str_sql = 'select count(*) from ' + str_tab
        str_sql = str_sql + ' where ' + str_col + ' >= DATE_ADD(CAST(now() AS DATE),INTERVAL -' + str(ago_days) + ' DAY) '
        ago_days = ago_days - 1
        str_sql = str_sql + ' and ' + str_col + ' < DATE_ADD(CAST(now() AS DATE),INTERVAL -' + str(ago_days) + ' DAY)'
        cur.execute(str_sql)
        r = cur.fetchone()
        c_row = 0
        if r is not None:
            c_row = r[0]
        conn.close()
        return c_row
    except Exception as e:
        print('str(Exception):\t', str(Exception))
        print('str(e):\t\t', str(e))
        print('repr(e):\t', repr(e))
        # Get information about the exception that is currently being handled
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('e.message:\t', exc_value)
        print("Note, object e and exc of Class %s is %s the same." %
              (type(exc_value), ('not', '')[exc_value is e]))
        print('traceback.print_exc(): ', traceback.print_exc())
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        print('-' * 60)
        return 0


def delete_source_db(source_ip, str_tab, str_col, ago_days):
    try:
        print("session" + source_ip)
        conn = pymysql.connect(host=source_ip, user='csswebmysql', passwd='gzwwzf@189', db='sttrade_hist', port=3306)
        cur = conn.cursor()
        str_sql = 'delete from ' + str_tab
        str_sql = str_sql + ' where ' + str_col + ' >= DATE_ADD(CAST(now() AS DATE),INTERVAL -' + str(ago_days) + ' DAY) '
        ago_days = ago_days - 1
        if ago_days < 3:
            ago_days = 9
        str_sql = str_sql + ' and ' + str_col + ' < DATE_ADD(CAST(now() AS DATE),INTERVAL -' + str(ago_days) + ' DAY)'
        cur.execute(str_sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print('str(Exception):\t', str(Exception))
        print('str(e):\t\t', str(e))
        print('repr(e):\t', repr(e))
        # Get information about the exception that is currently being handled
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('e.message:\t', exc_value)
        print("Note, object e and exc of Class %s is %s the same." %
              (type(exc_value), ('not', '')[exc_value is e]))
        print('traceback.print_exc(): ', traceback.print_exc())
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        print('-' * 60)


def clear_source_data(str_tab, str_col, ago_days):
    source_ip = '192.168.212.8'
    cc_source = check_db(source_ip, str_tab, str_col, ago_days)
    # print(cc_source)
    cc_target = check_db('localhost', str_tab, str_col, ago_days)
    # print(cc_target)
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if cc_source == cc_target:
        msg = time_str + str_tab + ':' + 'source=' + str(cc_source) + ' target=' + str(cc_target)
        print(msg)
        delete_source_db(source_ip, str_tab, str_col, ago_days)
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = time_str + str_tab + ':' + 'source=' + str(cc_source) + ' deleted successful.'
        print(msg)
    else:
        msg = time_str + str_tab + ':' + 'source=' + str(cc_source) + ' target=' + str(cc_target)
        print(msg + ' deleted failure.')


if __name__ == '__main__':
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("run begin", time_str)
    sync_data()
    clear_source_data('data_ypt_tran_hist', 'reg_date', 10)
    clear_source_data('file_transaction_hist', 'reg_date', 10)
    clear_source_data('data_traffic_report_hist', 'reg_date', 10)
    clear_source_data('tr_order_thrid_hist', 'create_time', 31)
    clear_source_data('owner_order_hist', 'reg_date', 31)
    clear_source_data('owner_order_single_ticket_hist', 'reg_date', 31)
    clear_source_data('owner_order_opt_hist_hist', 'opt_date', 31)
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("run completed", time_str)
