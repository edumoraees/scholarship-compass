-- ============================
-- INSERÇÃO DE DADOS - MODELO RELACIONAL
-- Fonte: tabela bruta tb_locacao_raw
-- ============================

-- Inserção dos Clientes
INSERT OR IGNORE INTO cliente (idCliente, nome, cidade, estado, pais)
SELECT DISTINCT
  idCliente,
  nomeCliente,
  cidadeCliente,
  estadoCliente,
  paisCliente
FROM tb_locacao
WHERE idCliente IS NOT NULL;

-- Inserção dos Vendedores
INSERT OR IGNORE INTO vendedor (idVendedor, nome, sexo, estado)
SELECT DISTINCT
  idVendedor,
  nomeVendedor,
  sexoVendedor,
  estadoVendedor
FROM tb_locacao
WHERE idVendedor IS NOT NULL;

-- Inserção dos Combustíveis
INSERT OR IGNORE INTO combustivel (idCombustivel, tipo)
SELECT DISTINCT
  idcombustivel,
  tipoCombustivel
FROM tb_locacao
WHERE idcombustivel IS NOT NULL;

-- Inserção dos Carros
INSERT OR IGNORE INTO carro (idCarro, chassi, marca, modelo, ano, idCombustivel, kmAtual)
SELECT DISTINCT
  t.idCarro,
  t.chassiCarro,
  t.marcaCarro,
  t.modeloCarro,
  t.anoCarro,
  t.idcombustivel,
  k.kmAtual
FROM tb_locacao t
LEFT JOIN km_max k ON k.idCarro = t.idCarro
WHERE t.idCarro IS NOT NULL;

-- Inserção das Locações
INSERT OR IGNORE INTO locacao (
  idLocacao, idCliente, idCarro, idVendedor,
  dataLocacao, horaLocacao, dataEntrega, horaEntrega,
  qtdDiaria, vlrDiaria
)
SELECT
  t.idLocacao,
  t.idCliente,
  t.idCarro,
  t.idVendedor,
  CASE
    WHEN t.dataLocacao IS NOT NULL THEN
      substr(CAST(t.dataLocacao AS TEXT),1,4) || '-' ||
      substr(CAST(t.dataLocacao AS TEXT),5,2) || '-' ||
      substr(CAST(t.dataLocacao AS TEXT),7,2)
    ELSE NULL
  END AS dataLocacaoISO,
  t.horaLocacao,
  CASE
    WHEN t.dataEntrega IS NOT NULL THEN
      substr(CAST(t.dataEntrega  AS TEXT),1,4) || '-' ||
      substr(CAST(t.dataEntrega  AS TEXT),5,2) || '-' ||
      substr(CAST(t.dataEntrega  AS TEXT),7,2)
    ELSE NULL
  END AS dataEntregaISO,
  t.horaEntrega,
  t.qtdDiaria,
  t.vlrDiaria
FROM tb_locacao t;