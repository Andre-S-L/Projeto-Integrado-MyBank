CREATE DATABASE MyBank;
USE MyBank;

CREATE TABLE tbl_cliente (
    Cliente_ID int PRIMARY KEY AUTO_INCREMENT,
    Cliente_Nome varchar (1200),
    Cliente_CPF char (14),
    Cliente_Nasc date,
    Cliente_Admin tinyint,
    Cliente_Registro datetime
);

CREATE TABLE tbl_conta (
    Conta_ID int PRIMARY KEY AUTO_INCREMENT,
    Conta_Senha varchar (999),
    Conta_PIN char (4),
    Conta_QntAtual decimal (10,2),
    Conta_Ativa tinyint,
    fk_Conta_Cliente_ID int
);
 
CREATE TABLE tbl_transferencia (
    Transferencia_ID int PRIMARY KEY AUTO_INCREMENT,
    fk_Transferencia_Conta_Emissor_ID int,
    Transferencia_Qnt decimal (10,2),
    fk_Transferencia_Conta_Receptor_ID int,
    Transferencia_Data datetime
);

CREATE TABLE tbl_agencia (
    Agencia_ID int PRIMARY KEY AUTO_INCREMENT,
    Agencia_Dinheiro_Total decimal (10,2),
    Agencia_Juros_Atual decimal (5,2),
    Agencia_Devolucao_Prazo_Maximo int,
    Agencia_Nome Varchar (999)
);

CREATE TABLE tbl_emprestimo (
    Emprestimo_ID int PRIMARY KEY AUTO_INCREMENT,
    Emprestimo_Valor decimal (10,2),
    Emprestimo_Taxa_Juros decimal (5,2),
    Emprestimo_Ativo tinyint,
    Emprestimo_Data_Obti date,
    Emprestimo_Data_Devol date,
    Emprestimo_Tempo_Corrido_Dias int,
    Emprestimo_ValorAPagar decimal (10,2),
    fk_Emprestimo_Conta_ID int
);

ALTER TABLE tbl_transferencia ADD CONSTRAINT FK_tbl_transferencia_2
    FOREIGN KEY (fk_Transferencia_Conta_Emissor_ID)
    REFERENCES tbl_conta (Conta_ID);
 
ALTER TABLE tbl_transferencia ADD CONSTRAINT FK_tbl_transferencia_3
    FOREIGN KEY (fk_Transferencia_Conta_Receptor_ID)
    REFERENCES tbl_conta (Conta_ID);
 
ALTER TABLE tbl_emprestimo ADD CONSTRAINT FK_tbl_emprestimo_2
    FOREIGN KEY (fk_Emprestimo_Conta_ID)
    REFERENCES tbl_conta (Conta_ID);
 
ALTER TABLE tbl_conta ADD CONSTRAINT FK_tbl_conta_2
    FOREIGN KEY (fk_Conta_Cliente_ID)
    REFERENCES tbl_cliente (Cliente_ID);
    
INSERT INTO tbl_agencia (Agencia_Dinheiro_Total, Agencia_Juros_Atual, Agencia_Devolucao_Prazo_Maximo, Agencia_Nome) VALUES ('0.00', '9.09', '60', 'MyBank');
INSERT INTO tbl_cliente (Cliente_Nome, Cliente_CPF, Cliente_Admin) VALUES ('Admin', '000.000.000-00', '1');
INSERT INTO tbl_conta (Conta_Senha, Conta_Ativa, fk_Conta_Cliente_ID) VALUES ('ADMIN', '1', '1');