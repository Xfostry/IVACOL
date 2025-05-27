
-- David Esteban Palma
-- Deiby Alejandro Rodriguez 

use electroya;
-- ej 1
insert into productos (nombre, precio, stock, categoria) 
values	("Auriculares Bose QuietComfort", 900000, 30, "Audio");
    
insert into clientes (nombre, email, direccion) 
values	("María González","maria.gonzalez@gmail.com", "Cll 80 #30-15, Bogotá");
    
insert into pedidos (fecha, total, idcliente) 
values 	('2025-04-10', 500000, 3);

-- ej 2

select * from productos
where precio > 1000000;

select * from clientes
where direccion like "%Bogotá%";

select * from productos
where categoria = "Audio";

select * from pedidos
where total > 1000000;

-- ej 3

select * from productos
order by precio asc;

select * from clientes
order by nombre asc;

select * from pedidos
order by fecha desc;

-- ej 4
select 
	pr.id,
    pr.nombre
from detallespedido dp
join pedidos p
join productos pr on pr.id = p.id
where p.id = 5
group by pr.id, p.id;


select
	c.nombre,
    p.total
from clientes c
join pedidos p
where p.total > 500000;

select 
    p.nombre as nombre_producto,
    dp.cantidad,
    dp.precioUnitario,
    pe.fecha as fecha_pedido,
    c.nombre as nombre_cliente
from detallespedido dp
join productos p on dp.idproducto = p.id
join pedidos pe on dp.idpedido = pe.id
join clientes c on pe.idcliente = c.id
order by pe.fecha desc;


-- ej 5

update productos
set precio = 2800000
where id = 2;

update productos
set stock = 45
where id = 15;

update clientes
set direccion = "Av. 3 de Mayo #8-40, Cali"
where id = 3;

select * from productos;

select * from clientes;

-- ej 6

select
	categoria, 
	count(stock) as cantidad_productos
from productos
group by categoria
order by cantidad_productos desc;
    
select c.nombre, sum(p.total) as total_gastado
from clientes c
join pedidos p on c.id = p.idcliente
group by c.id, c.nombre
order by total_gastado desc;

select 
	categoria, 
    format(avg(precio), 0) as precio_promedio
from productos
group by categoria
order by precio_promedio desc;

select 
	c.nombre as nombre_cliente, 
    p.nombre as nombre_producto, 
    sum(dp.cantidad) as cantidad_total
from clientes c
join pedidos pe on c.id = pe.idcliente
join detallespedido dp on pe.id = dp.idpedido
join productos p on dp.idproducto = p.id
group by c.id, p.id
order by cantidad_total desc;

select 
	p.categoria, 
    sum(dp.cantidad) as Ventas_Totales
from detallespedido dp
join productos p on dp.idproducto = p.id
group by p.categoria
order by Ventas_Totales desc;





	

