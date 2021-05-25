create database shop
use shop

create table in_stock (
	stock_id integer identity(1,1),
	constraint pk_stock primary key(stock_id),
	sell_price integer,
	stock_q integer
)

alter table in_stock add stock_name varchar(10)
create table buyer_stock (
	buyer_id integer,
	stock_id integer,
	constraint pk_bs primary key(buyer_id, stock_id),
	quantity integer,
	buy_price integer,
)

create table buyer_info (
	buyer_id integer identity(1,1),
	constraint pk_bi primary key(buyer_id),
	buyer_name varchar(15),
	buyer_address varchar(30),
)

create table costumers (
	costumer_id integer identity(1,1),
	constraint pk_costumers primary key(costumer_id),
	costumer_name varchar(20),
	costumer_address varchar(30)
)

create table detail_order (
	order_id integer identity(1,1),
	constraint pk_do primary key(order_id),
	date_ordered date,
	date_delivered date,
	costumer_id integer,
	total_price integer,
	paid varchar(1)
)

create table orders (
	order_id integer,
	stock_id integer,
	constraint pk_order primary key(order_id, stock_id),
	num_ordered integer,
)

create table defaulters (
	defaulter_id integer identity(1,1),
	order_id integer,
	constraint pk_defaulters primary key(defaulter_id)
)

create table profit (
	the_month varchar(10),
	constraint pk_profit primary key(the_month),
	the_profit integer
)

create table purchase_date (
	buyer_id integer,
	stock_id integer,
	quantity integer,
	purchase_date date not null,
	constraint pk_purchase primary key(buyer_id, stock_id, purchase_date)
)

insert into in_stock values (12000, 9000)
insert into in_stock values (120000, 19000)
insert into in_stock values (15000, 90000)
insert into in_stock values (10900, 1000)
insert into in_stock values (2000, 8000)
insert into in_stock values (12090, 10000)
insert into in_stock values (50000, 9500)
insert into in_stock values (47200, 100)
insert into in_stock values (37500, 9500)
insert into in_stock values (8900, 5000)

update in_stock set stock_name = 'Monitor' where stock_id = 1
update in_stock set stock_name = 'Computer' where stock_id = 2
update in_stock set stock_name = 'Keyboard' where stock_id = 3
update in_stock set stock_name = 'Mouse' where stock_id = 4
update in_stock set stock_name = 'HeadPhones' where stock_id = 5
update in_stock set stock_name = 'PS5' where stock_id = 6
update in_stock set stock_name = 'Printer' where stock_id = 7
update in_stock set stock_name = 'iPhone12' where stock_id = 8
update in_stock set stock_name = 'LapTop' where stock_id = 9
update in_stock set stock_name = 'Flascard' where stock_id = 10

insert into buyer_info values ('Uni-Care', 'Japan, Tokyo')
insert into buyer_info values ('Greentest', 'Kazakhstan, Almaty')
insert into buyer_info values ('Technics', 'Russia, Moscow')
insert into buyer_info values ('Digitals', 'Korea, Seoul')
insert into buyer_info values ('Vestidots', 'Beijing, China')
insert into buyer_info values ('OptMob', 'Berlin, Germany')

insert into buyer_stock values (1, 1, 1000, 8000)
insert into buyer_stock values (1, 5, 1000, 1200)
insert into buyer_stock values (2, 10, 20000, 7000)
insert into buyer_stock values (3, 6, 5000, 9990)
insert into buyer_stock values (3, 7, 5000, 38000)
insert into buyer_stock values (3, 9, 5000, 20000)
insert into buyer_stock values (4, 8, 1500, 35000)
insert into buyer_stock values (4, 2, 1500, 100000)
insert into buyer_stock values (5, 4, 7000, 8500)
insert into buyer_stock values (6, 3, 3000, 11000)

