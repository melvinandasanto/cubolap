use master;
CREATE DATABASE cubolap;
GO

CREATE TABLE rol (
    idrol INT IDENTITY(1,1) PRIMARY KEY,
    nombrerol VARCHAR(50) NOT NULL UNIQUE
    );
    GO

    CREATE TABLE usuario (
        idusuario INT IDENTITY(1,1) PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL,
        apellido VARCHAR(50) NOT NULL,
        contrasenia VARCHAR(50) NOT NULL,
        idrol INT NOT NULL,
        activo BIT NOT NULL DEFAULT 1,
        CONSTRAINT FK_Usuario_Rol FOREIGN KEY (idrol)
        REFERENCES ROL(idrol) ON DELETE CASCADE
    );
    GO

    CREATE TABLE conexiones (
        idconexion INT IDENTITY(1,1) PRIMARY KEY,
        nombreconexion VARCHAR(50) NOT NULL UNIQUE,
        gestor VARCHAR(20) NOT NULL CHECK (gestor IN ('SQL Server', 'MySQL')),
        host VARCHAR(100) NOT NULL,
        puerto INT NULL,
        usuario VARCHAR(50) NULL,
        contrasenia VARCHAR(100) NOT NULL,
        basedatos VARCHAR(50) NOT NULL,
        CONSTRAINT CK_Puerto_Requerido CHECK (
            (gestor = 'SQL Server' AND puerto IS NULL AND host IS NULL) OR 
            (gestor = 'MySQL' AND puerto IS NOT NULL AND host IS NOT NULL)
        )
    );
    GO