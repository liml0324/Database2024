
Drop Procedure if exists modify_book_ID;
Delimiter //
CREATE PROCEDURE modify_book_ID(IN old_ID CHAR(8), IN new_ID CHAR(8))
BEGIN
	declare 
	n1, n2 int;
	-- 检查新旧ID是否已在表中
	select count(*) from Book where ID=old_ID into n1;
	select count(*) from Book where ID=new_ID into n2;
	if n1=1 and n2=0 and not old_ID like '00%' and not new_ID like '00%' then
		update Book set ID=new_ID where ID=old_ID;
		update Borrow set book_ID=new_ID where book_ID=old_ID;
	end if;
END //
Delimiter ;

