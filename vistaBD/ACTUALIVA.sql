
-- DDL
create database ivacol;
-- drop database ivacol;
use ivacol;

create table departamento (
    id int primary key auto_increment comment 'identificador del departamento',
    nombre varchar(100) not null unique comment 'nombre del departamento o estado'
) comment = 'datos de los departamentos';

create table ciudad (
    id int primary key auto_increment comment 'identificador de la ciudad',
    nombre varchar(100) not null comment 'nombre de la ciudad',
    iddepartamento int not null comment 'identificador del departamento',
    foreign key (iddepartamento) references departamento(id)
) comment = 'datos de la ciudad del usuario';

create table roles (
    id int primary key auto_increment comment 'identificador del rol',
    nombrerol varchar(50) not null unique comment 'nombre del rol'
) comment = 'roles para usuarios';

create table genero (
    id int primary key auto_increment comment 'identificador de genero',
    nombre varchar(50) not null unique comment 'masculino o femenino'
) comment = 'genero con el que se identifica';

create table tipodocumento (
    id int primary key auto_increment comment 'identificador del tipo de documento',
    nombre varchar(10) not null unique comment 'tipo de documento (cc, ti, ce, etc.)'
) comment = 'tipos de documento del usuario';

create table usuarios (
    id int primary key auto_increment comment 'identificador del usuario',
    nombres varchar(100) not null comment 'nombre del usuario',
    apellidos varchar(100) not null comment 'apellido del usuario',
    idtipodocumento int not null comment 'identificador del tipo de documento',
    nodocumento varchar(20) not null unique comment 'numero de documento',
    idgenero int not null comment 'identificador de genero',
    idciudad int not null comment 'identificador de la ciudad',
    numero varchar(20) not null comment 'numero de contacto',
    correo varchar(100) not null unique comment 'correo del usuario',
    contrasena varchar(255) not null comment 'contrasena encriptada',
    direccion varchar(100) not null comment 'direccion del usuario',
    idrol int not null comment 'identificador del rol',
    foreign key (idtipodocumento) references tipodocumento(id),
    foreign key (idgenero) references genero(id),
    foreign key (idciudad) references ciudad(id),
    foreign key (idrol) references roles(id)
) comment = 'usuarios del sistema';

create table proveedores (
    id int primary key auto_increment comment 'identificador del proveedor',
    nit varchar(20) comment 'nit de la empresa',
    nombre varchar(100) not null comment 'nombre del proveedor',
    direccion varchar(200) not null comment 'direccion del proveedor',
    telefono varchar(20) not null comment 'telefono de contacto del proveedor',
    correo varchar(100) not null unique comment 'correo de contacto del proveedor'
) comment = 'datos de los proveedores de productos o servicios';

create table tiposimpuesto (
    id int primary key auto_increment comment 'identificador del tipo de impuesto',
    nombre varchar(50) not null unique comment 'nombre del impuesto (iva, retefuente, etc.)'
) comment = 'tipos de impuestos aplicados a las facturas';

create table facturas (
    id int primary key auto_increment comment 'identificador de la factura',
    idusuario int not null comment 'identificador del usuario que sube la factura',
    idproveedor int not null comment 'identificador del proveedor que emite la factura',
    numero int not null comment 'numero de factura',
    fecha date not null comment 'fecha de la factura',
    valtotal decimal(10,2) not null comment 'monto total de la factura',
    valiva decimal(10,2) not null comment 'monto del iva en la factura',
    foreign key (idusuario) references usuarios(id),
    foreign key (idproveedor) references proveedores(id)
) comment = 'datos de las facturas';

create table facturasimpuestos (
    id int primary key auto_increment comment 'identificador de la relacion',
    idfactura int not null comment 'identificador de la factura',
    idimpuesto int not null comment 'identificador del impuesto',
    valor decimal(10,2) not null comment 'valor calculado del impuesto en la factura',
    porcentaje decimal(5,2) not null comment 'porcentaje aplicado',
    foreign key (idfactura) references facturas(id),
    foreign key (idimpuesto) references tiposimpuesto(id)
) comment = 'relacion entre facturas e impuestos aplicados';

