#分析文件
import sqlite3
import os


def parseFile():
    print("parse file")


def parseSupTxt(file):
    ss = []
    with open(file) as lines:
        for line in lines:
            line = line.replace("\n","")
            line = line.strip()
            line = line.replace(" ","")
            if line.startswith("SUPID"):
                None
            elif line.startswith("------"):
                None
            elif line.startswith("已选择"):
                None
            elif line == "":
                None
            else:
                ss.append(line)
            # print(line)
    print("*" * 10)
    print(ss)
    print("*" * 10)
    return ss


def get_function_def(file):
    str = ""
    ss = []
    with open(file) as lines:
        bg = False
        for line in lines:
            line = line.replace("\n", "")
            line = line.strip()
            if bg:
                ss.append(line.replace("{", "").strip())
                if line.find(")") != -1:
                    bg = False
            if line.startswith("<%!"):
                bg = True
            if bg == False:
                continue
    print("-" * 10, file)
    # print(ss)
    ss2 = []
    functiondef = ""
    for s in ss:
        if s.find("(") != -1 and s.find(")") != -1:
            ss2.append(s)
        else:
            functiondef = functiondef + s
            if functiondef.find("(") != -1 and functiondef.find(")") != -1:
                ss2.append(functiondef)
                functiondef = ""
    for s in ss2:
        print(s)
    print("-" * 10)
    return ss2


def parseDir(path):
    files = os.listdir(path)
    # print(files)
    for filename in files:
        file = os.path.normpath(os.path.join(path, filename))
        if os.path.isfile(file):
            if filename == "sup.txt":
                ss = parseSupTxt(file)
                addRecord(path,ss,"sup")
            elif filename == "rechargeraction.jsp":
                ss = get_function_def(file)
                addRecord(path, ss, "recharge")
            elif filename == "yqorderprocessing.jsp":
                ss = get_function_def(file)
                addRecord(path, ss, "query")
            elif filename == "provfun.jsp":
                ss = get_function_def(file)
                addRecord(path, ss, "fund")
        else:
            print("directory is ", file)
            parseDir(file)


def addRecord(cust, ss, type):
    db = sqlite3.connect("e:\\allsup\\supapi.db")
    cur = db.cursor()
    sql = "Insert into t_cust_method(cust_name, method_name, type) values (?,?,?)"
    for s in ss:
        cur.execute(sql, (cust, s, type))  # 执行插入命令
    db.commit()
    db.close();  # 关闭数据库连接


def clearRecord():
    db = sqlite3.connect("e:\\allsup\\supapi.db")
    cur = db.cursor()
    sql = "delete from  t_cust_method"
    cur.execute(sql)
    sql = "delete from  t_result"
    cur.execute(sql)
    db.commit()
    db.close();  # 关闭数据库连接


def parseRecord():
    db = sqlite3.connect("e:\\allsup\\supapi.db")
    cur = db.cursor()
    sql = "select * from t_cust_method where type = 'sup' order by cust_name"
    cur.execute(sql)
    ss = cur.fetchall()
    # add cust
    cust_name = ""
    sup_name_list = []
    line_change = False
    cust_methods_list = []
    for s in ss:
        if s[0] != cust_name:
            if len(sup_name_list) > 0:
                cust_methods_list.append((cust_name,sup_name_list))
            cust_name = s[0]
            sup_name_list = []
            sup_name_list.append(s[1])
        else:
            sup_name_list.append(s[1])
    if len(sup_name_list) > 0:
        cust_methods_list.append((cust_name, sup_name_list))
    print(cust_methods_list)
    for cust in cust_methods_list:
        cust_name = cust[0]
        method_list = cust[1]
        for sup_name in method_list:
            sql = "update t_cust_method set sup_name = ? where cust_name=? and method_name like ?"
            cur.execute(sql, (sup_name, cust_name,'%' + sup_name + '%'))
    db.commit()
    db.close()


def getResult():
    db = sqlite3.connect("e:\\allsup\\supapi.db")
    cur = db.cursor()
    sql = "select cust_name, method_name,type,sup_name from t_cust_method where type = 'sup' order by cust_name"
    cur.execute(sql)
    ss = cur.fetchall()
    s0 = ""
    s1 = ""
    s2 = ""
    s3 = ""
    s4 = ""
    print("写入结果文件开始")
    result_list = []
    for s in ss:
        cust_name = s[0]
        sup_name = s[1]
        sql = "select cust_name, method_name,type,sup_name from t_cust_method where type = 'recharge' and cust_name=? and sup_name=?"
        cur.execute(sql, ( cust_name, sup_name ))
        recharge_list = cur.fetchone()
        #print(recharge_list)
        if recharge_list is None:
            s2 = ""
        else:
            s2 = recharge_list[1]
        sql = "select cust_name, method_name,type,sup_name from t_cust_method where type = 'query' and cust_name=? and sup_name=?"
        cur.execute(sql, ( cust_name, sup_name))
        query_list = cur.fetchone()
        if query_list is None:
            s3 = ""
        else:
            s3 = query_list[1]
        sql = "select cust_name, method_name,type,sup_name from t_cust_method where type = 'fund' and cust_name=? and sup_name=?"
        cur.execute(sql, (cust_name, sup_name))
        fund_list = cur.fetchone()
        if fund_list is None:
            s4 = ""
        else:
            s4 = fund_list[1]
        result_list.append((cust_name,sup_name,s2,s3,s4))
    for res in result_list:
        print(res)
        sql = "insert into t_result values(?,?,?,?,?)"
        cur.execute(sql, (res[0], res[1], res[2], res[3], res[4]))
        db.commit()
    db.close()
    print("操作结束")


if __name__ == "__main__":
    clearRecord()
    parseDir("E:\\allsup\\allsup");
    parseRecord()
    getResult()