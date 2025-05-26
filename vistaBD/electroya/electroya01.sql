-- Sentencias DDL (Data Definition Language) --> Define estructuras

-- Crear Base de Datos
create database electroya;

-- Ingresar BD
use electroya;

-- Crear tabla  de Productos
create table Productos(
	id int primary key auto_increment,
	nombre varchar(100) not null,
	precio int not null,
	stock int not null,
	categoria varchar(50)
);

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


-- --------------------------------------------------------------------- --
-- Sentencias DML (Data Manipulation Language) --> Trabaja con los datos --
-- --------------------------------------------------------------------- --

-- INSERT - Insertar(Ingresar) una o más filas(registros) de datos a una tabla

-- Ingresar registros a la tabla Productos
-- -------------------------------------------------------------
INSERT INTO Productos (nombre, precio, stock, categoria) 
VALUES
	('Celular Samsung Galaxy A34', 1200000, 50, 'Celulares'),
	('Televisor LG 55" 4K', 2500000, 20, 'Televisores'),
	('Portátil ASUS VivoBook', 2800000, 15, 'Computadores'),
	('Mouse Logitech inalámbrico', 70000, 100, 'Accesorios'),
	('Teclado Redragon Mecánico', 150000, 60, 'Accesorios'),
	('Tablet Lenovo 10"', 950000, 25, 'Tablets'),
	('Auriculares Sony WH-CH510', 180000, 40, 'Audio'),
	('Impresora HP DeskJet 2700', 350000, 10, 'Impresoras'),
	('Monitor Samsung 24"', 620000, 18, 'Monitores'),
	('Disco Duro Externo 1TB Toshiba', 250000, 30, 'Almacenamiento'),
	('Cámara de seguridad WiFi Ezviz', 220000, 35, 'Seguridad'),
	('Router TP-Link AC1200', 170000, 22, 'Redes'),
	('Parlante Bluetooth JBL Go 3', 200000, 45, 'Audio'),
	('Smartwatch Xiaomi Redmi Watch 3', 380000, 50, 'Wearables'),
	('Memoria USB 32GB Kingston', 35000, 120, 'Almacenamiento'),
	('Cargador portátil 10000mAh Xiaomi', 85000, 75, 'Accesorios'),
	('Base para portátil Cooler Master', 95000, 40, 'Accesorios'),
	('Mousepad gamer grande', 40000, 80, 'Accesorios'),
	('Cámara Logitech C920 HD', 300000, 17, 'Webcams'),
	('Soporte TV fijo hasta 65"', 70000, 25, 'Accesorios');

-- Ingresar registros a la tabla Clientes
-- -------------------------------------------------------------
INSERT INTO Clientes (nombre, email, direccion) 
VALUES
	('Carlos Pérez', 'carlos.perez@gmail.com', 'Cra 15 #45-23, Bogotá'),
	('Laura Ramírez', 'laura.ramirez@hotmail.com', 'Cll 50 #12-34, Medellín'),
	('Andrés Gómez', 'andres.gomez@yahoo.com', 'Av. 1 de Mayo #6-40, Cali'),
	('María Fernanda Torres', 'mariaf.torres@gmail.com', 'Cll 75 #20-14, Barranquilla'),
	('Daniela Castro', 'daniela.castro@gmail.com', 'Cra 30 #60-19, Cartagena'),
	('Juan Sebastián Rojas', 'juan.rojas@gmail.com', 'Cll 100 #55-10, Bucaramanga'),
	('Natalia López', 'natalia.lopez@gmail.com', 'Cll 22 #15-60, Pereira'),
	('Santiago Martínez', 'santi.mtz@gmail.com', 'Cra 18 #34-23, Manizales'),
	('Camila Rodríguez', 'camila.rodri@gmail.com', 'Cll 10 #5-15, Armenia'),
	('Luis Miguel Herrera', 'luis.herrera@gmail.com', 'Av. Circunvalar #80-30, Neiva'),
	('Paola Jiménez', 'paola.jimenez@gmail.com', 'Cll 90 #30-45, Ibagué'),
	('Felipe Suárez', 'felipe.suarez@gmail.com', 'Cra 45 #90-20, Santa Marta'),
	('Carolina Vargas', 'caro.vargas@gmail.com', 'Cll 70 #20-18, Cúcuta'),
	('Julián Castaño', 'julian.cast@gmail.com', 'Cra 40 #55-32, Pasto'),
	('Isabela Méndez', 'isabela.mendez@gmail.com', 'Cll 33 #10-90, Villavicencio'),
	('Ricardo León', 'ricardo.leon@gmail.com', 'Cra 27 #72-14, Montería'),
	('Luisa Fernanda Mejía', 'luisa.mejia@gmail.com', 'Cll 45 #30-11, Popayán'),
	('Mateo Niño', 'mateo.nino@gmail.com', 'Cll 88 #22-17, Valledupar'),
	('Diana Castellanos', 'diana.cast@gmail.com', 'Cra 20 #12-50, Tunja'),
	('Fernando Acosta', 'fernando.acosta@gmail.com', 'Cll 15 #5-40, Sincelejo');

