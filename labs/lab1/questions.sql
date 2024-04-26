use library1;
-- 1
Select ID, address from Reader where name='Rose';

-- 2
select Book.name, Borrow.Borrow_Date 
from Reader, Book, Borrow
where Reader.ID=Borrow.Reader_ID and Book.ID=Borrow.book_ID and Reader.name='Rose';

-- 3
select name from Reader
where ID not in (select Reader_ID from Borrow);

-- 4
select name, price from Book where author='Ullman';

-- 5
select Book.ID, Book.name 
from Book, Borrow, Reader
where Book.ID=Borrow.book_ID and Reader.ID=Borrow.Reader_ID and Borrow.Return_Date is null and Reader.name='李林';

-- 6
select Reader.name
from Reader, Borrow
where Reader.ID=Borrow.Reader_ID
group by Reader.ID
having count(Borrow.book_ID)>3;

-- 7
select name, ID from Reader
where ID not in
(select Reader.ID
from Reader, Borrow
where Reader.ID=Borrow.Reader_ID and Borrow.book_ID in
(select Borrow.book_ID from Borrow, Reader
where Reader.ID=Borrow.Reader_ID and Reader.name='李林'));

-- 8
select name, ID from Book where name like "%MySQL%";

-- 9
select Reader.ID, Reader.name, Reader.age, count(Borrow.book_ID) as borrow_num
from Reader, Borrow
where Reader.ID=Borrow.Reader_ID and YEAR(Borrow.Borrow_Date)=2023
group by Reader.ID, Reader.name, Reader.age
order by borrow_num desc
limit 20;

-- 10
drop view if exists Borrow_info;
create view Borrow_info as
select Reader.ID as Reader_ID, Reader.name as Reader_name, Borrow.book_ID, Book.name as book_name, Borrow.Borrow_Date
from Reader, Borrow, Book
where Reader.ID=Borrow.Reader_ID and Book.ID=Borrow.book_ID;

select Reader_ID, count(*) from Borrow_info
where Borrow_Date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
group by Reader_ID;