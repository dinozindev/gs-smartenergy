drop table emissoes_carbono cascade constraint;
drop table projetos_sustentaveis cascade constraint;
drop table regioes_sustentaveis cascade constraint;
drop table tipo_fontes cascade constraint;
drop table usuario cascade constraint;
drop table residencia cascade constraint;
drop table previsao_energetica cascade constraint;

create table tipo_fontes AS SELECT * FROM PF0645.tipo_fontes;
create table regioes_sustentaveis AS SELECT * FROM PF0645.regioes_sustentaveis;
create table projetos_sustentaveis AS SELECT * FROM PF0645.projetos_sustentaveis;
create table emissoes_carbono AS SELECT * FROM PF0645.emissoes_carbono;

CREATE TABLE usuario
(
    cpf_usuario CHAR(11) CONSTRAINT usuario_cpf_pk PRIMARY KEY,
    nome_usuario VARCHAR(80) CONSTRAINT usuario_nm_nn NOT NULL,                   
    email VARCHAR(255) CONSTRAINT usuario_mail_nn NOT NULL
    CONSTRAINT usuario_mail_unique UNIQUE,
    telefone CHAR(11) CONSTRAINT usuario_tel_nn NOT NULL,
    senha VARCHAR(30) CONSTRAINT usuario_sen_nn NOT NULL,
    CONSTRAINT chk_senha_usuario CHECK (LENGTH(senha) > 6),
    gasto_mensal NUMBER(9, 2) CONSTRAINT usuario_gasto_nn NOT NULL
);

CREATE TABLE residencia (
    ID_RESIDENCIA CHAR(36) constraint RESIDENCIA_ID_PK PRIMARY KEY, -- gerado no java / python
    CEP CHAR(9) constraint RESIDENCIA_CEP_NN NOT NULL,             
    LOGRADOURO VARCHAR2(70) constraint RESIDENCIA_LOG_NN NOT NULL, -- rua, avenida etc.
    COMPLEMENTO VARCHAR2(70),        
    BAIRRO VARCHAR2(50) constraint RESIDENCIA_BAI_NN NOT NULL,    
    LOCALIDADE VARCHAR2(70) constraint RESIDENCIA_LOC_NN NOT NULL, -- cidade            
    ESTADO VARCHAR(70) constraint RESIDENCIA_EST_NN NOT NULL,
    NUMERO NUMBER(6) constraint RESIDENCIA_NUM_NN NOT NULL,
    CPF_USUARIO CHAR(11) CONSTRAINT residencia_cpf_fk REFERENCES usuario (CPF_USUARIO) ON DELETE CASCADE 
);

CREATE TABLE previsao_energetica (
    PREVISAO_ID CHAR(36) CONSTRAINT PREVISAO_ID_PK PRIMARY KEY, -- uuid na criação no java / python        
    PREVISAO_DATA DATE CONSTRAINT PREVISAO_DATA_NN NOT NULL,            
    PREVISAO_GASTO NUMBER(9,2) CONSTRAINT PREVISAO_GASTO_NN NOT NULL,   
    PREVISAO_STATUS VARCHAR2(50) CONSTRAINT PREVISAO_STATUS_NN NOT NULL,
    CPF_USUARIO CHAR(11) CONSTRAINT previsao_cpf_fk REFERENCES usuario (CPF_USUARIO) ON DELETE CASCADE
);


INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('12345678901', 'Alice Santos', 'alice.santos@example.com', '21987654321', 'senha123', 150.50);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('23456789012', 'Bruno Lima', 'bruno.lima@example.com', '21987654322', 'brun0@lima', 120.75);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('34567890123', 'Carlos Souza', 'carlos.souza@example.com', '21987654323', 'carlossz', 180.30);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('45678901234', 'Daniela Ribeiro', 'daniela.ribeiro@example.com', '21987654324', 'daniela#1', 140.00);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('56789012345', 'Eduardo Pereira', 'eduardo.pereira@example.com', '21987654325', 'edup3reira', 160.40);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('67890123456', 'Fernanda Costa', 'fernanda.costa@example.com', '21987654326', 'f3rnandac', 200.90);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('78901234567', 'Gabriel Mello', 'gabriel.mello@example.com', '21987654327', 'gabmello7', 130.55);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('89012345678', 'Helena Castro', 'helena.castro@example.com', '21987654328', 'helenac1', 175.20);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('90123456789', 'Isabela Martins', 'isabela.martins@example.com', '21987654329', 'isaMart9', 165.35);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('01234567891', 'João Neves', 'joao.neves@example.com', '21987654330', 'joaoneves8', 190.80);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('11234567890', 'Larissa Campos', 'larissa.campos@example.com', '21987654331', 'laric4mpos', 110.25);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('22345678901', 'Marcelo Dias', 'marcelo.dias@example.com', '21987654332', 'm4rdias10', 155.65);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('33456789012', 'Natalia Oliveira', 'natalia.oliveira@example.com', '21987654333', 'natOlv!23', 145.70);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('44567890123', 'Otávio Lima', 'otavio.lima@example.com', '21987654334', 'Ot4vLim@', 125.95);

INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
VALUES ('55678901234', 'Patricia Mendes', 'patricia.mendes@example.com', '21987654335', 'PatMend$5', 210.50);

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('62c8a73a-afe3-49a9-aed7-be5ef4295818', '22030-000', 'Rua das Flores', 'Apto 101', 'Centro', 'Rio de Janeiro', 'Rio de Janeiro', 101, '12345678901');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('ca0f2280-733e-4a75-aba7-10eb123d7882', '22040-000', 'Av. Atlântica', 'Bloco A', 'Copacabana', 'Rio de Janeiro', 'Rio de Janeiro', 202, '23456789012');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('d2973e4d-1cdf-4d77-80df-f9e8a4e2ecc3', '11050-000', 'Rua Marechal Deodoro', NULL, 'Gonzaga', 'Santos', 'São Paulo', 150, '34567890123');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('6a65fb0a-fa17-4f56-991d-d08e02930027', '40140-000', 'Rua Almirante Barroso', 'Casa', 'Ondina', 'Salvador', 'Bahia', 12, '45678901234');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('afa4bcba-b427-4ae8-bd30-477e142cea67', '69037-000', 'Rua do Comércio', 'Sala 4', 'Centro', 'Manaus', 'Amazonas', 305, '56789012345');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('6024a322-f332-41c8-a0a6-f5608020fcc8', '29100-000', 'Av. Vitória', 'Cobertura', 'Jardim Camburi', 'Vitória', 'Espírito Santo', 85, '67890123456');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('41d64dfc-4db6-4d71-8ad8-e02bcbe97b8d', '30180-000', 'Rua Curitiba', 'Galpão', 'Centro', 'Belo Horizonte', 'Minas Gerais', 78, '78901234567');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('78817b73-7fc6-4a39-962c-0b782a73af0a', '05050-000', 'Rua Heitor Penteado', 'Loja 5', 'Vila Madalena', 'São Paulo', 'São Paulo', 22, '89012345678');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('30338730-3e06-4e36-b721-36a1abc73af3', '70070-000', 'Eixo Monumental', NULL, 'Asa Norte', 'Brasília', 'Distrito Federal', 1234, '90123456789');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('557ed58a-b481-44fc-a4a1-404184877a00', '30130-000', 'Av. Amazonas', 'Sala 20', 'Centro', 'Belo Horizonte', 'Minas Gerais', 200, '01234567891');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('b20a3c51-b493-4830-bed1-9333b7f6f27c', '65050-000', 'Rua da Paz', NULL, 'Renascença', 'São Luís', 'Maranhão', 32, '11234567890');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('fb3e8cc2-9d5e-4b53-b001-566c7bb36e9d', '88010-000', 'Rua Felipe Schmidt', NULL, 'Centro', 'Florianópolis', 'Santa Catarina', 54, '22345678901');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('c6b319f0-03c2-48cb-854d-40968d0fe297', '87010-000', 'Av. Herval', 'Cobertura', 'Zona 1', 'Maringá', 'Paraná', 402, '33456789012');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('6d90228f-4468-4078-94e0-c973a2987d00', '13400-000', 'Rua do Sol', 'Apto 10', 'Centro', 'Piracicaba', 'São Paulo', 88, '44567890123');