-- Ingresar registros a la tabla Pedidos
-- -------------------------------------------------------------
INSERT INTO Pedidos (fecha, total, idCliente) 
VALUES
	('2025-01-05', 2850000, 1),
	('2025-01-10', 130000, 2),
	('2025-01-12', 250000, 3),
	('2025-01-15', 1200000, 4),
	('2025-01-18', 470000, 5),
	('2025-01-20', 750000, 6),
	('2025-01-22', 2000000, 7),
	('2025-01-25', 85000, 8),
	('2025-01-27', 70000, 9),
	('2025-01-29', 620000, 10),
	('2025-02-01', 380000, 11),
	('2025-02-03', 90000, 12),
	('2025-02-05', 300000, 13),
	('2025-02-07', 2500000, 14),
	('2025-02-09', 950000, 15),
	('2025-02-11', 170000, 16),
	('2025-02-13', 40000, 17),
	('2025-02-15', 200000, 18),
	('2025-02-17', 85000, 19),
	('2025-02-19', 70000, 20),

	('2025-03-13', 150000, 1),  
	('2025-03-14', 350000, 1), 
	('2025-03-15', 180000, 1),  

	('2025-03-16', 950000, 2), 
	('2025-03-17', 400000, 2),  

	('2025-03-18', 620000, 4),
	('2025-03-19', 70000, 4),
	('2025-03-20', 1000000, 4), 

	('2025-03-21', 250000, 6),  
	('2025-03-22', 300000, 6),  

	('2025-03-23', 40000, 10),  
	('2025-03-24', 85000, 10),  

	('2025-03-25', 300000, 14), 
	('2025-03-26', 2800000, 14),

	('2025-03-27', 70000, 17), 
	('2025-03-28', 180000, 17), 
	('2025-03-29', 950000, 17), 

	('2025-03-30', 120000, 19), 
	('2025-03-31', 600000, 19), 
	('2025-04-01', 110000, 19);


-- Ingresar registros a la tabla detallesPedidos
-- -------------------------------------------------------------
INSERT INTO detallesPedido (cantidad, precioUnitario, idPedido, idProducto) 
VALUES
(1, 1200000, 1, 3),
(2, 40000, 1, 18),
(1, 150000, 1, 5),
(1, 90000, 1, 17),
(1, 130000, 2, 15),
(1, 20000, 2, 20),
(1, 160000, 2, 12),
(1, 250000, 3, 10),
(2, 60000, 4, 12),
(1, 200000, 4, 13),
(1, 300000, 4, 19),
(1, 350000, 5, 8),
(1, 90000, 5, 5),
(1, 125000, 5, 1),
(1, 750000, 6, 11),
(1, 300000, 6, 19),
(1, 1300000, 7, 2),
(1, 700000, 7, 6),
(1, 400000, 7, 4),
(1, 85000, 8, 16),
(2, 70000, 9, 4),
(1, 620000, 10, 9),
(1, 100000, 10, 13),
(1, 380000, 11, 19),
(1, 150000, 11, 5),
(1, 90000, 12, 5),
(1, 130000, 12, 15),
(1, 150000, 13, 8),
(1, 110000, 13, 14),
(1, 180000, 13, 7),
(1, 2500000, 14, 2),
(1, 90000, 14, 20),
(1, 700000, 15, 6),
(1, 250000, 15, 10),
(1, 400000, 15, 8),
(1, 170000, 16, 7),
(1, 90000, 16, 17),
(1, 40000, 17, 18),
(1, 220000, 17, 6),
(2, 100000, 18, 13),
(1, 160000, 18, 14),
(1, 85000, 19, 16),
(1, 120000, 19, 1),
(1, 100000, 19, 13),
(1, 70000, 20, 4),
(1, 40000, 20, 18),
(1, 300000, 20, 12),
(1, 150000, 21, 5),
(1, 120000, 21, 1),
(1, 350000, 22, 8),
(1, 200000, 22, 2),
(1, 180000, 23, 7),
(1, 70000, 23, 4),
(1, 950000, 24, 6),
(1, 110000, 24, 15),
(2, 200000, 25, 13),
(1, 70000, 25, 3),
(1, 620000, 26, 9),
(1, 70000, 26, 20),
(1, 70000, 27, 4),
(1, 1000000, 28, 3),
(1, 120000, 28, 11),
(1, 250000, 29, 10),
(1, 150000, 30, 5),
(1, 200000, 30, 11),
(1, 40000, 31, 18),
(1, 85000, 32, 16),
(1, 300000, 33, 19),
(1, 2800000, 34, 2),
(1, 70000, 35, 4),
(1, 180000, 36, 7),
(1, 950000, 37, 6),
(1, 120000, 38, 1),
(1, 600000, 39, 9),
(1, 110000, 40, 14),
(1, 150000, 40, 5);

select * from pedidos;
