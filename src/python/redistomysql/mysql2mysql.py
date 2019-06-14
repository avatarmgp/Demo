#-*-coding:utf-8-*-
import pymysql
import pymssql
import sys

def connectMysql(h,p,u,ps,db):
    conn = pymysql.connect(host=h, port=p, user=u, password=ps, database=db, charset="utf8")
    return conn

def connectSqlServer():
    conn = pymssql.connect("192.168.199.66", "manager", "65ezbuy@nicemanager", "Pro")
    return conn

sql = "insert into user_shopping_cart(customer_id,service_type_id,gpid,sku_id,url,remark,qty,original_unit_price,selected,create_date,update_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE customer_id=values(customer_id),service_type_id=values(service_type_id),gpid=values(gpid),sku_id=values(sku_id),url=values(url),remark=values(remark),qty=values(qty),original_unit_price=values(original_unit_price),selected=values(selected),create_date=values(create_date),update_date=values(update_date);"
#分国家
def divCatalog():
    connmmysql_sg = connectMysql("192.168.199.134",8066,"cart_sg","cart_sg@123","cart_sg")
    cursormysql_sg = connmmysql_sg.cursor()

    connmmysql_my = connectMysql("192.168.199.134",8066,"cart_my","cart_my@123","cart_my")
    cursormysql_my = connmmysql_my.cursor()

    connmmysql_other = connectMysql("192.168.199.134",8066,"cart_other","cart_other@123","cart_other")
    cursormysql_other = connmmysql_other.cursor()

    connmssql = connectSqlServer()
    cursormsssql = connmssql.cursor()

    cursormysql_sg.execute("select customer_id,service_type_id,gpid,sku_id,url,remark,qty,original_unit_price,selected,create_date,update_date from user_shopping_cart")

    lsg = []
    lmy = []
    lother = []
    results = cursormysql_sg.fetchall()
    for row in results:
        customerid = row[0]
        servicetypeid = row[1]
        gpid = row[2]
        skuid = row[3]
        cursormsssql.execute("select catalogcode from customer where customerid=%s", customerid)
        rs = cursormsssql.fetchall()
        if len(rs) > 0:
            record = str(rs[0])
            s = record.index('\'')
            e = record.index(')')
            catalogcode = record[s+1:e-2]
        else:
            catalogcode = "OTHER"

        if catalogcode == "SG":
            print("SG")
        elif catalogcode == "TH":
            lsg.append([customerid, servicetypeid, gpid, skuid])
            lother.append(row)
        elif catalogcode == "ID":
            lsg.append([customerid, servicetypeid, gpid, skuid])
            lother.append(row)
        elif catalogcode == "TWC":
            lsg.append([customerid, servicetypeid, gpid, skuid])
            lother.append(row)
        elif catalogcode == "PK":
            lsg.append([customerid, servicetypeid, gpid, skuid])
            lother.append(row)
        elif catalogcode == "MY":
            lsg.append([customerid, servicetypeid, gpid, skuid])
            lmy.append(row)
        else:
            lsg.append([customerid, servicetypeid, gpid, skuid])
            lother.append(row)

    for l in lsg:
        cursormysql_sg.execute("delete from user_shopping_cart where customer_id=%s and service_type_id=%s and gpid=%s and sku_id=%s",l)
    connmmysql_sg.commit()
    
    for l in lmy:
        cursormysql_my.execute(sql, l)
    connmmysql_my.commit()
    for l in lother:
        cursormysql_other.execute(sql, l)
    connmmysql_other.commit()

    cursormysql_sg.close()       
    connmmysql_sg.close()
    cursormysql_my.close()       
    connmmysql_my.close()
    cursormysql_other.close()       
    connmmysql_other.close()

def main(argv):
    divCatalog()

if __name__ == "__main__":
    main(sys.argv[1:])