insert into costumers values ('Kenneth Hampton', 'Kazakhstan, Almaty')
insert into costumers values ('Bonnie Morton', 'Kazakhstan, Nur-Sultan')
insert into costumers values ('Vivien Glenn', 'Ukrain, Kyiv')
insert into costumers values ('Joseph Ross', 'Belarus, Minsk')
insert into costumers values ('Alice Paul', 'Russia, Moscow')

insert into detail_order values ('01.01.2021', '11.01.2021', 1, 0, 'T')
insert into detail_order values ('02.01.2021', '12.01.2021', 2, 0, 'T')
insert into detail_order values ('03.01.2021', null, 3, 0, 'F')
insert into detail_order values ('04.01.2021', '14.01.2021', 4, 0, 'T')
insert into detail_order values ('05.01.2021', '15.01.2021', 4, 0, 'T')
insert into detail_order values ('06.01.2021', '16.01.2021', 5, 0, 'T')
insert into detail_order values ('07.01.2021', null, 2, 0, 'F')
insert into detail_order values ('11.02.2021', '21.02.2021', 1, 0, 'T')
insert into detail_order values ('12.02.2021', '22.02.2021', 2, 0, 'T')
insert into detail_order values ('04.03.2021', '14.03.2021', 4, 0, 'T')
insert into detail_order values ('05.03.2021', '15.03.2021', 4, 0, 'T')
insert into detail_order values ('06.03.2021', '16.03.2021', 5, 0, 'T')

insert into orders values (1, 1, 2)
insert into orders values (1, 10, 1)
insert into orders values (2, 7, 1)
insert into orders values (3, 5, 1)
insert into orders values (3, 2, 3)
insert into orders values (4, 4, 4)
insert into orders values (5, 9, 2)
insert into orders values (5, 8, 4)
insert into orders values (6, 6, 1)
insert into orders values (7, 3, 2)
insert into orders values (7, 9, 5)
insert into orders values (8, 5, 1)
insert into orders values (8, 9, 2)
insert into orders values (9, 3, 4)
insert into orders values (10, 7, 1)
insert into orders values (11, 2, 4)
insert into orders values (12, 10, 5)

declare @a int
set @a = 0
while @a <= 12
begin
	update detail_order set total_price = (select sum(o.num_ordered*s.sell_price) 
	from orders o join in_stock s on o.stock_id = s.stock_id
	where o.order_id = @a) where order_id = @a
	set @a = @a+1
end

select * from detail_order

insert into defaulters (order_id) select order_id from detail_order where paid like 'F' 
and order_id not in (select order_id from defaulters)

set LANGUAGE russian
GO

create FUNCTION comf_date (@date date)
RETURNS VARCHAR(15)
BEGIN
    declare @out VARCHAR(15);
    set @out=CONVERT(varchar,@date,105);
    RETURN @out
END
GO

select buyer_id,stock_id,quantity,dbo.comf_date(purchase_date) as purch_date from purchase_date

insert into purchase_date VALUES (1,3,1000,'01.01.2021')
insert into purchase_date VALUES (2,10,2000,'03.01.2021')
insert into purchase_date VALUES (1,5,3000,'05.01.2021')

select * from profit

alter table profit
drop pk_profit

alter TABLE profit
alter COLUMN the_month NVARCHAR(20) NOT NULL

alter table profit
add constraint pk_profit primary key(the_month)

insert into profit values (N'Январь', 0)
insert into profit values (N'Февраль', 0)
insert into profit values (N'Март', 0)
update profit set the_profit = (select sum((i.sell_price - b.buy_price)*o.num_ordered) 
from in_stock i join buyer_stock b on i.stock_id = b.stock_id
join orders o on i.stock_id = o.stock_id
join detail_order d on d.order_id = o.order_id
where DateName( month , DateAdd( month , month(d.date_ordered) , 0 ) - 1 ) = the_month)

select*from profit

