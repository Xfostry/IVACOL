use electroya;

select * from productos;

select nombre, precio from productos;

select
	nombre as Producto,
    precio as Precio_Unitario_$
from Productos;

select
	nombre as Producto,
    format(precio,0,'es_CO') as Precio_Unitario_$
from Productos;

-- Consultar con una condicion
select nombre, stock from Productos
where stock <= 50;

select nombre, categoria from Productos
where categoria = 'Accesorios';  -- si esta mal escrito no sale nada

-- Consultar por precio
select
	nombre as Producto,
    format(precio,0,'es_CO' ) as Precio_Unitario_$
from Productos where precio > 1000000;

-- ordenar por precio de menos a mas
select
	nombre as Producto,
    format(precio,0,'es_CO') as Precio_Unitario_$
from Productos order by precio asc ; -- asc = ascentende desc = descendente

-- ordenar por columna nombre
select * from productos
order by nombre asc;

-- mostrar teniendo en cuenta inicio y fin
select * from productos
where precio between 100000 and 300000
order by nombre asc;


-- ver los productos por nombre 'Cámara de seguridad WiFi Ezviz'
select * from Productos 
where nombre = 'Cámara de seguridad WiFi Ezviz';

select * from Productos
where id = 25; -- no hay entonces no sale

select * from productos; 

-- Modificar el registro de la tabla principal y no temporalmente
update Productos
set precio = 46000
where id = 15; -- especificar donde para evitar problemas

-- ASI NO SIRVE pq toca desactivar modo seguro porque esta relacionada
-- update Productos
-- set precio = 46000
-- where nombre = 'Cámara de seguridad WiFi Ezviz'; 
-- no es recomendable pero se salta asi
-- set SQL_SAFE_UPDATES = 0;  -- 1 para volver a activar

update Productos
set categoria = 'Complementos'
where categoria = 'accesorios';

select * from productos; 

-- eliminar con DELETE
delete from productos
	where id = 1; -- no funca porque esta conectado a otras tablas

select * from detallesPedido
where idProducto = 1;

-- ponemos mas info noc pq
insert into Productos(nombre, precio, stock, categoria)
values
    ('Lámpara LED Escritorio Base USB', 65000, 35, 'Iluminación'),
    ('Disco SSD 512GB Kingston', 310000, 20, 'Almacenamiento'),
    ('Soporte Ajustable para Celular', 25000, 50, 'Accesorios'),
    ('Barra de Sonido Samsung 2.1', 480000, 12, 'Audio'),
    ('Cámara GoPro HERO11 Black', 1800000, 8, 'Cámaras');

delete from productos
	where id = 22; -- los nuevos q no estan conectados (disco ssd)
    
    
-- sumar
select sum(stock) as stock_total from productos;
-- contar
select count(stock) as stock_total from productos;

-- tiene el 20% extra '.2'
select sum(stock)* 1.2 as stock_total from productos;


-- ver pedidos por cliente
select 
	pedidos.id as Numero_Pedido, 
    pedidos.fecha as Fecha, 
    pedidos.idCliente,
	clientes.nombre
from Pedidos -- se indica una tabla primero y luego se unen
join clientes on pedidos.idCliente = clientes.id -- join une tablas y on sirve para direccionar la llave foranea
order by pedidos.id asc;

-- lo mismo pero mas barato
 select 
	p.id as Numero_Pedido, 
    p.fecha as Fecha, 
    p.idCliente,
	c.nombre
from Pedidos p  -- despues de un espacio se pone el name pa llamarlo 'solo funciona en tablas'
join clientes c on p.idCliente = c.id
order by p.id asc;

-- sumadrepuntocom

-- show columns p;   -- no sirve pq el alias aca no existe
-- mamawebo

select * from pedidos;

select
	pr.nombre as Nombre_Producto,
    dp.cantidad,
    format(pr.precio, 0, "es_CO") as Precio_Unitario,
	format(dp.cantidad * pr.precio, 0, "es_CO") as Total_linea,
    dp.idPedido
from detallesPedido dp
join productos pr on dp.idProducto = pr.id
where dp.idPedido = 1;

-- Ver pedido con la fecha, el nombre del cliente y el total del pedido 1
select
    p.id as Pedido_No,
    p.fecha,
    c.nombre as Nombre_Cliente,
	format (dp.cantidad * pr.precio, 0, 'es_CO') as Total_Pedido,
        dp.idPedido as No_Pedido
from detallesPedido dp
join Productos pr on dp.inProducto = pr.id
join Pedidos p on dp.id
join Clientes c on p.idCliente = c.id
where dp.idPedido = 1;


-- por pedidos sacar total
select
   format (sum(cantidad * preciounitario), 0, 'es_CO') as Total_Pedido,
        dp.idPedido as No_Pedido
from detallesPedido dp
group by idPedido;

-- Todos los pedidos con sus totales pero que me muestre:
-- Numero del pedido, fecha del pedido





Kinky, nasty, y aunque sea fancy
Se pone cranky si lo hago romantic
Le gusta el sexo en exceso
Y en el proceso, me pide un beso

y la cosa suena rra 
scooby doo papa
y el bom bom bom bom bom 

puto el q lo lea











