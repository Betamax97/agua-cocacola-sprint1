CREATE DATABASE IF NOT EXISTS agua_cocacola;
USE agua_cocacola;

CREATE TABLE IF NOT EXISTS procesos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(60) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS consumos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  proceso_id INT NOT NULL,
  fecha DATE NOT NULL,
  consumo_m3 DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (proceso_id) REFERENCES procesos(id),
  -- HU-09: un proceso no puede tener dos registros con la misma fecha
  UNIQUE KEY uq_consumo_proceso_fecha (proceso_id, fecha)
);

CREATE TABLE IF NOT EXISTS referencias (
  id INT AUTO_INCREMENT PRIMARY KEY,
  proceso_id INT NOT NULL,
  mes CHAR(7) NOT NULL,
  valor_m3 DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (proceso_id) REFERENCES procesos(id),
  UNIQUE KEY uq_referencia_proceso_mes (proceso_id, mes)
);

CREATE TABLE IF NOT EXISTS alertas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  proceso_id INT NOT NULL,
  periodo CHAR(7) NOT NULL,
  desviacion_pct DECIMAL(6,2),
  nivel ENUM('informativa','preventiva','critica') NOT NULL,
  FOREIGN KEY (proceso_id) REFERENCES procesos(id)
);

INSERT IGNORE INTO procesos (nombre) VALUES
('lavado_envases'),
('limpieza_maquinaria'),
('refrigeracion'),
('mantenimiento'),
('tratamiento_residuales');
