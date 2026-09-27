-- =========================================================
-- Sistema de Controle de Patrimônio Institucional
-- Script de criação do banco de dados (MySQL)
-- =========================================================

CREATE DATABASE IF NOT EXISTS patrimonio_igreja
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE patrimonio_igreja;

-- Departamentos/setores da instituição (ex: Louvor, Cozinha, Secretaria)
CREATE TABLE IF NOT EXISTS departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Itens do patrimônio
CREATE TABLE IF NOT EXISTS itens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    categoria VARCHAR(100),
    valor DECIMAL(10,2),
    data_aquisicao DATE,
    departamento_id INT,
    status ENUM('disponivel', 'em_uso') NOT NULL DEFAULT 'disponivel',
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
        ON DELETE SET NULL
);

-- Histórico de movimentação (quem pegou, quando devolveu)
CREATE TABLE IF NOT EXISTS movimentacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    responsavel VARCHAR(150) NOT NULL,
    data_retirada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_devolucao DATETIME NULL,
    observacao VARCHAR(255),
    FOREIGN KEY (item_id) REFERENCES itens(id)
        ON DELETE CASCADE
);

-- Departamentos de exemplo (comuns em igrejas) - ajuste conforme a realidade local
INSERT IGNORE INTO departamentos (nome) VALUES
    ('Louvor'),
    ('Infantil'),
    ('Cozinha'),
    ('Secretaria'),
    ('Manutenção');
