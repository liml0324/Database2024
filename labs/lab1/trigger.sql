use library1;

drop trigger if exists when_insert_Borrow;
Delimiter //
create trigger when_insert_Borrow After Insert on Borrow
for each row
begin
	declare 
		new_book_ID, new_Reader_ID char(8);
	declare
		new_Borrow_Date, new_Return_Date date;
	declare old_times int;
	set new_book_ID=NEW.book_ID;
    set new_Reader_ID=NEW.Reader_ID;
	set new_Borrow_Date=NEW.Borrow_Date;
    set new_Return_Date=New.Return_Date;
    -- 新的还书日期不为空，必然已经归还
    if new_Return_Date is not null then
		update Book set status=0 where ID=new_book_ID;
	elseif new_Borrow_Date is not null then
		-- 否则如果新的借书日期不为空，必然已经借出
		update Book set status=1 where ID=new_book_ID;
    end if;
	select times into old_times from Book where ID=new_book_ID;
    update Book set times=old_times+1 where ID=new_book_ID;
--     Insert Into Debug (Borrow_Date, Return_Date)
-- 	value
-- 		(new_Borrow_Date, new_Return_Date);
end //
Delimiter ;

drop trigger if exists when_update_Borrow;
Delimiter //
create trigger when_update_Borrow After Update on Borrow
for each row
begin
	declare 
		new_book_ID, new_Reader_ID char(8);
	declare
		new_Borrow_Date, new_Return_Date date;
	declare old_times int;
	set new_book_ID=NEW.book_ID;
    set new_Reader_ID=NEW.Reader_ID;
	set new_Borrow_Date=NEW.Borrow_Date;
    set new_Return_Date=New.Return_Date;
    -- 新的还书日期不为空，必然已经归还
    if new_Return_Date is not null then
		update Book set status=0 where ID=new_book_ID;
	elseif new_Borrow_Date is not null then
		-- 否则如果新的借书日期不为空，必然已经借出
		update Book set status=1 where ID=new_book_ID;
    end if;
	select times into old_times from Book where ID=new_book_ID;
    if old.Borrow_Date is null and new.Borrow_Date is not null then
		update Book set times=old_times where ID=new_book_ID;
    end if;
--     Insert Into Debug (Borrow_Date, Return_Date)
-- 	value
-- 		(new_Borrow_Date, new_Return_Date);
end //
Delimiter ;