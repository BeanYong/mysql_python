#!coding:utf-8

import MySQLdb

# 转账类，封装相关方法
class TransferMoney:
	# 构造函数，传入数据库连接
	def __init__(self, conn):
		self.conn = conn;

	# 转账调度方法，send_account为转出账户，get_account为转入账户，money为转账金额
	def transfer(self, send_account, get_account, money):
		try:
			self.check_account_exist(send_account);
			self.check_account_exist(get_account);
			self.check_account_has_enough_money(send_account, money);
			self.reduce_money(send_account, money);
			self.add_money(get_account, money);
			self.conn.commit();
		except Exception as e:
			self.conn.rollback();
			raise e;
		
	# 判断账户是否存在
	def check_account_exist(self, account):
		cursor = self.conn.cursor();
		sql = "select id from account where account = %s" % account;
		try:
			cursor.execute(sql);
			rows = cursor.fetchall();
			if len(rows) != 1:
				raise Exception("帐号%s不存在" % account);
			print("帐号%s检查成功" % account);
		finally:
			cursor.close();


	# 判断当前账户余额是否足够
	def check_account_has_enough_money(self, account, money):
		cursor = self.conn.cursor();
		sql = "select id from account where account = %s and money >= %s" % (account, money);
		try:
			cursor.execute(sql);
			rows = cursor.fetchall();
			if len(rows) != 1:
				raise Exception("帐号%s余额不足" % account);
			print("帐号%s余额充足" % account);
		finally:
			cursor.close();

	# 为转出账户减少金额
	def reduce_money(self, account, money):
		cursor = self.conn.cursor();
		sql = "update account set money = money - %s where account = %s" % (money, account);
		try:
			cursor.execute(sql);
			if cursor.rowcount != 1:
				raise Exception("账户%s扣款失败" % account);
			print("帐号%s扣款成功" % account);
		finally:
			cursor.close();

	# 为转入账户增加金额
	def add_money(self, account, money):
		cursor = self.conn.cursor();
		sql = "update account set money = money + %s where account = %s"% (money, account);
		try:
			cursor.execute(sql);
			if cursor.rowcount != 1:
				raise Exception("转账到帐号%s失败" % account);
			print("转账成功");
		finally:
			cursor.close();


if __name__ == "__main__":
	send_account = 11;
	get_account = 12;
	money = 90;
	conn = MySQLdb.Connect(
		host = "127.0.0.1",
		port = 3306,
		user = "root",
		passwd = "beanyon",
		db = "test",
		charset = "utf8"
	    );
	try:
		transfer_money = TransferMoney(conn);
		transfer_money.transfer(send_account, get_account, money);
	except Exception as e:
		print(e);
	finally:
		conn.close();
