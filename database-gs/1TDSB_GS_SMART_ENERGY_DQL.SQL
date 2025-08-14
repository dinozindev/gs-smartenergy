-- rm558981 – Giovanna Revito Roz
-- rm558986 – Kaian Gustavo
-- rm554424 – Lucas Kenji Kikushi
-- Sala: 1TDSB
-- Professor: Marcel Thomé Filho

DROP TABLE emissoes_carbono CASCADE CONSTRAINTS;
DROP TABLE tipo_fontes CASCADE CONSTRAINTS;
DROP TABLE projetos_sustentaveis CASCADE CONSTRAINTS;
DROP TABLE regioes_sustentaveis CASCADE CONSTRAINTS;

desc PF0645.projetos_sustentaveis;
select * from PF0645.tipo_fontes;
select * from PF0645.regioes_sustentaveis;
select * from PF0645.emissoes_carbono;

-- Questão 1: Exibir o nome do tipo_fonte e a quantidade de projetos por tipo de fonte de energia (somente tipos com mais de 2 projetos, em ordem alfabética de nome)
SELECT  
    tf.nome AS "Nome do Tipo de Fonte",
    COUNT(ps.id_projeto) AS "Quantidade de Projetos"
FROM 
    PF0645.projetos_sustentaveis ps
JOIN 
    PF0645.tipo_fontes tf ON ps.id_tipo_fonte = tf.id_tipo_fonte  -- corrigido para id_tipo_fonte
GROUP BY 
    tf.nome
HAVING 
    COUNT(ps.id_projeto) > 2
ORDER BY 
    tf.nome;

-- Questão 2: Selecionar o id_projeto, descricao, e custo dos projetos que utilizam fontes de energia solar ou eólica
SELECT 
    ps.id_projeto AS "ID do Projeto",
    ps.descricao AS "Descrição",
    ps.custo AS "Custo"
FROM 
    PF0645.projetos_sustentaveis ps
JOIN 
    PF0645.tipo_fontes tf ON ps.id_tipo_fonte = tf.id_tipo_fonte  -- corrigido para id_tipo_fonte
WHERE 
    tf.nome IN ('Solar', 'Eólica')
ORDER BY 
    ps.descricao;

-- Questão 3: Selecionar o id_projeto, descricao, e status dos projetos com custo maior que R$500.000,00 e status "Em andamento"
SELECT 
    ps.id_projeto AS "ID do Projeto",
    ps.descricao AS "Descrição",
    ps.status AS "Status"
FROM 
    PF0645.projetos_sustentaveis ps
WHERE 
    ps.custo > 500000 
    AND ps.status = 'Em andamento'
ORDER BY 
    ps.id_projeto;

-- Questão 4: Selecionar o nome da região e a média do custo dos projetos, agrupando por região, com média arredondada para duas casas decimais, em ordem decrescente de custo
SELECT 
    rs.nome AS "Nome da Região",
    ROUND(AVG(ps.custo), 2) AS "Média de Custo"
FROM 
    PF0645.projetos_sustentaveis ps
JOIN 
    PF0645.regioes_sustentaveis rs ON ps.id_regiao = rs.id_regiao  -- corrigido para id_regiao
GROUP BY 
    rs.nome
ORDER BY 
    "Média de Custo" DESC;

-- Questão 5: Exibir o nome da região, tipo de fonte, quantidade total de projetos e média das emissões de carbono para regiões com média de emissões superior a 5000, arredondada para duas casas decimais
SELECT 
    rs.nome AS "Nome da Região",
    tf.nome AS "Tipo de Fonte",
    COUNT(ps.id_projeto) AS "Quantidade de Projetos",
    ROUND(AVG(ec.emissao), 2) AS "Média de Emissão de Carbono"
FROM 
    PF0645.projetos_sustentaveis ps
JOIN 
    PF0645.tipo_fontes tf ON ps.id_tipo_fonte = tf.id_tipo_fonte  -- associando corretamente a tabela tipo_fontes
JOIN 
    PF0645.regioes_sustentaveis rs ON ps.id_regiao = rs.id_regiao  -- associando corretamente a tabela regioes_sustentaveis
JOIN 
    PF0645.emissoes_carbono ec ON ps.id_tipo_fonte = ec.id_tipo_fonte  -- corrigido para a coluna de relacionamento correta
GROUP BY 
    rs.nome, tf.nome
HAVING 
    AVG(ec.emissao) > 5000
ORDER BY 
    rs.nome, tf.nome;


