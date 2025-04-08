create database IVACOL;
-- drop database IVACOL;
use IVACOL;

create table ciudad (
    id int primary key auto_increment comment 'identificador de la ciudad',
    nombre varchar(100) not null comment 'nombre de la ciudad',
    departamento varchar(100) not null comment 'departamento o estado'
) comment = 'datos de la ciudad del usuario';

create table roles (
    id int primary key auto_increment comment 'identificador del rol',
    nombreRol varchar(50) not null unique comment 'nombre del rol'
) comment = 'roles para usuarios';

create table Genero (
	id int primary key auto_increment comment 'identificador de genero',
    nombre varchar(50) not null comment'masculino o femenino'
)comment = 'genero con el que se identifica';

create table Tipoimpuestos (
    id int primary key auto_increment comment 'identificador del Tipo de impuesto',
    nombre varchar(50) not null unique comment 'nombre del impuesto (iva, retefuente, etc.)'
) comment = 'tipos de impuestos aplicados a las facturas';

create table usuarios (
    id int primary key auto_increment comment 'identificador del usuario',
    nombre varchar(100) not null comment 'nombre del usuario',
    tipoDocumento varchar(5) not null comment 'tipo de documento',
    noDocumento varchar(20) not null unique comment 'numero de documento',
    idGenero int not null comment'identificador de Genero',
    idCiudad int not null comment 'identificador de la ciudad',
    numero int not null comment 'numero de contacto',
    correo varchar(100) not null unique comment 'correo del usuario',
    contrasena varchar(255) not null comment 'contrasena encriptada',
    direccion varchar(100) not null comment 'direccion del usuario',
    idRol int not null comment 'identificador del rol',
    foreign key (idCiudad) references ciudad(id),
    foreign key (idRol) references roles(id),
    foreign key (idGenero) references Genero(id)
) comment = 'usuarios del sistema';

create table proveedores (
    id int primary key auto_increment comment 'identificador del proveedor',
    nombre varchar(100) not null comment 'nombre del proveedor',
    direccion varchar(200) not null comment 'direccion del proveedor',
    telefono varchar(20) not null comment 'telefono de contacto del proveedor',
    correo varchar(100) not null unique comment 'correo de contacto del proveedor'
) comment = 'datos de los proveedores de productos o servicios';

create table facturas (
    id int primary key auto_increment comment 'identificador de la factura',
    idUsuario int not null comment 'identificador del usuario que sube la factura',
    idProveedor int not null comment 'identificador del proveedor que emite la factura',
    numero int not null comment 'numero de factura',
    fecha date not null comment 'fecha de la factura',
    valTotal decimal(10,2) not null comment 'monto total de la factura',
    valIva decimal(10,2) not null comment 'monto del iva en la factura',
    foreign key (idUsuario) references usuarios(id),
    foreign key (idProveedor) references proveedores(id)
) comment = 'datos de las facturas';


create table facturasImpuestos (
    id int primary key auto_increment comment 'identificador de la relacion',
    idFactura int not null comment 'identificador de la factura',
    idImpuesto int not null comment 'identificador del impuesto',
    valor decimal(10,2) not null comment 'valor calculado del impuesto en la factura',
    porcentaje decimal(5,2) not null comment 'porcentaje aplicado',
    foreign key (idFactura) references facturas(id),
    foreign key (idImpuesto) references Tipoimpuestos(id)
) comment = 'relacion entre facturas e impuestos aplicados';

create table historialAcceso (
    id int primary key auto_increment comment 'identificador del acceso',
    idUsuario int not null comment 'usuario que ingreso al sistema',
    fechaHora datetime not null default current_timestamp comment 'fecha y hora del acceso',
    accion varchar(255) not null comment 'accion realizada (ingreso, subio factura, elimino factura, etc.)',
    foreign key (idUsuario) references usuarios(id)
) comment = 'registro de accesos y acciones de los usuarios';

create table imagenesFacturas (
    id int primary key auto_increment comment 'identificador de la imagen de la factura',
    idFactura int not null comment 'identificador de la factura asociada',
    imagen_url varchar(255) not null comment 'url o ubicacion de la imagen de la factura',
    descripcion varchar(255) comment 'descripcion adicional de la imagen',
    foreign key (idFactura) references facturas(id)
) comment = 'almacenamiento de las imagenes de las facturas';