create table accionessistema (
    id int primary key auto_increment comment 'identificador de la accion',
    nombre varchar(100) not null unique comment 'nombre de la accion realizada'
) comment = 'acciones que puede realizar un usuario en el sistema';

create table historialacceso (
    id int primary key auto_increment comment 'identificador del acceso',
    idusuario int not null comment 'usuario que ingreso al sistema',
    fechahora datetime not null default current_timestamp comment 'fecha y hora del acceso',
    idaccion int not null comment 'accion realizada (ingreso, subio factura, elimino factura, etc.)',
    foreign key (idusuario) references usuarios(id),
    foreign key (idaccion) references accionessistema(id)
) comment = 'registro de accesos y acciones de los usuarios';

create table imagenesfacturas (
    id int primary key auto_increment comment 'identificador de la imagen de la factura',
    idfactura int not null comment 'identificador de la factura asociada',
    imagen_url varchar(255) not null comment 'url o ubicacion de la imagen de la factura',
    descripcion varchar(255) comment 'descripcion adicional de la imagen',
    foreign key (idfactura) references facturas(id)
) comment = 'almacenamiento de las imagenes de las facturas';





-- DML

USE ivacol;

-- Tablas sin dependencias externas 

INSERT INTO departamento (nombre) VALUES
('Cundinamarca'),
('Antioquia'),
('Valle del Cauca');

INSERT INTO roles (nombrerol) VALUES
('Administrador'),
('Usuario Standard'),
('Contador');

INSERT INTO genero (nombre) VALUES
('Masculino'),
('Femenino'),
('No especifica');

INSERT INTO tipodocumento (nombre) VALUES
('CC'), -- Cedula Ciudadania
('CE'), -- Cedula Extranjeria
('NIT'); -- Numero Identificacion Tributaria

INSERT INTO accionessistema (nombre) VALUES
('Inicio Sesion'),
('Subir Factura'),
('Eliminar Factura'),
('Consultar Reporte'),
('Cerrar Sesion');

INSERT INTO tiposimpuesto (nombre) VALUES
('IVA 19%'),
('IVA 5%'),
('Retefuente Servicios 6%'),
('Retefuente Compras 2.5%'),
('ICA Bogotá 9.66/1000');

-- Tablas con dependencias

INSERT INTO ciudad (nombre, iddepartamento) VALUES
('Bogotá D.C.', 1), -- Asume Cundinamarca ID = 1
('Medellín', 2),    -- Asume Antioquia ID = 2
('Cali', 3),        -- Asume Valle del Cauca ID = 3
('Soacha', 1),      -- Asume Cundinamarca ID = 1
('Envigado', 2);    -- Asume Antioquia ID = 2

INSERT INTO proveedores (nit, nombre, direccion, telefono, correo) VALUES
('800123456-1', 'Proveedor Alpha SAS', 'Calle Falsa 123', '3101112233', 'contacto@alpha.com'),
('900987654-2', 'Suministros Beta Ltda', 'Avenida Siempre Viva 45', '3114445566', 'ventas@beta.net'),
('830001122-3', 'Comercial Gamma y Cia', 'Carrera 7 # 8-90', '3127778899', 'info@gamma.co'),
('901222333-4', 'Insumos Delta EU', 'Transversal 15 # 100-01', '3130001122', 'pedidos@delta.org'),
('860555666-5', 'Servicios Epsilon SAS', 'Diagonal 50 Sur # 20-30', '3143334455', 'servicio@epsilon.com.co');

