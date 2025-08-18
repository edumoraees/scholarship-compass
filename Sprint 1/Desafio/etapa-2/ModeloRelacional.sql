-- MODELO RELACIONAL - CONCESSIONÁRIA


-- Tabela de Cliente
CREATE TABLE IF NOT EXISTS cliente (
  idCliente     INTEGER PRIMARY KEY,
  nome          TEXT NOT NULL,
  cidade        TEXT,
  estado        TEXT,
  pais          TEXT
);

-- Tabela de Vendedor
CREATE TABLE IF NOT EXISTS vendedor (
  idVendedor    INTEGER PRIMARY KEY,
  nome          TEXT NOT NULL,
  sexo          INTEGER CHECK (sexo IN (0,1)) , -- 0=feminino, 1=masculino
  estado        TEXT
);

-- Tabela de Combustível
CREATE TABLE IF NOT EXISTS combustivel (
  idCombustivel INTEGER PRIMARY KEY,
  tipo          TEXT NOT NULL
);

-- Tabela de Carro
CREATE TABLE IF NOT EXISTS carro (
  idCarro       INTEGER PRIMARY KEY,
  chassi        TEXT UNIQUE,
  marca         TEXT,
  modelo        TEXT,
  ano           INTEGER,
  idCombustivel INTEGER,
  kmAtual       INTEGER,
  FOREIGN KEY (idCombustivel) REFERENCES combustivel(idCombustivel)
);

-- Tabela de Locação
CREATE TABLE IF NOT EXISTS locacao (
  idLocacao     INTEGER PRIMARY KEY,
  idCliente     INTEGER NOT NULL,
  idCarro       INTEGER NOT NULL,
  idVendedor    INTEGER NOT NULL,
  dataLocacao   TEXT,  -- ISO: 'YYYY-MM-DD'
  horaLocacao   TEXT,  -- 'HH:MM' 
  dataEntrega   TEXT,
  horaEntrega   TEXT,
  qtdDiaria     INTEGER,
  vlrDiaria     NUMERIC(18,2),
  FOREIGN KEY (idCliente)  REFERENCES cliente(idCliente),
  FOREIGN KEY (idCarro)    REFERENCES carro(idCarro),
  FOREIGN KEY (idVendedor) REFERENCES vendedor(idVendedor)
);