INSERT INTO residencia (ID_RESIDENCIA, CEP, LOGRADOURO, COMPLEMENTO, BAIRRO, LOCALIDADE, ESTADO, NUMERO, CPF_USUARIO)
VALUES ('174677c1-7256-441d-8247-c6dfb6a5dfe3', '29050-000', 'Av. César Hilal', 'Loja A', 'Santa Lúcia', 'Vitória', 'Espírito Santo', 66, '55678901234');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('4a6c1c85-e8f2-4a5f-92a9-1fa8ebdf3a47', TO_DATE('01-NOV-2024', 'DD-MON-YYYY'), 150.50, 'CONCLUIDO', '12345678901');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('b3c924ab-0ed9-4692-9cda-7d97f26d8f91', TO_DATE('05-NOV-2024', 'DD-MON-YYYY'), 120.75, 'CONCLUIDO', '23456789012');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('842f2e15-5b4f-43ab-9a8d-2fa8f52a9945', TO_DATE('10-NOV-2024', 'DD-MON-YYYY'), 180.30, 'CONCLUIDO', '34567890123');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('d62535c7-939c-4db3-84e0-0c67412fa870', TO_DATE('12-NOV-2024', 'DD-MON-YYYY'), 140.00, 'CONCLUIDO', '45678901234');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('ea891d13-f27d-4bbd-b229-9379cf8f7b99', TO_DATE('15-NOV-2024', 'DD-MON-YYYY'), 160.40, 'CONCLUIDO', '56789012345');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('b3ec1767-8a2e-4379-9efc-7b3654d9a32c', TO_DATE('18-NOV-2024', 'DD-MON-YYYY'), 200.90, 'CONCLUIDO', '67890123456');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('f98b65f6-e17f-4d5d-8c93-5e7f758cf66f', TO_DATE('20-NOV-2024', 'DD-MON-YYYY'), 130.55, 'CONCLUIDO', '78901234567');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('c1af894b-b7b3-4e2f-a882-81cb6d2333ad', TO_DATE('22-NOV-2024', 'DD-MON-YYYY'), 175.20, 'CONCLUIDO', '89012345678');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('882c4d23-d77b-4e45-89b4-16d3793f0d5a', TO_DATE('24-NOV-2024', 'DD-MON-YYYY'), 165.35, 'CONCLUIDO', '90123456789');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('70d745ff-d1c2-48d1-ae36-4155ab007ed4', TO_DATE('26-NOV-2024', 'DD-MON-YYYY'), 190.80, 'CONCLUIDO', '01234567891');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('7e8c6cb3-2469-4711-a330-d1fc74bb1e69', TO_DATE('28-NOV-2024', 'DD-MON-YYYY'), 110.25, 'CONCLUIDO', '11234567890');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('f139c037-834f-42f4-9676-f34c1b5b9b67', TO_DATE('29-NOV-2024', 'DD-MON-YYYY'), 155.65, 'CONCLUIDO', '22345678901');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('ba8d49d5-3d53-4d47-b122-396b01c7805c', TO_DATE('05-NOV-2024', 'DD-MON-YYYY'), 145.70, 'CONCLUIDO', '33456789012');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('66eb19c8-cd65-4297-ae68-eab1424c3ae9', TO_DATE('10-NOV-2024', 'DD-MON-YYYY'), 125.95, 'CONCLUIDO', '44567890123');

INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO)
VALUES ('e4e2cf85-c94b-4b6f-83f2-66e3b06c6227', TO_DATE('15-NOV-2024', 'DD-MON-YYYY'), 210.50, 'CONCLUIDO', '55678901234');

commit;