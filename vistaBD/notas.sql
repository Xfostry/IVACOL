-- DDL (Data Definition Language) ESTRUCTURA

-- drop database disquera;

create database disquera;
use disquera;

create table Productos(
id int primary key auto_increment,
nombre varchar(100) not null,
precio int not null,
stock int not null,
categoria varchar(50) not null
);


create table Clientes(
id int primary key auto_increment,
nombre varchar(100) not null,
email varchar(100) not null,
direccion varchar(200) not null
);

create table Pedidos(
id int primary key auto_increment,
idPedido int not null,
fecha date not null,
total int not null,
foreign key (idPedido) references Clientes(id)
);

create table detallePedido(
id int primary key auto_increment,
idPedido int not null,
idProducto int not null,
cantidad int not null,
precioUnitario int not null,
foreign key (idPedido) references Pedidos(id),
foreign key (idProducto) references Productos(id)
);
drop table detallePedido;

-- CAMBIAR ESTRUCTURA O ADICIONAR CAMPOS
alter table detallePedido
	add column cantidadP int not null;

-- CAMBIAR ESTRUCTURA O ADICIONAR CAMPOS EN UN LUGAR ESPECIFICO
alter table detallePedido
	add column cantidadPr int not null after idProducto;
    
-- CAMBIAR ESTRUCTURA O ADICIONAR CAMPOS LLAVE FORANEA
alter table detallePedido
	add foreign key (sapo) references Productos(id);
    
    
-- PROPIA BD
-- CREAR BASE DE DATOS
create database TODOIVA;
use TODOIVA;

-- BORRAR BD
-- drop database todoiva;

-- CREAR TABLA
create table CLIENTES(
		id int primary key auto_increment,
		nombre varchar(100) not null,
		numero int(10) not null,
        correo varchar(100) not null,
        direccion varchar(100) not null
);
-- TABLA CON LLAVE FORANEA
create table FACTURAS(
		id int primary key auto_increment,
        idCliente int not null,
		foreign key (idCliente) references CLIENTES(id),
		idFactura int not null,
        fecha date not null,
        valorTotal decimal(10,2) not null,
        valorIva decimal(10,2) not null
);
use CLIENTES;

-- BORRAR TABLA
-- drop table CLIENTES;


-- Mostrar BD
show databases;

-- Mostrar tablas de una BD
show tables;

-- Mostrar comunas de una tabla
show columns from CLIENTES;

-- AGREGAR COMENTARIOS EN LA TABLA
-- mal hecha  aqui -- comment on table CLIENTES is 'la tabla almacena informacion de usuarios';
use TODOIVA;
use CLIENTES;
alter table CLIENTES comment = "la tabla almacena la informacion de los usuarios";
-- otro metodo
create table FACTURAS5555(
		id int primary key auto_increment,
        idCliente int not null comment 'llama al cliente',
		foreign key (idCliente) references CLIENTES(id),
		idFactura int not null,
        fecha date not null,
        valoresTotales decimal(10,2) not null,
        valorIva decimal(10,2) not null
) comment = "tabla de facturas";

-- comentario en la columna de la tabla
alter table FACTURAS5555 
	modify column fecha date not null comment 'mamawebo';
    
-- Renombrar tabla
rename table FACTURAS5555 to FACTURITAS;

-- Renombrar columna
alter table FACTURITAS
	change column valorTotal Total decimal(10,2) not null;
-- se vuelven a especificar los valores

-- Modificar una columna
alter table FACTURITAS
	modify column id int;

-- Quitar una columna de una tabla
alter table FACTURITAS
	drop column valorIva;
    
-- Para quitar la PK
alter table FACTURITAS
    drop primary key;

-- Duplicar una tabla
create table hola like FACTURITAS;


    


