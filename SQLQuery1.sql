USE master
GO

IF EXISTS (SELECT name FROM sys.databases WHERE name = 'cubolap')
DROP DATABASE cubolap
GO

CREATE DATABASE cubolap
GO

USE cubolap
GO

-- Tabla rol
CREATE TABLE rol(
    idruta INT IDENTITY(1,1) PRIMARY KEY,
    nombreruta VARCHAR(50) NOT NULL UNIQUE
)
GO

-- Tabla usuarios
CREATE TABLE usuarios(
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    contrasena VARCHAR(50) NOT NULL
)
GO

-- Insertar datos
SET IDENTITY_INSERT usuarios ON

INSERT INTO usuarios (id, nombre, contrasena)
VALUES (1, 'Rony', '12345')

SET IDENTITY_INSERT usuarios OFF
GO