alter table buyer_stock add constraint fk_bs foreign key(stock_id) references in_stock(stock_id)
alter table buyer_stock add constraint fk_buyerstock foreign key(buyer_id) references buyer_info(buyer_id)
alter table detail_order add constraint fk_do foreign key(costumer_id) references costumers(costumer_id)
alter table orders add constraint fk_orders foreign key(order_id) references detail_order(order_id)
alter table defaulters add constraint fk_defaulters foreign key(order_id) references detail_order(order_id)
alter table purchase_date add constraint fk_purchase foreign key(buyer_id) references buyer_info(buyer_id)
alter table purchase_date add constraint fk_pd foreign key(stock_id) references in_stock(stock_id)

select s.stock_name, sum(o.num_ordered) as orders
from in_stock s join orders o
on s.stock_id = o.stock_id 
group by s.stock_name order by orders desc

select c.costumer_name as Costumer, count(d.order_id) as orders
from costumers c join detail_order d
on c.costumer_id = d.costumer_id
group by c.costumer_name order by orders desc

select s.stock_name, (i.sell_price - b.buy_price) as profit
from in_stock s join in_stock i on s.stock_id = i.stock_id
join buyer_stock b on b.stock_id = i.stock_id
order by profit desc

select i.buyer_name, count(b.stock_id) as items
from buyer_info i join buyer_stock b
on i.buyer_id = b.buyer_id
group by i.buyer_name order by items desc

select b.buyer_name as buyer, s.stock_name as stock, p.purchase_date as purchase
from purchase_date p join buyer_info b on p.buyer_id = b.buyer_id
join stock_decs s on p.stock_id = s.stock_id

select c.costumer_name as costumer, c.costumer_address as address
from costumers c join detail_order d on c.costumer_id = d.costumer_id
join orders o on o.order_id = d.order_id 
join in_stock s on s.stock_id = o.stock_id
where s.stock_name like 'LapTop' and d.paid not like 'F'

/*1*/
create table to_buy(
	stock_id integer,
	constraint pk_to_buy primary key(stock_id),
	stock_name varchar(10)
)

alter table to_buy
add CONSTRAINT fk_tb FOREIGN KEY(stock_id) REFERENCES in_stock(stock_id)

select*from in_stock

create index ix_stock_q on in_stock(stock_q)

select*from to_buy
select*from buyer_stock
GO

create trigger purchase_done
on purchase_date
after insert, update as
begin
	update in_stock set stock_q = stock_q + (select quantity from inserted)
	where stock_id = (select stock_id from inserted)
	delete from to_buy where stock_id = (select stock_id from inserted)
end
GO

create trigger to_buy_insert_delete
on to_buy 
after insert, delete as
begin
	declare @action varchar(20)
	set @action = (case when exists(select*from inserted)
						then 'insert'
						when exists(select*from deleted)
						then 'delete'
					end)
	declare @name varchar(10)
	if @action = 'insert'
	begin
		set @name = (select stock_name from inserted)
		print concat(N'Товар ',@name ,N' требует закупа!')
	end
	else begin
		set @name = (select stock_name from deleted)
		print concat(N'Товар ',@name ,N' больше не требует закупа!')
	end
end
GO

create function stock_name
(@id integer)
returns varchar(10) as
begin
	declare @name varchar(10) = 
	(select stock_name from in_stock where stock_id = @id)
	return(@name)
end
GO

create procedure stock_to_buy as
begin
	declare @a integer = (select max(stock_id) from in_stock)
	declare @i integer = 1
	while @i <= @a
	begin
		declare @quantity integer = (select stock_q from in_stock where stock_id = @i)
		if @quantity <= 100 and @i not in (select stock_id from to_buy)
		begin
			insert into to_buy values(@i,dbo.stock_name(@i))
		end
	set @i = @i+1
	end
end
GO

update in_stock set stock_q = 45 where stock_id = 4 or stock_id = 8
exec stock_to_buy
select*from to_buy
select*from purchase_date
insert into purchase_date values(3,4,1000,'23.04.21')

/*5*/
create table order_status(
	status varchar(5),
	constraint pk_status primary key(status),
	status_desc varchar(100)
)

alter TABLE order_status
alter column status_desc NVARCHAR(100)

