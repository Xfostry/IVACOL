-- DDL Estructura

-- Crear Base de Datos
create database disquera;
-- drop database disquera;
-- Ingresar BD
use disquera;

-- Crear tabla  de Productos
create table Productos(
	id int primary key auto_increment,
	nombre varchar(100) not null,
	precio int not null,
	stock int not null,
	categoria varchar(50)
);

-- Borra tabla Productos
-- drop table Productos;

-- Borrar Base de Datos
-- drop database disquera;

-- Crear tabla  de Clientes
create table Clientes(
	id int primary key auto_increment,
	nombre varchar(100) not null,
	email varchar(100) not null,
	direccion varchar(200) 
);

-- Crear tabla  de Pedidos con llave Foranea
create table Pedidos(
	id int primary key auto_increment,
	fecha date not null,
    total int not null,
    idCliente int not null,
    foreign key (idCliente) references Clientes(id)
);

-- Crear tabla  de Detalles del Pedido con llave Foranea
create table detallesPedido(
	id int primary key auto_increment,
    cantidad int not null,
    precioUnitario int not null,
    idPedido int not null,
    idProducto int not null,
    foreign key (idPedido) references Pedidos(id),
    foreign key (idProducto) references Productos(id)
);

drop table detallesPedido;


-- Crear tabla  de Detalles del Pedido con foranea Pedido faltando al producto
create table detallesPedido(
	id int primary key auto_increment,
    cantidades int not null,
    precioUnitario int not null,
    idPedido int not null,
    idProducto int not null,
    foreign key (idPedido) references Pedidos(id)
);

-- Cambiar estructura de la tabla o adicionar una reelación(FK)
alter table detallesPedido
	add foreign key (idProducto) references Productos(id);
    
-- DML
-- Recuperar o mostrar informacion -- Select
select * from Productos; -- * 'asterisco' muestra todo

-- Cargar x en una tabla -- Insert into
INSERT INTO productos (nombre, precio, stock, categoria)
VALUES
	('Disco de Ayuwoki', 180000, 30, 'Musica'), -- sin comillas no se entiende como texto 
	('Camara pro', 5000000, 5, 'Fotografia'),
    ('Laptop HP Pavilion', 2500000, 15, 'Electrónica'),
    ('Samsung Galaxy S21', 2800000, 30, 'Tecnología'),
    ('Camiseta Adidas', 95000, 100, 'Ropa'),
    ('Mochila Nike', 130000, 50, 'Accesorios'),
    ('Televisor Samsung 55"', 3500000, 20, 'Electrónica'),
    ('Auriculares Sony WH-1000XM4', 1300000, 25, 'Electrónica'),
    ('Zapatos deportivos Puma', 180000, 40, 'Calzado'),
    ('Smartwatch Apple Series 7', 1500000, 18, 'Tecnología'),
    ('Cámara Canon EOS 90D', 4500000, 12, 'Fotografía'),
    ('Estufa a gas Teka', 950000, 22, 'Electrodomésticos'),
    ('Silla ergonómica Herman Miller', 3000000, 8, 'Mobiliario'),
    ('Perfume Chanel No. 5', 500000, 60, 'Cosméticos'),
    ('Bicicleta de montaña Trek', 1500000, 14, 'Deportes'),
    ('Lentes Ray-Ban Aviator', 350000, 35, 'Accesorios'),
    ('Xbox Series X', 4200000, 10, 'Videojuegos'),
    ('Pantalones Levi’s 501', 180000, 45, 'Ropa'),
    ('Aspiradora Dyson V11', 2500000, 7, 'Electrodomésticos'),
    ('Tablet Samsung Galaxy Tab S7', 2000000, 12, 'Electrónica'),
    ('Juego de sábanas Queen Size', 120000, 80, 'Hogar'),
    ('Cafetera Nespresso', 800000, 60, 'Electrodomésticos');
select * from productos;

select id as 'codigo del producto', nombre as 'nombre del producto', precio from productos; -- muestra todos los valores con lo que se pide 'id, nombre y precio'

INSERT INTO clientes (nombre, email, direccion)
VALUES
    ('Carlos Rodríguez', 'carlos.rodriguez@email.com', 'Calle 45 # 23-34, Bogotá, Cundinamarca'),
    ('Ana María Pérez', 'ana.perez@email.com', 'Avenida 19 # 78-56, Medellín, Antioquia'),
    ('Luis González', 'luis.gonzalez@email.com', 'Carrera 15 # 8-22, Cali, Valle del Cauca'),
    ('María Fernanda Díaz', 'maria.diaz@email.com', 'Calle 72 # 56-34, Barranquilla, Atlántico'),
    ('Jorge Martínez', 'jorge.martinez@email.com', 'Carrera 50 # 12-45, Cartagena, Bolívar'),
    ('Camila García', 'camila.garcia@email.com', 'Calle 103 # 45-67, Bucaramanga, Santander'),
    ('Felipe Sánchez', 'felipe.sanchez@email.com', 'Carrera 30 # 10-11, Pereira, Risaralda'),
    ('Isabel Torres', 'isabel.torres@email.com', 'Avenida 4 # 22-19, Cúcuta, Norte de Santander'),
    ('Santiago Gómez', 'santiago.gomez@email.com', 'Calle 9 # 15-10, Santa Marta, Magdalena'),
    ('Laura Ramírez', 'laura.ramirez@email.com', 'Carrera 22 # 34-22, Ibagué, Tolima');
select * from clientes;

insert into pedidos (fecha, total, idCliente)
values
	('2025-04-01', 5000000, 10);
    
select * from pedidos;

insert into detallespedido (cantidades, precioUnitario, idPedido, idProducto)
values
	(10, 250000, 1, 5),
    (3, 250000, 1, 5);

select * from detallespedido;
    
-- Eliminar registros
DELETE FROM detallespedido WHERE idPedido = 1;
DELETE FROM pedidos WHERE id between 1 and 7;
DELETE FROM pedidos WHERE id=9;

-- Reiniciar el contador de autoincremento para que el siguiente id sea 1
ALTER TABLE pedidos AUTO_INCREMENT = 1;
ALTER TABLE detallespedido AUTO_INCREMENT = 1;
    


    
    
    