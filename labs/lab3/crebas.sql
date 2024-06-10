/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2024-05-17 20:43:12                          */
/*==============================================================*/

use faculty;

alter table 主讲课程 
   drop foreign key FK_主讲课程_主讲课程_教师;

alter table 主讲课程 
   drop foreign key FK_主讲课程_主讲课程2_课程;

alter table 发表论文 
   drop foreign key FK_发表论文_发表论文_教师;

alter table 发表论文 
   drop foreign key FK_发表论文_发表论文2_论文;

alter table 承担项目 
   drop foreign key FK_承担项目_承担项目_教师;

alter table 承担项目 
   drop foreign key FK_承担项目_承担项目2_项目;

drop table if exists 主讲课程;

drop table if exists 发表论文;

drop table if exists 承担项目;

drop table if exists 教师;

drop table if exists 论文;

drop table if exists 课程;

drop table if exists 项目;

/*==============================================================*/
/* Table: 主讲课程                                                  */
/*==============================================================*/
create table 主讲课程
(
   工号                   char(5) not null  comment '',
   课程号                  char(255) not null  comment '',
   年份                   int  comment '',
   学期                   int  comment '',
   承担学时                 int  comment '',
   primary key (工号, 课程号, 年份, 学期)
   -- foreign key (工号) references 教师 (工号),
   -- foreign key (课程号) references 课程 (课程号)
);

/*==============================================================*/
/* Table: 发表论文                                                  */
/*==============================================================*/
create table 发表论文
(
   工号                   char(5) not null  comment '',
   序号                   int not null  comment '',
   排名                   int  comment '',
   是否通讯作者               bool  comment '',
   primary key (工号, 序号)
   -- foreign key (工号) references 教师 (工号),
   -- foreign key (序号) references 论文 (序号)
);

/*==============================================================*/
/* Table: 承担项目                                                  */
/*==============================================================*/
create table 承担项目
(
   工号                   char(5) not null  comment '',
   项目号                  char(255) not null  comment '',
   排名                   int  comment '',
   承担经费                 float(12,2)  comment '',
   primary key (工号, 项目号)
   -- foreign key (工号) references 教师 (工号),
   -- foreign key (项目号) references 项目 (项目号)
);

/*==============================================================*/
/* Table: 教师                                                    */
/*==============================================================*/
create table 教师
(
   工号                   char(5) not null  comment '',
   姓名                   char(255)  comment '',
   性别                   int  comment '',
   职称                   int  comment '',
   primary key (工号)
);

/*==============================================================*/
/* Table: 论文                                                    */
/*==============================================================*/
create table 论文
(
   序号                   int not null  comment '',
   论文名称                 char(255)  comment '',
   发表源                  char(255)  comment '',
   发表年份                 date  comment '',
   类型                   int  comment '',
   级别                   int  comment '',
   primary key (序号)
);

/*==============================================================*/
/* Table: 课程                                                    */
/*==============================================================*/
create table 课程
(
   课程号                  char(255) not null  comment '',
   课程名称                 char(255)  comment '',
   学时数                  int  comment '',
   课程性质                 int  comment '',
   primary key (课程号)
);

/*==============================================================*/
/* Table: 项目                                                    */
/*==============================================================*/
create table 项目
(
   项目号                  char(255) not null  comment '',
   项目名称                 char(255)  comment '',
   项目来源                 char(255)  comment '',
   项目类型                 int  comment '',
   总经费                  float(10,2)  comment '',
   开始年份                 int  comment '',
   结束年份                 int  comment '',
   primary key (项目号)
);

alter table 主讲课程 add constraint FK_主讲课程_主讲课程_教师 foreign key (工号)
      references 教师 (工号) on delete restrict on update restrict;

alter table 主讲课程 add constraint FK_主讲课程_主讲课程2_课程 foreign key (课程号)
      references 课程 (课程号) on delete restrict on update restrict;

alter table 发表论文 add constraint FK_发表论文_发表论文_教师 foreign key (工号)
      references 教师 (工号) on delete restrict on update restrict;

alter table 发表论文 add constraint FK_发表论文_发表论文2_论文 foreign key (序号)
      references 论文 (序号) on delete restrict on update restrict;

alter table 承担项目 add constraint FK_承担项目_承担项目_教师 foreign key (工号)
      references 教师 (工号) on delete restrict on update restrict;

alter table 承担项目 add constraint FK_承担项目_承担项目2_项目 foreign key (项目号)
      references 项目 (项目号) on delete restrict on update restrict;

Insert into 教师 (工号, 姓名, 性别, 职称)-- 
values
('00001', '张俊霞', 1, 4),
('00002', '李诚', 1, 4),
('00003', '金培权', 1, 4),
('00004', '李烨昊', 1, 2),
('00005', '许胤龙', 1, 6),
('00006', '徐宏力', 1, 6),
('00007', '孙广中', 1, 6),
('00008', '张兰', 2, 6), 
('00009', '张昱', 2, 6),
('00010', '蔡晓辉', 2, 5),
('00011', '谈海生', 1, 5),
('00012', '王超', 1, 5),
('00013', '李永坤', 1, 5)
;


insert into 课程
values
('CS1001A', '计算机程序设计A', 100, 1),
('MATH1006', '数学分析(B1)', 120, 1),
('MATH1009', '线性代数(B1)', 80, 1),
('MATH1007', '数学分析(B2)', 120, 1),
('011103', '代数结构', 60, 1),
('PHYS1001B', '力学B', 50, 1),
('PHYS1002B', '热学B', 30, 1),
('011127', '数据结构', 100, 1),
('CS1002A', '计算系统概论A', 100, 1),
('011040', '图论', 60, 1),
('011151', '模拟与数字电路', 80, 1),
('011152', '模拟与数字电路实验', 40, 1),
('CS3001H', '计算机组成原理(H)', 100, 1),
('011705','操作系统原理与设计(H)', 100, 1),
('HS1618M', '艺术的启示', 40, 2),
('011703', '编译原理和技术(H)', 100, 1),
('011146', '算法基础', 90, 1),
('HS1504', '科技考古概论', 40, 1),
('COMP6102P', '并行算法', 60, 2), 
('COMP6226P', '边缘与云计算', 60, 2),
('COMP7205P', '计算机系统性能评价与预测', 40, 2),
('MATH6102P', '李代数及其表示理论', 80, 2), 
('MATH6437P', '辛拓扑初步', 80, 2),
('MATH7408P', '数论选讲', 80, 2)
;