insert into order_status values('F', N'Поиск заказа')
insert into order_status values('C', N'Сбор заказа')
insert into order_status values('S', N'Отправка заказа')
insert into order_status values('D', N'Заказ выполнен')

select*from orders
select*from detail_order
alter table detail_order add Status varchar(5)
update detail_order set status = 'D'
alter table detail_order add constraint fk_do_status foreign key(Status) references order_status(status) 
GO

create function total_price (@id integer)
returns integer as
begin
	declare @total integer = (select sum(o.num_ordered*s.sell_price) 
	from orders o join in_stock s on o.stock_id = s.stock_id
	where o.order_id = @id)
	return @total
end
GO

create procedure online_order
@costumer_id integer
as
begin
	declare @date date = convert(date, getdate())
	insert into detail_order values(@date, null, @costumer_id, null, 'F', 'F')
end

select * from detail_order
GO

create trigger paid_status
on detail_order 
after update as
begin
	declare @id integer = (select order_id from inserted)
	declare @paid varchar(1) = (select paid from detail_order where order_id = @id)
	declare @date date = (select date_delivered from detail_order where order_id = @id)
	if @paid = 'T'
		update detail_order set Status = 'S' where order_id = @id
	if @date is not null
		update detail_order set Status = 'D' where order_id = @id
end
GO

create trigger stock_update
on orders 
after insert as
begin
	declare @id integer = (select order_id from inserted)
		update detail_order set Status = 'C' where order_id = @id
		update detail_order set total_price = dbo.total_price(@id) where order_id = @id
		update in_stock set stock_q = stock_q - (select num_ordered from inserted)
		where stock_id = (select stock_id from inserted)
end
GO

create trigger order_id
on detail_order
after insert as
begin
	declare @id integer = (select order_id from inserted)
	print concat(N'Новый заказ с id ',@id)
end
GO

--DBCC TRACEON (2528, -1)

--delete from detail_order WHERE order_id=1006

select*from order_status
select*from in_stock
select*from detail_order
select*from orders
exec online_order @costumer_id = 3
exec online_order @costumer_id = 1
select*from orders
insert into orders values(1007,1,100)
insert into orders values(1007,6,300)
insert into orders values(1007,3,30)
insert into orders values(1007,2,30)

SELECT * from costumers

insert into orders values((select max(order_id) from detail_order),1,100)
update detail_order set paid = 'T' where order_id = 1007
update detail_order set date_delivered = '25.05.21' where order_id = 1007

select*from costumers
/*3*/
select*from detail_order
create table bonus_cards(
	costumer_id integer,
	constraint pk_bonus primary key(costumer_id),
	constraint fk_bonus foreign key(costumer_id) references costumers(costumer_id),
	bonuses integer,
	open_date date,
	last_bonus date
)

create table presents(
	present_id integer identity(1,1),
	constraint pk_presents primary key(present_id),
	present_name varchar(50),
	present_price integer
)

insert into presents values('PowerBank', 7000)
insert into presents values('Headphones', 3000)
insert into presents values('SmartTag', 5000)
insert into presents values('Laptop Bag', 1200)
insert into presents values('Lamp', 4500)
insert into presents values('FlashCard', 2700)

create table presents_bonus(
	id integer identity(1,1),
	costumer_id integer,
	constraint pk_present_bonus primary key(id),
	constraint fk_present_bonus foreign key(costumer_id) references costumers(costumer_id),
	present_id integer,
	constraint fk_bonus_present foreign key(present_id) references presents(present_id)
)

create function calculate_bonuses (@id integer)
returns decimal(10,2) as
begin
	declare @bonus decimal(10,2) = 
	(select sum(total_price*0.001) from detail_order
	where costumer_id = @id)
	return @bonus
end

create trigger bonus_update
on detail_order
after insert, update as
begin
	declare @id integer = (select costumer_id from inserted)
	declare @status varchar(5) = (select Status from detail_order where order_id = (select order_id from inserted))
	if @status = 'D'
	begin
		if @id in (select costumer_id from bonus_cards)
		begin
			update bonus_cards set last_bonus = (select date_ordered from inserted) where costumer_id = @id
			update bonus_cards set bonuses = dbo.calculate_bonuses(@id) where costumer_id = @id
		end
		else begin
			declare @date date = (select date_ordered from inserted)
			insert into bonus_cards values(@id,dbo.calculate_bonuses(@id), @date,@date)
		end
	end
