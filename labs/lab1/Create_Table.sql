drop database if exists Library1; 
CREATE database Library1 character set='utf8';
use Library1;
CREATE table Book (
	ID char(8),
    name varchar(10) not null,
    author varchar(10),
    price float,
    status int default 0,
    times int default 0,
    primary key (ID)
);

create table Reader(
	ID char(8),
    name varchar(10),
    age int,
    address varchar(20),
    primary key (ID)
);

create table Borrow (
	book_ID char(8),
    Reader_ID char(8),
    Borrow_Date date default null,
    Return_Date date default null,
    primary key (book_ID, Reader_ID),
    foreign key (book_ID) references Book(ID),
    foreign key (Reader_ID) references Reader(ID)
);

-- insert into Book(ID, name, author, price, status, times)
-- values
-- 	('00000001','运筹学教程','胡运权',39,0,0),
-- 	('00000002','音乐理论基础','李重光',25,0,0),
-- 	('00000003','天气之子','新海诚',42,0,0),
-- 	('10000000','数据库系统基础教程','Ullman',58,0,0),
-- 	('10000001','数据库系统实现','Ullman',56,0,0),
-- 	('10000002','数据库系统全书','Ullman',43,0,0),
-- 	('10000003','数据库系统概念','Abraham',70,0,0),
-- 	('10000004','Java语言程序设计','梁勇',100,0,0),
-- 	('10000005','软件工程','Roger',80,0,0),
-- 	('10000007','编译原理','Alfred',95,0,0),
-- 	('10000008','算法导论','Thomas',98,0,0),
-- 	('10000009','深入理解计算机系统','Randal',99.9,0,0),
-- 	('10000010','人工智能一种现代方法','Stuart',128,0,0),
--     ('10000011', '高性能MySQL', 'Silvia', 100, 0, 0);
--     
-- insert into Reader(ID, name, age, address)
-- values
-- 	('00000001','Rose',20,'New York'),
-- 	('00000002','李林',19,'USTC'),
-- 	('00000003','张三',30,'合肥'),
-- 	('00000004','李四',40,'南京'),
-- 	('00000005','王五',39,'上海'),
-- 	('00000006','唐三',20,'圣魂村'),
-- 	('00000007','唐昊',61,'圣魂村'),
-- 	('00000008','Kobe',42,'Los Angeles'),
-- 	('00000009','冥火大公',1000,'永火官邸'),
-- 	('00000010','萧炎',44,'乌坦城'),
-- 	('00000011','海波东',60,'伽马帝都'),
-- 	('00000012','甘雨',1200,'璃月'),
-- 	('00000013','妮露',17,'广东湛江'),
-- 	('00000014','申鹤',40,'璃月'),
-- 	('00000015','散兵',500,'净善宫'),
-- 	('00000016','纳西妲',500,'净善宫'),
-- 	('00000017','三月七',37,'星穹列车'),
-- 	('00000018','霍霍',14,'十王司'),
-- 	('00000019','玲可',16,'贝洛伯格'),
-- 	('00000020','停云',25,'复活赛赛场'),
-- 	('00000021','花火',20,'酒馆'),
-- 	('00000022','银狼',18,'星穹列车'),
-- 	('00000023','点刀哥',90,'容县'),
-- 	('00000024','小约翰可汗',24,'通辽'),
-- 	('00000025','镜流',1000,'仙舟罗浮');
    
Drop Procedure if exists modify_book_ID;
Delimiter //
CREATE PROCEDURE modify_book_ID(IN old_ID CHAR(8), IN new_ID CHAR(8))
BEGIN
	declare 
	n1, n2 int;
    declare 
        new_name, new_author varchar(10);
	declare
        new_price float;
	declare
        new_status, new_times int;
	-- 检查新旧ID是否已在表中
	select count(*) from Book where ID=old_ID into n1;
	select count(*) from Book where ID=new_ID into n2;
    select name into new_name from Book where ID = old_ID;
	select author into new_author from Book where ID = old_ID;
    select price into new_price from Book where ID = old_ID;
    select status into new_status from Book where ID = old_ID;
    select times into new_times from Book where ID = old_ID;
    
	if n1=1 and n2=0 and not old_ID like '00%' and not new_ID like '00%' then
        Insert into Book (ID, name, author, price, status, times)
        Value
			(new_ID, new_name, new_author, new_price, new_status, new_times);
		update Borrow set book_ID=new_ID where book_ID=old_ID;
		-- update Book set ID=new_ID where ID=old_ID;
        Delete from Book where ID=old_ID;
        select '执行成功';
	elseif n1=0 then
		signal SQLSTATE '45000' set message_text='要求修改的ID不存在';
	elseif n2>0 then
		signal SQLSTATE '45000' set message_text='修改后的ID已存在';
	elseif old_ID like '00%' then
		signal SQLSTATE '45000' set message_text='不允许修改超级ID';
	elseif new_ID like '00%' then
		signal SQLSTATE '45000' set message_text='不允许将ID修改为超级ID';
	end if;
END //
Delimiter ;