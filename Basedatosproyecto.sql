use master;
CREATE DATABASE CuboLAP;
GO

CREATE TABLE ROL (
    IDRol INT IDENTITY(1,1) PRIMARY KEY,
        NombreRol VARCHAR(50) NOT NULL UNIQUE
    );
    GO

    CREATE TABLE USUARIO (
        IDUsuario INT IDENTITY(1,1) PRIMARY KEY,
        NumeroIdentidad VARCHAR(15) NOT NULL UNIQUE,
        Nombre VARCHAR(50) NOT NULL,
        Apellido VARCHAR(50) NOT NULL,
        Contrasena VARCHAR(100) NOT NULL,
        IDRol INT NOT NULL,
        Activo BIT NOT NULL DEFAULT 1,
        CONSTRAINT FK_Usuario_Rol FOREIGN KEY (IDRol)
        REFERENCES ROL(IDRol) ON DELETE CASCADE
    );
    GO

    CREATE TABLE CONEXIONES (
        idconexion INT IDENTITY(1,1) PRIMARY KEY,
        nombreconexion VARCHAR(50) NOT NULL UNIQUE,
        gestor VARCHAR(20) NOT NULL CHECK (gestor IN ('SQL Server', 'MySQL')),
        host VARCHAR(100) NOT NULL,
        puerto INT NULL,
        usuario VARCHAR(50) NOT NULL,
        contrasenia VARCHAR(100) NOT NULL,
        basedatos VARCHAR(50) NOT NULL,
        CONSTRAINT CK_Puerto_Requerido CHECK (
            (Gestor = 'SQL Server' AND Puerto IS NOT NULL) OR 
            (Gestor = 'MySQL' AND Puerto IS NOT NULL)
        )
    );
    GO