end

create trigger presents_bonus_trade
on presents_bonus
after insert as
begin
	declare @trans integer = (select id from inserted)
	declare @id integer = (select costumer_id from inserted)
	declare @present integer = (select present_id from inserted)
	declare @bonus integer = (select bonuses from bonus_cards where costumer_id = @id)
	declare @price integer = (select present_price from presents where present_id = @present)
	if @bonus >= 5000 and @bonus >= @price
	begin
		update bonus_cards set bonuses = bonuses - @price
		where costumer_id = @id
		print ('Обмен бонусов на подарки прошел успешно!')
	end
	else begin
		delete from presents_bonus where id = @trans
		print ('Недостаточно бонусов!')
	end
end

create function cost_name (@id integer)
returns varchar(20) as
begin
	declare @name varchar(20) = (select costumer_name from costumers where costumer_id = @id)
	return @name
end

create procedure pay_by_bonuses (@order_id integer) as
begin
	declare @total integer = (select total_price from detail_order where order_id = @order_id)
	declare @costumer integer = (select costumer_id from detail_order where order_id = @order_id)
	declare @bonuses integer = (select bonuses from bonus_cards where costumer_id = @costumer)
	if @bonuses >= 5000 and @bonuses >= @total
	begin
		update bonus_cards set bonuses = bonuses - @total where costumer_id = @costumer
		update detail_order set total_price = 0 where order_id = @order_id
		update detail_order set paid = 'T' where order_id = @order_id
		print concat('Покупка номер ', @order_id, ' оплачена бонусами!')
	end
	else begin
		print 'Недостаточно бонусов!'
	end
end

create procedure presents_trade (@costumer_id integer, @present_id integer) as
begin
	insert into presents_bonus values(@costumer_id, @present_id)
end

create trigger bonus_messenges 
on bonus_cards
after update as
begin
	declare @id integer = (select costumer_id from inserted)
	declare @bonus integer = (select bonuses from inserted)
	declare @day date = (select dateadd(day, 3, last_bonus) from inserted)
	if @bonus >= 5000 and @bonus < 10000
	begin
		print concat('Пользователь ', dbo.cost_name(@id), ' может начать использовать свои бонусы!')
	end
	if @bonus >= 10000
	begin
		print concat('Пользователь ', dbo.cost_name(@id), ' должен использовать бонусы до ', @day)
	end
end

create index ix_bonus on bonus_cards(bonuses)

create procedure check_bonus as
begin
	declare @id integer = 1
	declare @max integer = (select max(costumer_id) from bonus_cards)
	declare @date date = convert(date, getdate())
	while @id <= @max
	begin
		if @id in (select costumer_id from bonus_cards where bonuses >= 10000 and datediff(day, last_bonus, @date) >= 3)
		begin
			update bonus_cards set bonuses = 0 where costumer_id = @id
			print concat('Бонусы пользователя ', dbo.cost_name(@id), ' обнулены!') 
		end
		if @id in (select costumer_id from bonus_cards where datediff(year, open_date, @date) >= 1)
		begin
			delete from bonus_cards where costumer_id = @id
			print concat('Срок действия бонусной карты пользователя ', dbo.cost_name(@id), ' истек!')
		end
	set @id = @id+1
	end
end

select*from bonus_cards
select*from detail_order
select*from presents_bonus
exec online_order @costumer_id = 3
insert into orders values (20, 5, 1)
exec pay_by_bonuses @order_id = 21
exec presents_trade @costumer_id = 3, @present_id = 4
exec presents_trade @costumer_id = 1, @present_id = 4
exec online_order @costumer_id = 3
insert into orders values (25, 5, 1)
update bonus_cards set bonuses = 100000 where costumer_id = 4
exec pay_by_bonuses @order_id = 24
update detail_order set status = 'D' where order_id = 25

