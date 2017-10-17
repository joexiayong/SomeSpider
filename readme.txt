this is a git repository.

关于utf8的编码问题：
	1.修改Pymysql库的默认编码
		需修改Pymysql的源码，pip install pymysql即可显示路径
		修改connections.py文件 设置DEFULT_CHARSET，charset的值为utf8
	
	2.Mysql的默认编码问题
	在linux中 修改/etc/mysql中的配置文件
	查看编码：show variables like 'character%';	