INSERT INTO usuarios (nombres, apellidos, idtipodocumento, nodocumento, idgenero, idciudad, numero, correo, contrasena, direccion, idrol) VALUES
('Juan Carlos', 'Perez Gomez', 1, '10101010', 1, 1, '3209876543', 'jc.perez@email.com', 'hash_contrasena_1', 'Calle 10 # 20-30', 1), -- CC, Masc, Bogota, Admin (IDs: 1, 1, 1, 1)
('Maria Lucia', 'Rodriguez Silva', 1, '20202020', 2, 2, '3218765432', 'ml.rodriguez@email.com', 'hash_contrasena_2', 'Carrera 50 # 60-70', 2), -- CC, Fem, Medellin, User Std (IDs: 1, 2, 2, 2)
('Pedro Antonio', 'Martinez Diaz', 2, '30303030', 1, 3, '3107654321', 'pa.martinez@email.com', 'hash_contrasena_3', 'Avenida 3N # 40-50', 2), -- CE, Masc, Cali, User Std (IDs: 2, 1, 3, 2)
('Ana Sofia', 'Gonzalez Lopez', 1, '40404040', 2, 4, '3116543210', 'as.gonzalez@email.com', 'hash_contrasena_4', 'Diagonal 100 # 1-2', 3),   -- CC, Fem, Soacha, Contador (IDs: 1, 2, 4, 3)
('Luis Fernando', 'Hernandez Ramirez', 3, '50505050-5', 1, 5, '3125432109', 'lf.hernandez@email.com', 'hash_contrasena_5', 'Calle 30 Sur # 40-50', 2); -- NIT, Masc, Envigado, User Std (IDs: 3, 1, 5, 2)

INSERT INTO facturas (idusuario, idproveedor, numero, fecha, valtotal, valiva) VALUES
(1, 1, 1001, '2024-01-15', 119000.00, 19000.00), -- Usuario 1, Proveedor 1
(2, 2, 2050, '2024-02-20', 250000.00, 47500.00), -- Usuario 2, Proveedor 2
(3, 3, 3100, '2024-03-10', 85000.50, 16150.10),  -- Usuario 3, Proveedor 3
(4, 4, 4005, '2024-04-01', 50000.00, 2500.00),   -- Usuario 4, Proveedor 4 (IVA 5%)
(5, 5, 5220, '2024-05-05', 1000000.00, 190000.00); -- Usuario 5, Proveedor 5

-- 3. Tablas de Relación y Auditoría

INSERT INTO facturasimpuestos (idfactura, idimpuesto, valor, porcentaje) VALUES
(1, 1, 19000.00, 19.00),  -- Factura 1, IVA 19% (ID Impuesto: 1)
(2, 1, 47500.00, 19.00),  -- Factura 2, IVA 19% (ID Impuesto: 1)
(2, 4, 6250.00, 2.50),    -- Factura 2, Retefuente Compras 2.5% (ID Impuesto: 4)
(3, 1, 16150.10, 19.00),  -- Factura 3, IVA 19% (ID Impuesto: 1)
(4, 2, 2500.00, 5.00),    -- Factura 4, IVA 5% (ID Impuesto: 2)
(5, 1, 190000.00, 19.00), -- Factura 5, IVA 19% (ID Impuesto: 1)
(5, 3, 60000.00, 6.00);   -- Factura 5, Retefuente Servicios 6% (ID Impuesto: 3)

INSERT INTO historialacceso (idusuario, idaccion, fechahora) VALUES
(1, 1, '2024-05-10 08:00:00'), -- Usuario 1, Inicio Sesion (IDs: 1, 1)
(1, 2, '2024-05-10 08:05:00'), -- Usuario 1, Subir Factura (IDs: 1, 2) -> Factura 1
(2, 1, '2024-05-10 09:15:00'), -- Usuario 2, Inicio Sesion (IDs: 2, 1)
(2, 2, '2024-05-10 09:20:00'), -- Usuario 2, Subir Factura (IDs: 2, 2) -> Factura 2
(3, 1, '2024-05-11 10:00:00'), -- Usuario 3, Inicio Sesion (IDs: 3, 1)
(3, 2, '2024-05-11 10:05:00'), -- Usuario 3, Subir Factura (IDs: 3, 2) -> Factura 3
(4, 1, '2024-05-12 11:30:00'), -- Usuario 4, Inicio Sesion (IDs: 4, 1)
(4, 2, '2024-05-12 11:35:00'), -- Usuario 4, Subir Factura (IDs: 4, 2) -> Factura 4
(5, 1, '2024-05-13 14:00:00'), -- Usuario 5, Inicio Sesion (IDs: 5, 1)
(5, 2, '2024-05-13 14:07:00'); -- Usuario 5, Subir Factura (IDs: 5, 2) -> Factura 5