exec presents_trade @costumer_id = 4, @present_id = 3
exec presents_trade @costumer_id = 4, @present_id = 2
exec online_order @costumer_id = 4
insert into orders values(24, 3, 20)

update bonus_cards set open_date = '02.05.2020' where costumer_id = 1
exec online_order @costumer_id = 4
insert into orders values (22, 5, 10)
insert into orders values (22, 2, 10)
update detail_order set status = 'D' where order_id = 22
exec check_bonus
select*from detail_order
select*from bonus_cards
update bonus_cards set bonuses = 15470 where costumer_id = 4
update bonus_cards set last_bonus = '30.04.2021' where costumer_id = 3
exec check_bonus

exec online_order @costumer_id = 4
insert into orders values (23, 5, 5)
exec pay_by_bonuses 23

/*2*/
create table discounts(
	stock_id integer,
	constraint fk_discounts foreign key(stock_id) references in_stock(stock_id),
	discount integer
)

create function new_price(@stock_id integer, @discount integer)
returns decimal(10,2) as
begin
	declare @percent decimal(5,2) = @discount*0.01
	declare @price decimal(10,2) = 
	(select (sell_price - sell_price*@percent) from in_stock where stock_id = @stock_id)
	return @price
end

create procedure set_discount as
begin
	declare @today date = convert(date, getdate())
	declare @last_day date = (select distinct last_date from discounts)
	if day(@today) = 5 and datediff(day, @last_day, @today) >= 28
	begin
		declare @max integer = (select max(stock_id) from discounts)
		declare @i integer = 1
		while @i <= @max
		begin
			if @i in (select stock_id from discounts)
			begin
				update in_stock set sell_price = 
				(select i.sell_price/(1-d.discount/100) from in_stock i join discounts d on d.stock_id = i.stock_id where i.stock_id = @i)
				where stock_id = @i
			end
			set @i = @i +1
		end
		delete from discounts
	end
end

create trigger new_discounts 
on discounts
after delete as
begin
	declare @today date = convert(date, getdate())
	declare @max integer = (select max(stock_id) from in_stock)
	declare @amount integer = floor(RAND()*(@max-1+1))+1
	declare @i integer = 1
	while @i <= @amount
	begin
		declare @stock integer = floor(RAND()*(@max-1+1))+1
		declare @discount integer = floor(RAND()*(70-10+1))+10
		if @stock not in (select stock_id from discounts)
		begin
			insert into discounts values (@stock, @discount, @today)
			update in_stock set sell_price = dbo.new_price(@stock, @discount) where stock_id = @stock
		end
		set @i = @i+1
	end
end

exec set_discount
select*from discounts
select*from in_stock
update discounts set last_date = '05.04.21'

select stock_id, dbo.new_price(stock_id, 10) from in_stock

/* 4 */
create table accounts(
	acc_id int PRIMARY KEY,
	acc_name VARCHAR(25),
	wealth int
)

insert into accounts VALUES(1,'Boss',3000,'February')
insert into accounts VALUES(2,'Shop',30000,'February')

alter table accounts
add last_upd VARCHAR(25)

select *from accounts

create table employees(
	emp_id int IDENTITY(1,1) primary key,
	emp_wage int
)

insert into employees VALUES(1000)
insert into employees VALUES(800)
insert into employees VALUES(800)
insert into employees VALUES(800)

select * from employees

create FUNCTION profit_fun
(@mes varchar(25))
RETURNS @T table(profit_ int,mon_ VARCHAR(25))
as
BEGIN
	declare @emp_wages int=(select sum(emp_wage) from employees);
	with dinam as 
	(select sum(
		case
			when total_price=0 then -sell_price*num_ordered
			else (sell_price-buy_price)*num_ordered
		end
		)-@emp_wages as profit,DATENAME(month,date_ordered) as mon
	from detail_order do 
	join orders o on do.order_id=o.order_id 
	join buyer_stock bs on bs.stock_id=o.stock_id 
	join in_stock ins on ins.stock_id=o.stock_id
	GROUP by DATENAME(month,date_ordered)
	HAVING DATENAME(month,date_ordered)=@mes
	)
	INSERT into @T
	select profit, mon
	from dinam
	RETURN
