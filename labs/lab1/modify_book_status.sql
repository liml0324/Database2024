
drop trigger if exists modify_book_status;
Delimiter //
create trigger modify_book_status After Insert on Borrow
for each row
begin
	declare 
		new_book_ID, new_Reader_ID char(8);
	declare
		new_Borrow_Date, new_Return_Date date;
	set new_book_ID=NEW.book_ID;
    set new_Reader_ID=NEW.Reader_ID;
	set new_Borrow_Date=NEW.Borrow_Date;
    set new_Return_Date=New.Return_Date;
    -- 新的还书日期不为空，必然已经归还
    if not new_Return_Date=null and not new_Return_Date='1970-01-01' then
		update Book set status=0 where ID=new_book_ID;
	else 
		-- 否则如果新的借书日期不为空，必然已经借出
		if not new_Borrow_Date=null then
			update Book set status=1 where ID=new_book_ID;
		end if;
    end if;
end //
Delimiter ;