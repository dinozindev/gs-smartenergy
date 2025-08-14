-- rm558981 – Giovanna Revito Roz
-- rm558986 – Kaian Gustavo
-- rm5544214 – Lucas Kenji Kikushi
-- Sala: 1TDSB

DROP TABLE emissoes_carbono CASCADE CONSTRAINTS;
DROP TABLE tipo_fontes CASCADE CONSTRAINTS;
DROP TABLE projetos_sustentaveis CASCADE CONSTRAINTS;
DROP TABLE regioes_sustentaveis CASCADE CONSTRAINTS;
DROP TABLE usuario CASCADE CONSTRAINTS;
DROP TABLE residencia CASCADE CONSTRAINTS;
DROP TABLE precisao_energetica CASCADE CONSTRAINTS;

CREATE TABLE emissoes_carbono AS SELECT * FROM PF0645.emissoes_carbono;
CREATE TABLE tipo_fontes AS SELECT * FROM PF0645.tipo_fontes;
CREATE TABLE projetos_sustentaveis AS SELECT * FROM PF0645.projetos_sustentaveis;
CREATE TABLE regioes_sustentaveis AS SELECT * FROM PF0645.regioes_sustentaveis;

desc PF0645.projetos_sustentaveis;
select * from PF0645.tipo_fontes;
select * from PF0645.regioes_sustentaveis;
select * from PF0645.emissoes_carbono;

CREATE TABLE usuario (
    CPF_USUARIO CHAR(11) CONSTRAINT usuariogl_cpf_pk PRIMARY KEY,        
    NOME_USUARIO VARCHAR2(80) CONSTRAINT usuariogl_nome_nn NOT NULL,   
    EMAIL VARCHAR2(255) CONSTRAINT usuariogl_email_nn NOT NULL,
    TELEFONE CHAR(11) CONSTRAINT usuariogl_tel_nn NOT NULL,          
    SENHA VARCHAR2(30) CONSTRAINT usuariogl_senha_nn NOT NULL, 
    GASTO_MENSAL NUMBER(9,2) CONSTRAINT usuariogl_gasto_nn NOT NULL,
    CONSTRAINT chk_senha_usuario_gl CHECK (LENGTH(SENHA) > 6),
    CONSTRAINT usuariogl_email_unique UNIQUE (EMAIL)
);

CREATE TABLE residencia (
    ID_RESIDENCIA CHAR(36) CONSTRAINT residencia_id_pk PRIMARY KEY, 
    CEP CHAR(9) CONSTRAINT residencia_cep_nn NOT NULL,             
    LOGRADOURO VARCHAR2(70) CONSTRAINT residencia_log_nn NOT NULL, 
    COMPLEMENTO VARCHAR2(70),        
    BAIRRO VARCHAR2(50) CONSTRAINT residencia_bai_nn NOT NULL,    
    LOCALIDADE VARCHAR2(70) CONSTRAINT residencia_loc_nn NOT NULL,            
    ESTADO VARCHAR(70) CONSTRAINT residencia_est_nn NOT NULL,
    NUMERO NUMBER(6) CONSTRAINT residencia_num_nn NOT NULL,
    CPF_USUARIO CHAR(11) CONSTRAINT residencia_cpf_fk REFERENCES usuario (CPF_USUARIO) ON DELETE CASCADE 
);

CREATE TABLE previsao_energetica (
    PREVISAO_ID CHAR(36) CONSTRAINT precisao_id_pk PRIMARY KEY,        
    PREVISAO_DATA DATE CONSTRAINT precisao_data_nn NOT NULL,            
    PREVISAO_GASTO NUMBER(9,2) CONSTRAINT precisao_gasto_nn NOT NULL,   
    PREVISAO_STATUS VARCHAR2(50) CONSTRAINT precisao_status_nn NOT NULL,
    CPF_USUARIO CHAR(11) CONSTRAINT precisao_cpf_fk REFERENCES usuario (CPF_USUARIO) ON DELETE CASCADE
);

SELECT * FROM USUARIO;
SELECT * FROM RESIDENCIA;
SELECT * FROM PREVISAO_ENERGETICA;
