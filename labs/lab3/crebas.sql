/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2024-05-17 20:43:12                          */
/*==============================================================*/

use faculty;

-- alter table 主讲课程 
--    drop foreign key FK_主讲课程_主讲课程_教师;

-- alter table 主讲课程 
--    drop foreign key FK_主讲课程_主讲课程2_课程;

-- alter table 发表论文 
--    drop foreign key FK_发表论文_发表论文_教师;

-- alter table 发表论文 
--    drop foreign key FK_发表论文_发表论文2_论文;

-- alter table 承担项目 
--    drop foreign key FK_承担项目_承担项目_教师;

-- alter table 承担项目 
--    drop foreign key FK_承担项目_承担项目2_项目;


-- alter table 主讲课程 
--    drop foreign key FK_主讲课程_主讲课程_教师;

-- alter table 主讲课程 
--    drop foreign key FK_主讲课程_主讲课程2_课程;

-- alter table 发表论文 
--    drop foreign key FK_发表论文_发表论文_教师;

-- alter table 发表论文 
--    drop foreign key FK_发表论文_发表论文2_论文;

-- alter table 承担项目 
--    drop foreign key FK_承担项目_承担项目_教师;

-- alter table 承担项目 
--    drop foreign key FK_承担项目_承担项目2_项目;

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
   primary key (工号, 课程号)
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
   承担经费                 float  comment '',
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
   总经费                  float  comment '',
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

