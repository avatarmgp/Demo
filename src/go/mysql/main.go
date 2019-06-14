package main

import (
	"database/sql"
	"fmt"
	"strings"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

const (
	userName = "root"
	password = "root"
	ip       = "127.0.0.1"
	port     = "3306"
	dbName   = "defaultcart"
)

var DB *sql.DB

// 购物车数据
type UserShoppingCart struct {
	UniqueIndex       string // primary index,做聚集索引
	CustomerId        int64
	ServiceTypeId     int64
	Gpid              int64
	SkuId             string
	Url               string
	Remark            string
	Qty               int64
	OriginalUnitPrice int64
	CreateDate        int64
	UpdateDate        int64
	Selected          bool
}

// 初始化数据库
func InitDB() bool {
	//构建连接："用户名:密码@tcp(IP:端口)/数据库?charset=utf8"
	path := strings.Join([]string{userName, ":", password, "@tcp(", ip, ":", port, ")/", dbName, "?charset=utf8"}, "")

	//打开数据库,前者是驱动名，所以要导入： _ "github.com/go-sql-driver/mysql"
	DB, _ = sql.Open("mysql", path)
	//设置数据库最大连接数
	DB.SetConnMaxLifetime(100)
	//设置上数据库最大闲置连接数
	DB.SetMaxIdleConns(10)
	//验证连接
	if err := DB.Ping(); err != nil {
		fmt.Println("opon database fail")
		return false
	}
	fmt.Println("connnect success")

	return true
}

// 插入数据
func InsertData(cs []*UserShoppingCart) bool {
	// 开启事务
	tx, err := DB.Begin()
	if err != nil {
		fmt.Println("tx failed")
		return false
	}

	var stmt *sql.Stmt
	for i := 0; i < len(cs); i++ {
		// 准备sql语句
		stmt, err = tx.Prepare("Insert into user_shopping_cart (customer_id,service_type_id,gpid,sku_id,url,remark,qty,original_unit_price,create_date,update_date,selected) VALUES (?,?,?,?,?,?,?,?,?,?,?)")
		if err != nil {
			print(err)
			return false
		}
		// 传递参数，执行
		_, err = stmt.Exec(cs[i].CustomerId, cs[i].ServiceTypeId, cs[i].Gpid, cs[i].SkuId, cs[i].Url, cs[i].Remark, cs[i].Qty, cs[i].OriginalUnitPrice, cs[i].CreateDate, cs[i].UpdateDate, cs[i].Selected)
		if err != nil {
			fmt.Println("Exec fail")
			return false
		}
	}

	// 提交事务
	tx.Commit()

	return true
}

// 删除数据
func DeleteData(score int) bool {
	// 准备事务
	tx, err := DB.Begin()
	if err != nil {
		fmt.Println("tx fail")
		return false
	}
	// 准备sql语句
	stmt, err := tx.Prepare("Delete from test where score = ?")
	if err != nil {
		fmt.Println("Prepare fail")
		return false
	}
	// 执行sql
	res, err := stmt.Exec(score)
	if err != nil {
		fmt.Println("Exec fail")
		return false
	}

	// 提交事务
	tx.Commit()
	fmt.Println(res.LastInsertId())

	return true
}

// 更新数据
func UpdateData(score int) bool {
	// 准备sql语句
	stmt, err := tx.Prepare("Delete from test where score = ?")
	if err != nil {
		fmt.Println("Prepare fail")
		return false
	}
	// 执行sql
	res, err := stmt.Exec(score)
	if err != nil {
		fmt.Println("Exec fail")
		return false
	}

	// 提交事务
	tx.Commit()
	fmt.Println(res.LastInsertId())

	return true
}

// 查询
func SelectData(customreId int64, serviceTypeId int64, gpId int64, skuId int64) UserShoppingCart {
	var s UserShoppingCart
	err := DB.QueryRow("select * from user_shopping_cart where customer_id = ? and service_type_id = ? and gpid = ? and sku_id = ?", customreId, serviceTypeId, gpId, skuId).Scan(&s.UniqueIndex, &s.CustomerId, &s.ServiceTypeId, &s.Gpid, &s.SkuId, &s.Url, &s.Remark, &s.Qty, &s.OriginalUnitPrice, &s.CreateDate, &s.UpdateDate, &s.Selected)
	if err != nil {
		fmt.Println("查询出错了")
		print(err)
	}
	return s
}

// 聚集索引查询
func SelectDataByPK(pk string) UserShoppingCart {
	var s UserShoppingCart
	err := DB.QueryRow("select * from user_shopping_cart where unique_index = ?", pk).Scan(&s.UniqueIndex, &s.CustomerId, &s.ServiceTypeId, &s.Gpid, &s.SkuId, &s.Url, &s.Remark, &s.Qty, &s.OriginalUnitPrice, &s.CreateDate, &s.UpdateDate, &s.Selected)
	if err != nil {
		fmt.Println("查询出错了")
	}
	return s
}

type Index struct {
	customreId    int64
	serviceTypeId int64
	gpId          int64
	skuId         string
}

// 多行查询
func SelectDatas(indexs []Index) []UserShoppingCart {
	start := time.Now().UnixNano()
	var sql string
	for k, index := range indexs {
		sql += fmt.Sprintf("select * from user_shopping_cart where customer_id = %v and service_type_id = %v and gpid = %v and sku_id = '%v'", index.customreId, index.serviceTypeId, index.gpId, index.skuId)
		if k != len(indexs)-1 {
			sql += " join "
		}
	}

	rows, err := DB.Query(sql)
	if err != nil {
		fmt.Println("查询出错了")
		return nil
	}

	var scores []UserShoppingCart
	for rows.Next() {
		var s UserShoppingCart
		err := rows.Scan(&s.CustomerId, &s.ServiceTypeId, &s.Gpid, &s.SkuId, &s.Url, &s.Remark, &s.Qty, &s.OriginalUnitPrice, &s.CreateDate, &s.UpdateDate, &s.Selected)
		if err != nil {
			fmt.Println("rows fail")
		}
		scores = append(scores, s)
	}

	println(time.Now().UnixNano() - start)
	return scores
}

func SelectDatas(indexs []Index) []*UserShoppingCart {
	start := time.Now().UnixNano()
	var sql string
	for k, index := range indexs {
		sql += fmt.Sprintf("select * from user_shopping_cart where customer_id = %v and service_type_id = %v and gpid = %v and sku_id = '%v'", index.customreId, index.serviceTypeId, index.gpId, index.skuId)
		if k != len(indexs)-1 {
			sql += " join "
		}
	}

	rows, err := DB.Query(sql)
	if err != nil {
		fmt.Println("查询出错了")
		return nil
	}

	var scores []UserShoppingCart
	for rows.Next() {
		var s UserShoppingCart
		err := rows.Scan(&s.CustomerId, &s.ServiceTypeId, &s.Gpid, &s.SkuId, &s.Url, &s.Remark, &s.Qty, &s.OriginalUnitPrice, &s.CreateDate, &s.UpdateDate, &s.Selected)
		if err != nil {
			fmt.Println("rows fail")
		}
		scores = append(scores, s)
	}

	println(time.Now().UnixNano() - start)
	return scores
}

// 时间统计
func timeCalc() {
	_, err := DB.Query("set @d=now()")
	rows, err := DB.Query("select timestampdiff(second,@d,now())")
	if err == nil {
		for rows.Next() {
			var t int64
			err = rows.Scan(&t)
			if err == nil {
				println(t)
			} else {
				print(err)
			}
		}
	}
}

func main() {
	success := InitDB()
	/*if success {
		start := time.Now().UnixNano()
		for loop := 0; loop < 1; loop++ {
			for cId := 0; cId < 1; cId++ {
				var cs []*UserShoppingCart
				for i := 0; i < 1; i++ {
					c := &UserShoppingCart{
						CustomerId:        int64(100000000000000 + i),
						ServiceTypeId:     1,
						Gpid:              int64(i),
						SkuId:             int64(i),
						Url:               "www.baidu.com",
						Remark:            "这是评论",
						Qty:               10,
						OriginalUnitPrice: 100,
						CreateDate:        time.Now().Unix(),
						UpdateDate:        time.Now().Unix(),
						Selected:          false,
					}
					cs = append(cs, c)
				}
				InsertData(cs)
			}
		}

		end := time.Now().UnixNano()

		print(end - start)
	}

	if success {
		start := time.Now().UnixNano()

		SelectData(0, 1, 0, 0)

		end := time.Now().UnixNano()
		print(end - start)
	}*/

	var indexs []Index
	start := time.Now().UnixNano()
	if success {
		for i := 0; i < 2; i++ {
			indexs = append(indexs, Index{
				customreId:    int64(i),
				serviceTypeId: 1,
				gpId:          1,
				skuId:         "sss",
			})
		}
		SelectDatas(indexs)
	}

	print(time.Now().UnixNano() - start)

	time.Sleep(time.Second * 100)
}