INSERT INTO imagenesfacturas (idfactura, imagen_url, descripcion) VALUES
(1, '/uploads/facturas/factura_1001_prov1.jpg', 'Foto Factura 1001'), -- Factura 1
(2, '/uploads/facturas/scan_2050_beta.pdf', 'PDF Factura 2050'),    -- Factura 2
(3, '/uploads/facturas/img_fact_3100_gamma.png', 'Imagen Factura 3100'), -- Factura 3
(4, '/uploads/facturas/delta_factura_4005.jpeg', 'Factura 200'),               -- Factura 4
(5, '/uploads/facturas/epsilon_5220.tiff', 'Factura Servicios Mayo'); -- Factura 5




--  Solicitar datos

-- seleccionar todos los datos de la tabla usuarios
select * from usuarios;

-- seleccionar solo nombres, apellidos y correo de todos los usuarios
select nombres, apellidos, correo from usuarios;

-- seleccionar los datos del usuario con correo 'jc.perez@email.com'
select * from usuarios where correo = 'jc.perez@email.com';

-- seleccionar usuarios que pertenezcan a la ciudad con id = 1 (bogotá)
select nombres, apellidos, correo from usuarios where idciudad = 1;

-- seleccionar todas las facturas con un valor total mayor a 90000
select * from facturas where valtotal > 90000;

-- seleccionar facturas emitidas en una fecha específica
select * from facturas where fecha = '2024-02-20';

-- seleccionar facturas emitidas dentro de un rango de fechas
select * from facturas where fecha between '2024-01-01' and '2024-03-31';

-- seleccionar todos los proveedores cuyo nombre contenga 'beta'
select * from proveedores where nombre like '%beta%';

-- obtener nombres de usuario y el nombre de su rol (unión de tablas)
select u.nombres, u.apellidos, r.nombrerol
from usuarios u
join roles r on u.idrol = r.id;

-- obtener nombres de usuario, su ciudad y el departamento al que pertenece (unión de tres tablas)
select u.nombres, u.apellidos, c.nombre as nombre_ciudad, d.nombre as nombre_departamento
from usuarios u
join ciudad c on u.idciudad = c.id
join departamento d on c.iddepartamento = d.id;

-- obtener detalles de la factura (número, fecha, total) junto con el nombre del usuario que la subió y el nombre del proveedor
select f.numero, f.fecha, f.valtotal, u.nombres as nombre_usuario, p.nombre as nombre_proveedor
from facturas f
join usuarios u on f.idusuario = u.id
join proveedores p on f.idproveedor = p.id;

-- obtener los detalles de una factura específica (id=2) y los impuestos aplicados (nombre del impuesto, valor, porcentaje)
select f.numero, f.fecha, f.valtotal, ti.nombre as nombre_impuesto, fi.valor as valor_impuesto, fi.porcentaje
from facturas f
join facturasimpuestos fi on f.id = fi.idfactura
join tiposimpuesto ti on fi.idimpuesto = ti.id
where f.id = 2;

-- obtener el historial de acceso (nombre usuario, nombre acción, fecha/hora), ordenado por fecha descendente
select u.nombres as nombre_usuario, ac.nombre as nombre_accion, ha.fechahora
from historialacceso ha
join usuarios u on ha.idusuario = u.id
join accionessistema ac on ha.idaccion = ac.id
order by ha.fechahora desc;

-- contar cuántos usuarios hay por cada ciudad
select c.nombre as nombre_ciudad, count(u.id) as numero_de_usuarios
from ciudad c
join usuarios u on c.id = u.idciudad
group by c.nombre
order by numero_de_usuarios desc;

-- calcular la suma total facturada por cada proveedor
select p.nombre as nombre_proveedor, sum(f.valtotal) as total_facturado
from proveedores p
join facturas f on p.id = f.idproveedor
group by p.nombre
order by total_facturado desc;

-- obtener las 5 facturas más recientes
select * from facturas order by fecha desc limit 5;

-- obtener las facturas junto con la url de sus imágenes (usando left join por si alguna factura no tiene imagen)
select f.numero, f.fecha, imf.imagen_url, imf.descripcion
from facturas f
left join imagenesfacturas imf on f.id = imf.idfactura;

-- obtener los usuarios que son 'administrador'
select u.nombres, u.apellidos, u.correo
from usuarios u
join roles r on u.idrol = r.id
where r.nombrerol = 'administrador';
