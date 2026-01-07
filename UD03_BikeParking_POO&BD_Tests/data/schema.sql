PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS registros;
DROP TABLE IF EXISTS bicis;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
  dni   TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  email  TEXT NOT NULL UNIQUE
);

CREATE TABLE bicis (
  serie_cuadro TEXT PRIMARY KEY,
  dni_usuario  TEXT NOT NULL,
  marca        TEXT NOT NULL,
  modelo       TEXT NOT NULL,
  FOREIGN KEY (dni_usuario) REFERENCES usuarios(dni)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE TABLE registros (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp    TEXT NOT NULL,
  accion       TEXT NOT NULL CHECK (accion IN ('IN','OUT')),
  serie_cuadro TEXT NOT NULL,
  dni_usuario  TEXT NOT NULL,
  FOREIGN KEY (serie_cuadro) REFERENCES bicis(serie_cuadro)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  FOREIGN KEY (dni_usuario) REFERENCES usuarios(dni)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE INDEX idx_registros_serie_timestamp
  ON registros(serie_cuadro, timestamp);

CREATE INDEX idx_bicis_dni_usuario
  ON bicis(dni_usuario);
