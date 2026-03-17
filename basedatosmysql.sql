use master;
CREATE DATABASE CuboLAP;
GO

CREATE TABLE ROL (
    IDRol INT AUTO_INCREMENT PRIMARY KEY,
    NombreRol VARCHAR(50) NOT NULL UNIQUE
    );
    GO

CREATE TABLE USUARIO (
        IDUsuario INT AUTO_INCREMENT PRIMARY KEY,
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
        IDConexion INT AUTO_INCREMENT PRIMARY KEY,
        NombreConexion VARCHAR(50) NOT NULL UNIQUE,
        Gestor VARCHAR(20) NOT NULL CHECK (Gestor IN ('SQL Server', 'MySQL')),
        Host VARCHAR(100) NOT NULL,
        Puerto INT NULL,
        Usuario VARCHAR(50) NOT NULL,
        Contrasena VARCHAR(100) NOT NULL,
        BaseDatos VARCHAR(50) NOT NULL,
        CONSTRAINT CK_Puerto_Requerido CHECK (
            (Gestor = 'SQL Server' AND Puerto IS NOT NULL) OR 
            (Gestor = 'MySQL' AND Puerto IS NOT NULL)
        )
    );
    GO