END

select * from dbo.profit_fun('April')
select * from detail_order

drop PROCEDURE month_profit

create PROCEDURE month_profit
@mes VARCHAR(25)
as
BEGIN
declare @p int=(select profit_ from dbo.profit_fun(@mes))
update accounts
set wealth=wealth+0.5*@p,
last_upd=@mes
where dbo.fn_month_name_to_number(@mes)>dbo.fn_month_name_to_number(last_upd)
and @p is not null
END

exec month_profit 'May'

SELECT * from accounts

create function fn_month_name_to_number (@monthname varchar(25))
returns int as
begin
declare @monthno as int;
select @monthno =
case @monthname
when 'January' then 1
when 'February' then 2
when 'March' then 3
when 'April' then 4
when 'May' then 5
when 'June' then 6
when 'July' then 7
when 'August' then 8
when 'September' then 9
when 'October' then 10
when 'November' then 11
when 'December' then 12
end
return @monthno
end

select dbo.fn_month_name_to_number('May')


/* 6 */
CREATE PROCEDURE controll as
begin
    SELECT SUM(total_price) FROM detail_order ;   
end
create table his( 
orders char(20)null,
new_total_price float null,
old_total_price float null,
date datetime null
);
create trigger history
on detail_order
after update as if update(total_price) 
begin
    declare @new_total_price float
 declare @old_total_price float
 declare @orders char(20)
 select @new_total_price=(select total_price from inserted)
 select @old_total_price =(select total_price from deleted)
 select @orders = (select order_id from deleted )
 insert into his values(@orders,@new_total_price,@old_total_price,getdate())
 end
CREATE FUNCTION cheking (@the_profit integer)
RETURNS VARCHAR(40) as
    BEGIN
     DECLARE @sf_value VARCHAR(40);
        IF @the_profit >= 0
            SET @sf_value = 'Mozhno prodolzhit';
        ELSE
            SET @sf_value = 'Ne rekomenduetsya prodolzhat';
     RETURN @sf_value;
    END
GO

/*create trigger otmena 
on detail_order
after delete as
begin
	insert into his (orders,new_total_price,old_total_price,date)
	select order_id,'отменен товар на сумму'+total_price  from deleted
end*/

create table admins (
	login varchar(20),
	password varchar(30)
)
GO

create table custs_login (
	cust_id int,
	login varchar(30),
	PASSWORD VARCHAR(14),
	constraint pk_custs PRIMARY KEY(cust_id),
	CONSTRAINT pk_to_customer FOREIGN KEY(cust_id) REFERENCES costumers(costumer_id)
)

alter table custs_login
drop pk_to_customer

alter table custs_login
add CONSTRAINT fk_to_customer FOREIGN KEY(cust_id) REFERENCES costumers(costumer_id)

insert into admins values('a_anarbekova', 'Abcdefg1234')
insert into admins values('e_kurmangali', 'Qwerty8910')

--fill custs_login
INSERT into custs_login VALUES(1,'ken_ham','kenhem123.')
INSERT into custs_login VALUES(2,'bon_mor','bonmor123..')
INSERT into custs_login VALUES(3,'viv_gle','vivgle123.')
INSERT into custs_login VALUES(4,'jos_ros','josros123.')
INSERT into custs_login VALUES(5,'ali_pau','alipau123.')


select*from admins
select*from custs_login

select * from custs_login cl
join costumers c on
c.costumer_id=cl.cust_id
where login='bon_mor' and PASSWORD='bonmor123..'

select *from in_stock
SELECT*from costumers
SELECT*from detail_order
select*from orders

select costumer_id from costumers where costumer_name = 'Yera Kenzh' and costumer_address = 'Kz,Shym'