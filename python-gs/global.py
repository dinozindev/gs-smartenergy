import oracledb #pip install oracledb
import json # exportação para json 
import pandas as pd #pip install pandas
import re # regex
import openpyxl #pip install openpyxl - para permitir exportação para .xlsx
import uuid
# módulo importado para utilização de datetime
from datetime import datetime

# expressões regulares
regexValor = r'^\d{1,8}(\.\d{1,2})?$'
regexValor7 = r'^\d{1,7}(\.\d{1,2})?$'
regexNome = r"^[A-Za-zÀ-ÿ'\- ]+$"
regexEmail = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
regexTel = r"^\d{2} \d{5}-\d{4}$" 
regexCpf = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$' 
regexCep = r'^\d{5}-\d{3}$'
regexNumero = r'^\d{1,6}$'
regexData = r"^(0[1-9]|[12][0-9]|3[01])-(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)-\d{4}$"

# Configura o Pandas para exibir todas as linhas e colunas
pd.set_option('display.max_rows', None)  # Sem limite para linhas
pd.set_option('display.max_columns', None)  # Sem limite para colunas
pd.set_option('display.width', None)  # Sem limitação de largura
pd.set_option('display.max_colwidth', None)  # Sem limitação para largura das colunas

# FUNÇÕES REUTILIZÁVEIS
# exporta os registros para json
def exportar_para_json(dados_tabela, nome_arquivo):
    with open(nome_arquivo, 'w') as json_file:
        json.dump(dados_tabela, json_file, indent=4)
    print(f"\nDados exportados para arquivo de nome: {nome_arquivo} com sucesso! ✅")

# exporta os registros para excel
def exportar_para_excel(dados_tabela, nome_arquivo):
    df = pd.DataFrame(dados_tabela)
    df.to_excel(nome_arquivo, index=False, engine='openpyxl')
    print(f"\nDados exportados para arquivo de nome: {nome_arquivo} com sucesso! ✅")

# retorna os dados da tabela --> retornar_colunas = True para a função de exportar registros para JSON
# utilização de parametros adicionais --> parametros_adicionais = params
def select_registros(select_sql, parametros_adicionais=None, retornar_colunas=False):
    with conectar() as conn:
        cursor = conn.cursor()
        if parametros_adicionais:
            cursor.execute(select_sql, parametros_adicionais)
        else:
            cursor.execute(select_sql)
        dados = cursor.fetchall()
        if retornar_colunas:
            colunas = [coluna[0] for coluna in cursor.description]
            cursor.close()
            return dados, colunas
        cursor.close()
        return dados

# verifica se existe algum registro em X tabela
def existem_registros(select_sql):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(select_sql)
        registro_count = cursor.fetchone()[0] > 0
        cursor.close()
        return registro_count

# transforma a data para que possa ser passada ao JSON
def serialize_data(data):
    if isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, datetime):
        return data.isoformat()  # Converte datetime para string no formato ISO
    return data 

# definindo conexão com banco de dados.
def conectar():
    return oracledb.connect (
        user="RM554424",
        password="040704",
        dsn="oracle.fiap.com.br:1521/orcl"
    )

# FUNÇÕES DO USUÁRIO
# cadastrar usuario
def cadastro_usuario():
    print("Iniciando cadastro do usuário...\n")
    usuario = {}
    # cadastro nome
    while True:
        try:
            nome = input("Digite o nome..................................: ").strip()
            if re.match(regexNome, nome) is None:
                raise ValueError("Digite um nome válido.") 
            if len(nome) > 80:
                raise ValueError("Digite um nome com até 80 caracteres.")   
        except ValueError as e:
            print(e)  
        else:
            usuario['nome'] = nome
            print('Nome registrado com sucesso.')
            break
    # cadastro email
    while True:
        try:
            email = input("Digite o email.................................: ").strip()
            if re.match(regexEmail, email) is None:
                raise ValueError("Digite um email válido.")
            if len(email) > 255:
                raise ValueError("Digite um email com até 255 caracteres.")
            if verificar_email_repetido(email):
                raise ValueError("O email inserido já está cadastrado.")
        except ValueError as e:
            print(e)
        else:
            usuario['email'] = email
            print('Email registrado com sucesso.')
            break
    # cadastro senha
    while True:
        try:
            senha = input("Digite uma nova senha..........................: ").strip()
            if len(senha) <= 6 or len(senha) > 30:
                raise ValueError("Sua senha deve conter ao menos 6 e no máximo 30 caracteres.")
        except ValueError as e:
            print(e)
        else:
            usuario['senha'] = senha
            print("Senha registrada com sucesso.")
            break
    # cadastro CPF
    while True:
        try:
            cpf = input("Digite o CPF (ex: xxx.xxx.xxx-xx)..............: ")
            cpf_repetido = verificar_usuario(cpf)
            if cpf_repetido:
                raise ValueError("O CPF inserido já está sendo utilizado.")
        except ValueError as e:
            print(e) 
        else:
            cpf = re.sub(r"[.-]", "", cpf)
            usuario['cpf'] = cpf
            print('CPF registrado com sucesso.')
            break
    # cadastro telefone
    while True:
        try:
            telefone = input("Digite o número de telefone (ex: xx xxxxx-xxxx): ")
            if re.match(regexTel, telefone) is None:
                raise ValueError("Digite um número de telefone válido.")
        except ValueError as e:
            print(e)
        else:
            telefone_formatado = re.sub(r"[ -]", "", telefone)
            usuario['telefone'] = telefone_formatado
            print("Telefone registrado com sucesso.")
            break
    usuario['gasto_mensal'] = 0
    
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) 
                VALUES (:cpf, :nome, :email, :telefone, :senha, :gasto_mensal)""", 
                usuario)
            conn.commit()
            print("\nUsuário cadastrado com sucesso! ✅")
        except oracledb.DatabaseError as e:
            error, = e.args 
            print("\nErro ao cadastrar o usuário no SQL!")
            print("Código do erro:", error.code)
            print("Mensagem do erro:", error.message)
            print("Contexto do erro:", error.context)
        finally:
            cursor.close()

# visualizar um usuário pelo CPF
def read_usuario(cpf):
    try:
        if not verificar_usuario(cpf):
            raise ValueError("\nUsuário não encontrado.")
        cpf = re.sub(r"[.-]", "", cpf)
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal FROM usuario WHERE cpf_usuario = :cpf", {"cpf": cpf})
                usuario_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_usuario(usuario_atual)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu do usuário...")

# visualizar todos os usuários
def read_all_usuarios():
        usuarios = select_registros("SELECT * FROM usuario")
        if usuarios:
            for usuario in usuarios:
                imprimir_usuario(usuario)
        else:
            print("\nNenhum registro encontrado de usuário.\n")
        input("Pressione ENTER para voltar ao menu: ")
        print("\nRetornando ao menu do usuário...")

# imprime os dados do usuário
def imprimir_usuario(usuario_atual):
        print(f"\n==============[ INFORMAÇÕES DO USUÁRIO {usuario_atual[1]} ]==============\n") 
        print(f"CPF..............: {usuario_atual[0]}")
        print(f"Nome.............: {usuario_atual[1]}") 
        print(f"Email............: {usuario_atual[2]}") 
        print(f"Telefone.........: {usuario_atual[3]}") 
        print(f"Senha............: {usuario_atual[4]}") 
        print(f"Gasto Mensal.....: {usuario_atual[5]}KWh \n")

# deleta um usuario a partir do CPF
def deletar_usuario(cpf):
    try:
        if not verificar_usuario(cpf):
            raise ValueError("Usuário não encontrado.")
        cpf = re.sub(r"[.-]", "", cpf)
        with conectar() as conn:
            with conn.cursor() as cursor:              
                while True:
                    op_delete = input(f"\nDeseja realmente deletar o usuário de CPF {cpf}? (a residência e as previsões energéticas também serão removidos) S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM usuario WHERE cpf_usuario = :cpf", {"cpf": cpf})
                        conn.commit()
                        print("\nUsuário removido com sucesso! ✅")
                        break
                    elif op_delete.upper() == "N":
                        print("\nUsuário não foi removido.")
                        break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de usuário...')

# atualiza um usuario
def atualizar_usuario(cpf):
    try:
        if not verificar_usuario(cpf):
            raise ValueError("Usuário não encontrado.")
        cpf = re.sub(r"[.-]", "", cpf)
        with conectar() as conn:
            with conn.cursor() as cursor:                 
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DO USUÁRIO 🚹 ]==============\n")
                    print("1 - Atualizar Nome")
                    print("2 - Atualizar Email")
                    print("3 - Atualizar Telefone")
                    print("4 - Atualizar Senha") 
                    print("5 - Atualizar Gasto Mensal") 
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 5 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        break
                    match op_atualizar:
                        case 1:
                            while True:
                                try:
                                    nome = input("Digite o novo nome............................: ").strip()
                                    if re.match(regexNome, nome) is None:
                                        raise ValueError("Digite um nome válido.")
                                    if len(nome) > 80:
                                        raise ValueError("Digite um nome com até 80 caracteres.")    
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE usuario SET nome_usuario = :nome WHERE cpf_usuario = :cpf", {"nome": nome, "cpf": cpf})
                                    conn.commit()
                                    print('\nNome atualizado com sucesso. ✅')
                                    break
                        case 2:
                            while True:
                                try:
                                    email = input("Digite o novo email..........................: ").strip()
                                    if re.match(regexEmail, email) is None:
                                        raise ValueError("Digite um email válido.")
                                    if len(email) > 255:
                                        raise ValueError("Digite um email com até 255 caracteres.")
                                    if verificar_email_repetido(email):
                                        raise ValueError("O email inserido já foi cadastrado.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE usuario SET email = :email WHERE cpf_usuario = :cpf", {"email": email, "cpf": cpf})
                                    conn.commit()
                                    print('\nEmail atualizado com sucesso. ✅')
                                    break
                        case 3:
                            while True:
                                try:
                                    telefone = input("Digite o novo número de telefone (ex: xx xxxxx-xxxx): ")
                                    if re.match(regexTel, telefone) is None:
                                        raise ValueError("Digite um número de telefone válido.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    telefone = re.sub(r"[ -]", "", telefone)
                                    cursor.execute("UPDATE usuario SET telefone = :telefone WHERE cpf_usuario = :cpf", {"telefone": telefone, "cpf": cpf})
                                    conn.commit()
                                    print("\nTelefone atualizado com sucesso. ✅")
                                    break
                        case 4:
                            while True:
                                try:
                                    senha = input("Digite uma nova senha......................: ").strip()
                                    if len(senha) <= 6 or len(senha) > 30:
                                        raise ValueError("Sua senha deve conter ao menos 6 e no máximo 30 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE usuario SET senha = :senha WHERE cpf_usuario = :cpf", {"senha": senha, "cpf": cpf})
                                    conn.commit()
                                    print("\nSenha atualizada com sucesso. ✅")
                                    break
                        case 5:
                            while True:
                                try:
                                    gasto_mensal = float(input("Qual o novo gasto mensal (Em KWh)?.....: "))
                                    if gasto_mensal <= 0:
                                        raise ValueError("Digite um valor maior que zero.")
                                    gasto_mensal = str(gasto_mensal)
                                    if re.match(regexValor7, gasto_mensal) is None:
                                            raise ValueError("Digite um gasto_mensal válido (10 dígitos no máximo, 2 casas decimais no máximo)") 
                                    gasto_mensal = float(gasto_mensal)
                                except ValueError as e:
                                    if "could not convert string to float" in str(e):
                                        print("Digite um valor numérico válido.")
                                    else:
                                        print(e)
                                else:
                                    cursor.execute("UPDATE usuario SET gasto_mensal = :gasto_mensal WHERE cpf_usuario = :cpf", {"gasto_mensal": gasto_mensal, "cpf": cpf})
                                    conn.commit()
                                    print('\nGasto Mensal atualizado com sucesso. ✅')
                                    break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de usuário...')

# verifica a existencia do usuario e retorna o usuario
def verificar_usuario(cpf):
    # verifica formato do CPF
    if re.match(regexCpf, cpf) is None:
        raise ValueError("Digite um CPF válido.")
    cpf = re.sub(r"[.-]", "", cpf) 
    # busca o usuario pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE cpf_usuario = :cpf", {"cpf": cpf})
        usuario_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return usuario_existe

# exporta os registros de usuarios em JSON
def exportar_usuarios_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM usuario") == False:
            raise ValueError("\nNenhum usuário cadastrado.")
        usuarios, colunas = select_registros("SELECT * FROM usuario", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de usuários para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                usuarios_json = [dict(zip(colunas, usuario)) for usuario in usuarios]
                exportar_para_json(usuarios_json, 'usuarios.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de usuário...')

# exporta os registros de usuarios em Excel (.xlsx)
def exportar_usuarios_excel():
    try:
        if existem_registros("SELECT COUNT(1) FROM usuario") == False:
            raise ValueError("\nNenhum usuário cadastrado.")
        usuarios, colunas = select_registros("SELECT * FROM usuario ORDER BY 1", None, True)
        while True:
            export_opt = input("\nDeseja exportar os registros de usuários para Excel (.xlsx)? (S ou N): ").upper()
            if export_opt == 'S':
                usuarios_excel = [dict(zip(colunas, usuario)) for usuario in usuarios]
                exportar_para_excel(usuarios_excel, 'usuarios.xlsx')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de usuários...')

# gerenciamento usuario
def gerenciar_usuario():
        print("\nIniciando menu de gerenciamento do usuário...") 
        while True:
            print("\n==============[ GERENCIAMENTO DE USUÁRIOS​ ]==============\n")
            print("1 - Cadastrar Usuário")
            print("2 - Visualizar Usuário por CPF")
            print("3 - Visualizar todos os Usuários")
            print("4 - Atualizar Usuário")
            print("5 - Deletar Usuário")
            print("6 - Exportar Usuários para JSON")
            print("7 - Exportar Usuários para Excel")
            print("0 - Sair")
            verif_usuario_op = input("\nSelecione uma opção: ")
            if not verif_usuario_op.isdigit() or int(verif_usuario_op) > 7 or int(verif_usuario_op) < 0:
                print("\nSelecione uma opção válida.")
                continue
            verif_usuario_op = int(verif_usuario_op)
            if verif_usuario_op == 0:
                break
            elif verif_usuario_op == 1:
                cadastro_usuario()
            elif verif_usuario_op == 2:
                input_cpf = input("Digite o CPF do Usuário que deseja visualizar (xxx.xxx.xxx-xx): ")
                read_usuario(input_cpf)
            elif verif_usuario_op == 3:
                read_all_usuarios()
            elif verif_usuario_op == 4:
                input_cpf = input("Digite o CPF do Usuário que deseja atualizar (xxx.xxx.xxx-xx).: ")
                atualizar_usuario(input_cpf)
            elif verif_usuario_op == 5:
                input_cpf = input("Digite o CPF do Usuário que deseja deletar (xxx.xxx.xxx-xx)...: ")
                deletar_usuario(input_cpf)
            elif verif_usuario_op == 6:
                exportar_usuarios_json()
            elif verif_usuario_op == 7:
                exportar_usuarios_excel()

# verifica se o email do usuário já existe (UNIQUE)
def verificar_email_repetido(email):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE email = :email", {"email": email})
        email_repetido = cursor.fetchone()[0] > 0
        cursor.close()
        return email_repetido

# verifica se o usuario ja tem uma residencia cadastrada em seu nome 
def verificar_usuario_residencia(cpf):
    # verifica formato do CPF
    if re.match(regexCpf, cpf) is None:
        raise ValueError("Digite um CPF válido.")
    cpf = re.sub(r"[.-]", "", cpf) 
    # busca o usuario pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM residencia WHERE cpf_usuario = :cpf", {"cpf": cpf})
        usuario_possui_residencia = cursor.fetchone()[0] > 0
        cursor.close()
        return usuario_possui_residencia

# atualiza gasto mensal do usuario (relacionado a previsao_energetica)
def atualizar_gasto_usuario(cpf, novo_gasto):
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE usuario
                SET gasto_mensal = :novo_gasto
                WHERE cpf_usuario = :cpf
            """, {"novo_gasto": novo_gasto, "cpf": cpf})
            conn.commit()
            print(f"Gasto mensal do Usuário de CPF {cpf} atualizado para {novo_gasto:.2f}KWh")
        except oracledb.DatabaseError as e:
            error, = e.args
            print("Erro ao atualizar o gasto mensal:", error.message)

# FUNÇÕES DA RESIDÊNCIA
# cadastrar residencia
def cadastro_residencia(cpf):
    residencia = {}
    try:
        if not verificar_usuario(cpf):
            raise ValueError('Usuário não encontrado.')
        if verificar_usuario_residencia(cpf):
            raise ValueError("Usuário já possui residência cadastrada em seu nome. Impossível cadastrar outra.")
        cpf = re.sub(r"[.-]", "", cpf) 
    except ValueError as e:
        print(e)
    else:
        print("Iniciando cadastro da residência...\n")
        residencia['cpf_usuario'] = cpf
        residencia['id_residencia'] = str(uuid.uuid4())
        # cadastro cep
        while True:
            try:
                cep = input("Digite o CEP (Formato: XXXXX-XXX)................................: ").strip()
                if re.match(regexCep, cep) is None:
                    raise ValueError("Digite um CEP válido.")   
            except ValueError as e:
                print(e)  
            else:
                residencia['cep'] = cep
                print('CEP registrado com sucesso.')
                break
        # cadastro logradouro
        while True:
            try:
                logradouro = input("Digite o logradouro / endereço...................................: ").strip()
                if len(logradouro) < 5:
                    raise ValueError("Digite um logradouro com pelo menos 5 caracteres.")
                if len(logradouro) > 70:
                    raise ValueError("Digite um logradouro com até 70 caracteres.")
            except ValueError as e:
                print(e)
            else:
                residencia['logradouro'] = logradouro
                print('Logradouro registrado com sucesso.')
                break
        # cadastro complemento
        while True:
            try:
                complemento = input("Digite um complemento (Ex: Casa, Loja)...........................: ").strip()
                if len(complemento) > 70:
                    raise ValueError("O complemento deve ter no máximo 70 caracteres.")
            except ValueError as e:
                print(e)
            else:
                residencia['complemento'] = complemento
                print("Complemento registrado com sucesso.")
                break
        # cadastro bairro
        while True:
            try:
                bairro = input("Digite o bairro..................................................: ").strip()
                if len(bairro) < 2:
                    raise ValueError("Digite um bairro com pelo menos 2 caracteres.")
                if len(bairro) > 50:
                    raise ValueError("Digite um bairro com até 50 caracteres.")
            except ValueError as e:
                print(e) 
            else:
                residencia['bairro'] = bairro
                print('Bairro registrado com sucesso.')
                break
        # cadastro cidade
        while True:
            try:
                cidade = input("Digite a cidade..................................................: ").strip()
                if len(cidade) < 2:
                    raise ValueError("Digite uma cidade com pelo menos 2 caracteres.")
                if len(cidade) > 70:
                    raise ValueError("Digite uma cidade com até 70 caracteres.")
            except ValueError as e:
                print(e) 
            else:
                residencia['localidade'] = cidade
                print('Cidade registrado com sucesso.')
                break
        # cadastro estado
        while True:
            try:
                estado = input("Digite o estado..................................................: ").strip()
                if len(estado) < 5:
                    raise ValueError("Digite um estado com pelo menos 5 caracteres.")
                if len(estado) > 70:
                    raise ValueError("Digite um estado com até 70 caracteres.")
            except ValueError as e:
                print(e) 
            else:
                residencia['estado'] = estado
                print('Estado registrado com sucesso.')
                break
        # cadastro numero
        while True:
            try:
                numero = input("Digite o número da residência....................................: ")
                if re.match(regexNumero, numero) is None:
                    raise ValueError("Digite um número de residência válido (máximo de 6 dígitos).")
            except ValueError as e:
                print(e)
            else:
                numero = int(numero)
                residencia['numero'] = numero
                print("Número registrado com sucesso.")
                break
        
        with conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO residencia (id_residencia, cep, logradouro, complemento, bairro, localidade, estado, numero, cpf_usuario) 
                    VALUES (:id_residencia, :cep, :logradouro, :complemento, :bairro, :localidade, :estado, :numero, :cpf_usuario)""", 
                    residencia)
                conn.commit()
                print(f"\nResidência de ID {residencia['id_residencia']} cadastrada com sucesso! ✅")
            except oracledb.DatabaseError as e:
                error, = e.args 
                print("\nErro ao cadastrar a Residência no SQL!")
                print("Código do erro:", error.code)
                print("Mensagem do erro:", error.message)
                print("Contexto do erro:", error.context)
            finally:
                cursor.close()

# visualizar uma residência pelo ID
def read_residencia(id):
    try:
        if not verificar_residencia(id):
            raise ValueError("\nResidência não encontrada.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM residencia WHERE id_residencia = :id", {"id": id})
                residencia = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_residencia(residencia)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de residência...")

# visualizar todas as residências
def read_all_residencias():
        residencias = select_registros("SELECT * FROM residencia")
        if residencias:
            for residencia in residencias:
                imprimir_residencia(residencia)
        else:
            print("\nNenhum registro encontrado de residência.\n")
        input("Pressione ENTER para voltar ao menu: ")
        print("\nRetornando ao menu de residência...")

# imprime os dados da residência
def imprimir_residencia(residencia):
        print(f"\n==============[ INFORMAÇÕES DA RESIDÊNCIA DE ID {residencia[0]} ]==============\n") 
        print(f"ID....................: {residencia[0]}")
        print(f"CEP...................: {residencia[1]}") 
        print(f"Logradouro / Endereço.: {residencia[2]}") 
        print(f"Complemento...........: {residencia[3] if residencia[3] != None else "Nenhum"}") 
        print(f"Bairro................: {residencia[4]}") 
        print(f"Cidade................: {residencia[5]}")
        print(f"Estado................: {residencia[6]}")
        print(f"Número................: {residencia[7]}")
        print(f"CPF do Proprietário...: {residencia[8]}\n")

# deleta uma residência pelo ID
def deletar_residencia(id):
    try:
        if not verificar_residencia(id):
            raise ValueError("Residência não encontrada.")
        with conectar() as conn:
            with conn.cursor() as cursor:              
                while True:
                    op_delete = input(f"\nDeseja realmente deletar a residência de ID {id}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM residencia WHERE id_residencia = :id", {"id": id})
                        conn.commit()
                        print("\nResidência removida com sucesso! ✅")
                        break
                    elif op_delete.upper() == "N":
                        print("\nResidência não foi removida.")
                        break
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de Residência...')

# atualiza os dados da residência
def atualizar_residencia(id):
    try:
        if not verificar_residencia(id):
            raise ValueError("Residência não encontrada.")
        with conectar() as conn:
            with conn.cursor() as cursor:                 
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DA RESIDÊNCIA ]==============\n")
                    print("1 - Atualizar CEP")
                    print("2 - Atualizar Logradouro / Endereço")
                    print("3 - Atualizar Complemento")
                    print("4 - Atualizar Bairro") 
                    print("5 - Atualizar Cidade") 
                    print("6 - Atualizar Estado")
                    print("7 - Atualizar Número")
                    print("8 - Atualizar Proprietário")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 8 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        break
                    match op_atualizar:
                        case 1:
                            while True:
                                try:
                                    cep = input("Digite o novo CEP (Formato: XXXXX-XXX).............................: ").strip()
                                    if re.match(regexCep, cep) is None:
                                        raise ValueError("Digite um CEP válido.")   
                                except ValueError as e:
                                    print(e)  
                                else:
                                    cursor.execute("UPDATE residencia SET cep = :cep WHERE id_residencia = :id", {"cep": cep, "id": id})
                                    conn.commit()
                                    print('\nCEP atualizado com sucesso. ✅')
                                    break       
                        case 2:
                            while True:
                                try:
                                    logradouro = input("Digite o novo logradouro / endereço.................................: ").strip()
                                    if len(logradouro) < 5:
                                        raise ValueError("Digite um logradouro com pelo menos 5 caracteres.")
                                    if len(logradouro) > 70:
                                        raise ValueError("Digite um logradouro com até 70 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE residencia SET logradouro = :logradouro WHERE id_residencia = :id", {"logradouro": logradouro, "id": id})
                                    conn.commit()
                                    print('\nLogradouro atualizado com sucesso. ✅')
                                    break               
                        case 3:
                            while True:
                                try:
                                    complemento = input("Digite um novo complemento (Ex: Casa, Loja)..........................: ").strip()
                                    if len(complemento) > 70:
                                        raise ValueError("O complemento deve ter no máximo 70 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE residencia SET complemento = :complemento WHERE id_residencia = :id", {"complemento": complemento, "id": id})
                                    conn.commit()
                                    print("\nComplemento atualizado com sucesso. ✅")
                                    break
                        case 4:
                            while True:
                                try:
                                    bairro = input("Digite o novo bairro..............: ").strip()
                                    if len(bairro) < 2:
                                        raise ValueError("Digite um bairro com pelo menos 2 caracteres.")
                                    if len(bairro) > 50:
                                        raise ValueError("Digite um bairro com até 50 caracteres.")
                                except ValueError as e:
                                    print(e) 
                                else:
                                    cursor.execute("UPDATE residencia SET bairro = :bairro WHERE id_residencia = :id", {"bairro": bairro, "id": id})
                                    conn.commit()
                                    print("\nBairro atualizado com sucesso. ✅")
                                    break
                        case 5:
                            while True:
                                try:
                                    cidade = input("Digite a nova cidade..............: ").strip()
                                    if len(cidade) < 2:
                                        raise ValueError("Digite uma cidade com pelo menos 2 caracteres.")
                                    if len(cidade) > 70:
                                        raise ValueError("Digite uma cidade com até 70 caracteres.")
                                except ValueError as e:
                                    print(e) 
                                else:
                                    cursor.execute("UPDATE residencia SET localidade = :localidade WHERE id_residencia = :id", {"localidade": cidade, "id": id})
                                    conn.commit()
                                    print('\nCidade atualizada com sucesso. ✅')
                                    break
                        case 6:
                            while True:
                                try:
                                    estado = input("Digite o novo estado..............: ").strip()
                                    if len(estado) < 5:
                                        raise ValueError("Digite um estado com pelo menos 5 caracteres.")
                                    if len(estado) > 70:
                                        raise ValueError("Digite um estado com até 70 caracteres.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE residencia SET estado = :estado WHERE id_residencia = :id", {"estado": estado, "id": id})
                                    conn.commit()
                                    print('\nEstado atualizado com sucesso. ✅')
                                    break
                        case 7:
                            while True:
                                try:
                                    numero = input("Digite o novo número da residência: ")
                                    if re.match(regexNumero, numero) is None:
                                        raise ValueError("Digite um número de residência válido (máximo de 6 dígitos).")
                                except ValueError as e:
                                    print(e)
                                else:
                                    numero = int(numero)
                                    cursor.execute("UPDATE residencia SET numero = :numero WHERE id_residencia = :id", {"numero": numero, "id": id})
                                    conn.commit()
                                    print('\nNúmero da residência atualizado com sucesso. ✅')
                                    break
                        case 8:
                            while True:
                                try:
                                    cpf = input("Digite o CPF do novo proprietário (Formato: xxx.xxx.xxx-xx): ")
                                    if not verificar_usuario(cpf):
                                        raise ValueError('Usuário não encontrado.')
                                    if verificar_usuario_residencia(cpf):
                                        raise ValueError("Usuário já possui residência cadastrada em seu nome. Impossível associá-lo a residência atual.")
                                except ValueError as e:
                                    print(e)
                                    break
                                else:
                                    cpf = re.sub(r"[.-]", "", cpf) 
                                    cursor.execute("UPDATE residencia SET cpf_usuario = :cpf WHERE id_residencia = :id", {"cpf": cpf, "id": id})
                                    conn.commit()
                                    print('\nProprietário atualizado com sucesso. ✅')
                                    break

    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de usuário...')

# exporta as residencias para json
def exportar_residencias_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM residencia") == False:
            raise ValueError("\nNenhuma residência cadastrada.")
        residencias, colunas = select_registros("SELECT * FROM residencia", None, True)
        while True:
            export_opt = input("\nDeseja exportar os registros de residências para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                residencias_json = [dict(zip(colunas, residencia)) for residencia in residencias]
                exportar_para_json(residencias_json, 'residencias.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de residências...')

# exporta as residencias para excel
def exportar_residencias_excel():
    try:
        if existem_registros("SELECT COUNT(1) FROM residencia") == False:
            raise ValueError("\nNenhuma residência cadastrada.")
        residencias, colunas = select_registros("SELECT * FROM residencia ORDER BY 1", None, True)
        while True:
            export_opt = input("\nDeseja exportar os registros de residências para Excel (.xlsx)? (S ou N): ").upper()
            if export_opt == 'S':
                residencias_excel = [dict(zip(colunas, residencia)) for residencia in residencias]
                exportar_para_excel(residencias_excel, 'residencias.xlsx')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de residências...')

# gerenciamento residencia
def gerenciar_residencia():
        print("\nIniciando menu de gerenciamento de residência...") 
        while True:
            print("\n==============[ GERENCIAMENTO DE RESIDÊNCIAS ]==============\n")
            print("1 - Cadastrar Residência")
            print("2 - Visualizar Residência por ID")
            print("3 - Visualizar todas as Residências")
            print("4 - Atualizar Residência")
            print("5 - Deletar Residência")
            print("6 - Exportar Residências para JSON")
            print("7 - Exportar Residências para Excel")
            print("0 - Sair")
            verif_residencia_op = input("\nSelecione uma opção: ")
            if not verif_residencia_op.isdigit() or int(verif_residencia_op) > 7 or int(verif_residencia_op) < 0:
                print("\nSelecione uma opção válida.")
                continue
            verif_residencia_op = int(verif_residencia_op)
            if verif_residencia_op == 0:
                break
            elif verif_residencia_op == 1:
                cpf_input = input("Digite o CPF do Usuário que deseja cadastrar a residência (xxx.xxx.xxx-xx): ")
                cadastro_residencia(cpf_input)
            elif verif_residencia_op == 2:
                id_residencia = input("Digite o ID da residência que deseja visualizar: ")
                read_residencia(id_residencia)
            elif verif_residencia_op == 3:
                read_all_residencias()
            elif verif_residencia_op == 4:
                id_residencia = input("Digite o ID da residência que deseja atualizar.: ")
                atualizar_residencia(id_residencia)
            elif verif_residencia_op == 5:
                id_residencia = input("Digite o ID da residência que deseja deletar...: ")
                deletar_residencia(id_residencia)
            elif verif_residencia_op == 6:
                exportar_residencias_json()
            elif verif_residencia_op == 7:
                exportar_residencias_excel()

# verifica a existencia da residencia e retorna a residencia
def verificar_residencia(id):
    # busca a residencia pelo banco de dados
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM residencia WHERE id_residencia = :id", {"id": id})
        residencia_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return residencia_existe

# FUNÇÕES DO PROJETO SUSTENTÁVEL
# criação de um projeto
def criar_projeto():
    projeto = {}
    try:
        fontes, regioes = verificar_fontes_regioes()
    except ValueError as e:
        print(e)
    else:
        print("\nIniciando Criação de Projeto Sustentável...")
        while True:
            try:
                id = input("Digite o ID do projeto (Valor numérico, sem ponto decimal): ")
                if not id.isdigit():
                    raise ValueError("Digite um valor numérico válido.")
                id_repetido = verificar_projeto(id)
                if id_repetido:
                    raise ValueError("O ID inserido já foi cadastrado.")
            except ValueError as e:
                print(e) 
            else: 
                projeto['id_projeto'] = int(id)
                print('ID registrado com sucesso.')
                break
        while True:
            try:
                if fontes:
                    print("\n==============[ TIPOS DE FONTES DE ENERGIA ]==============\n")
                    for i in range(len(list(fontes))):
                        print(f"{i} - {fontes[i][1]}")
                    op_fonte = input("\nQual tipo de fonte é utilizada no projeto?: ")
                    if not op_fonte.isdigit() or int(op_fonte) > (len(list(fontes)) - 1) or int(op_fonte) < 0:
                        raise ValueError("\nSelecione uma opção válida.")
            except ValueError as e:
                print(e)
            else: 
                op_fonte = int(op_fonte)
                projeto['id_tipo_fonte'] = fontes[op_fonte][0]
                print('Tipo de fonte registrada com sucesso.')
                break
        while True:
            try:
                if regioes:
                    print("\n==============[ REGIÕES SUSTENTÁVEIS ]==============\n")
                    for i in range(len(list(regioes))):
                        print(f"{i} - {regioes[i][1]}")
                    op_regiao = input("\nEm qual região o projeto está?: ")
                    if not op_regiao.isdigit() or int(op_regiao) > (len(list(regioes)) - 1) or int(op_regiao) < 0:
                        raise ValueError("\nSelecione uma opção válida.")
            except ValueError as e:
                print(e)
            else: 
                op_regiao = int(op_regiao)
                projeto['id_regiao'] = regioes[op_regiao][0]
                print('Região Sustentável registrada com sucesso.')
                break
        while True:
            try:
                custo = float(input("Qual o custo do projeto?.....: "))
                if custo <= 0:
                    raise ValueError("Digite um valor maior que zero.")
                custo = str(custo)
                if re.match(regexValor, custo) is None:
                        raise ValueError("Digite uma custo válido (10 dígitos no máximo, 2 casas decimais no máximo)") 
                custo = float(custo)
            except ValueError as e:
                if "could not convert string" in str(e):
                    print("Digite um valor numérico válido.")
                else:
                    print(e)
            else:
                print("Custo registrado com sucesso.")
                projeto['custo'] = custo
                break
        while True:
            try:
                descricao_projeto = input("Digite a descrição do projeto................................: ").strip()
                if not descricao_projeto:
                    raise ValueError("Digite uma descrição válida.")
                if len(descricao_projeto) > 255:
                    raise ValueError("A descrição deve ter no máximo 255 caracteres.") 
            except ValueError as e:
                print(e)
            else:
                projeto['descricao'] = descricao_projeto
                print('Descrição registrada com sucesso.')
                break
        while True:
            try: 
                status = input("Qual o status do projeto? ('Concluido' ou 'Em Andamento'): ")
                if status != "Concluido" and status != "Em Andamento":
                    raise ValueError("Digite uma opção válida.")
            except ValueError as e:
                print(e)
            else:
                projeto['status'] = status
                print('Status registrado com sucesso.')
                break

        with conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO projetos_sustentaveis (id_projeto, descricao, custo, status, id_tipo_fonte, id_regiao) 
                    VALUES (:id_projeto, :descricao, :custo, :status, :id_tipo_fonte, :id_regiao)""", 
                    projeto)
                conn.commit()
                print(f"\nProjeto de ID: {id} cadastrado com sucesso! ✅​") 
            except oracledb.DatabaseError as e:
                error, = e.args 
                print("\nErro ao cadastrar o Projeto no SQL!")
                print("Código do erro:", error.code)
                print("Mensagem do erro:", error.message)
                print("Contexto do erro:", error.context)
            finally:
                cursor.close()
    finally:
        print('\nRetornando ao menu de projetos...')

# atualiza o projeto
def atualizar_projeto(id):
    try:
        if not verificar_projeto(id):
            raise ValueError("Projeto não encontrado.")
        fontes, regioes = verificar_fontes_regioes()
    except ValueError as e:
        print(e)
    else:
        id = int(id)
        with conectar() as conn:
            with conn.cursor() as cursor:                 
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DO PROJETO ]==============\n")
                    print("1 - Atualizar Descrição")
                    print("2 - Atualizar Custo")
                    print("3 - Atualizar Status")
                    print("4 - Atualizar Tipo de Fonte")  
                    print("5 - Atualizar Região Sustentável")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 5 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        break
                    match op_atualizar:
                        case 1:
                            while True:
                                try:
                                    descricao_projeto = input("Digite a nova descrição do projeto................................: ").strip()
                                    if not descricao_projeto:
                                        raise ValueError("Digite uma descrição válida.")
                                    if len(descricao_projeto) > 255:
                                        raise ValueError("A descrição deve ter no máximo 255 caracteres.") 
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE projetos_sustentaveis SET descricao = :descricao_projeto WHERE id_projeto = :id", {"descricao_projeto": descricao_projeto, "id": id})
                                    conn.commit()
                                    print('\nDescrição atualizada com sucesso. ✅')
                                    break
                        case 2:
                            while True:
                                try:
                                    custo = float(input("Qual o novo custo do projeto?.....: "))
                                    if custo <= 0:
                                        raise ValueError("Digite um valor maior que zero.")
                                    custo = str(custo)
                                    if re.match(regexValor, custo) is None:
                                            raise ValueError("Digite um custo válido (10 dígitos no máximo, 2 casas decimais no máximo)") 
                                    custo = float(custo)
                                except ValueError as e:
                                    if "could not convert string to float" in str(e):
                                        print("Digite um valor numérico válido.")
                                    else:
                                        print(e)
                                else:
                                    cursor.execute("UPDATE projetos_sustentaveis SET custo = :custo WHERE id_projeto = :id", {"custo": custo, "id": id})
                                    conn.commit()
                                    print('\nCusto atualizado com sucesso. ✅')
                                    break
                        case 3:
                            while True:
                                try:
                                    status = input("Qual o novo status do projeto? ('Concluido' ou 'Em Andamento'): ")
                                    if status != "Concluido" and status != "Em Andamento":
                                        raise ValueError("Digite uma opção válida.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE projetos_sustentaveis SET status = :status WHERE id_projeto = :id", {"status": status, "id": id})
                                    conn.commit()
                                    print("\nStatus atualizado com sucesso. ✅")
                                    break
                        case 4:
                            while True:
                                try:
                                    if fontes:
                                        print("\n==============[ TIPOS DE FONTES DE ENERGIA ]==============\n")
                                        for i in range(len(list(fontes))):
                                            print(f"{i} - {fontes[i][1]}")
                                        op_fonte = input("\nQual tipo de fonte é utilizada no projeto?: ")
                                        if not op_fonte.isdigit() or int(op_fonte) > (len(list(fontes)) - 1) or int(op_fonte) < 0:
                                            raise ValueError("\nSelecione uma opção válida.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    id_fonte = fontes[int(op_fonte)][0]
                                    cursor.execute("UPDATE projetos_sustentaveis SET id_tipo_fonte = :id_fonte WHERE id_projeto = :id", {"id_fonte": id_fonte, "id": id})
                                    conn.commit()
                                    print("\nFonte atualizada com sucesso. ✅")
                                    break
                        case 5:
                            while True:
                                try:
                                    if regioes:
                                        print("\n==============[ REGIÕES SUSTENTÁVEIS ]==============\n")
                                        for i in range(len(list(regioes))):
                                            print(f"{i} - {regioes[i][1]}")
                                        op_regiao = input("\nEm qual região o projeto está?: ")
                                        if not op_regiao.isdigit() or int(op_regiao) > (len(list(regioes)) - 1) or int(op_regiao) < 0:
                                            raise ValueError("\nSelecione uma opção válida.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    id_regiao = regioes[int(op_regiao)][0]
                                    cursor.execute("UPDATE projetos_sustentaveis SET id_regiao = :id_regiao WHERE id_projeto = :id", {"id_regiao": id_regiao, "id": id})
                                    conn.commit()
                                    print("\nRegião atualizada com sucesso. ✅")
                                    break
    finally:
        print('\nRetornando ao menu de projetos...')

# remove o projeto
def deletar_projeto(id):
    try:
        if not verificar_projeto(id):
            raise ValueError("Projeto não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente deletar o Projeto Sustentável de ID {id}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM projetos_sustentaveis WHERE id_projeto = :id", {"id": id})
                        conn.commit()
                        print("\nProjeto removido com sucesso. ✅​")
                        break
                    elif op_delete.upper() == "N":
                        print("\nProjeto não foi removido.")
                        break
    except ValueError as e:
        print(e)   
    finally:
        print('\nRetornando ao menu de Projetos...') 

# get projeto
def read_projeto(id):
    try:
        if not verificar_projeto(id):
            raise ValueError("\nProjeto não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_projeto, descricao, custo, status, id_tipo_fonte, id_regiao FROM projetos_sustentaveis WHERE id_projeto = :id", {"id": id})
                projeto_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_projeto(projeto_atual)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de projetos...")

# get * projetos
def read_all_projetos():
        projetos = select_registros("SELECT * FROM projetos_sustentaveis ORDER BY 1")
        if projetos:
            imprimir_multiplos_projetos(projetos)
        else:
            print("\nNenhum registro encontrado de projeto.\n")
        input("\nPressione ENTER para voltar ao menu: ")
        print("\nRetornando ao menu de projetos...")

# imprime um projeto
def imprimir_projeto(projeto_atual):
    print(f"\n==============[ INFORMAÇÕES DO PROJETO DE ID {projeto_atual[0]} ]==============\n") 
    print(f"ID................: {projeto_atual[0]}")
    print(f"Descrição.........: {projeto_atual[1]}") 
    print(f"Custo.............: R${projeto_atual[2]}") 
    print(f"Status............: {projeto_atual[3]}") 
    print(f"Tipo de Fonte.....: {obter_fonte(projeto_atual[4])[0]}")
    print(f"Região............: {obter_regiao(projeto_atual[5])[0]}\n") 

# imprime todos os registros
def imprimir_multiplos_projetos(projetos):
    df = pd.DataFrame(projetos, columns=['ID do Projeto', 'Descrição', 'Custo', 'Status', 'ID do Tipo de Fonte', 'ID da Região'])
    print(f"\n==============================================[ INFORMAÇÕES DOS PROJETOS SUSTENTÁVEIS ]==============================================\n") 
    print(df)

# exporta os registros de projeto em JSON
def exportar_projetos_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM projetos_sustentaveis") == False:
            raise ValueError("\nNenhum projeto cadastrado.")
        projetos, colunas = select_registros("SELECT * FROM projetos_sustentaveis ORDER BY 1", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de projetos para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                projetos_json = [dict(zip(colunas, projeto)) for projeto in projetos]
                exportar_para_json(projetos_json, 'projetos.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de projetos...')

# exporta os registros de projeto em Excel (.xlsx)
def exportar_projetos_excel():
    try:
        if existem_registros("SELECT COUNT(1) FROM projetos_sustentaveis") == False:
            raise ValueError("\nNenhum projeto cadastrado.")
        projetos, colunas = select_registros("SELECT * FROM projetos_sustentaveis ORDER BY 1", None, True)
        while True:
            export_opt = input("\nDeseja exportar os registros de projetos para Excel (.xlsx)? (S ou N): ").upper()
            if export_opt == 'S':
                projetos_excel = [dict(zip(colunas, projeto)) for projeto in projetos]
                exportar_para_excel(projetos_excel, 'projetos.xlsx')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de projetos...')

# gerenciamento projeto sustentavel
def gerenciar_projetos():
        print("\nIniciando menu de gerenciamento de projetos...") 
        while True:
            print("\n==============[ GERENCIAMENTO DE PROJETOS​ ]==============\n")
            print("1 - Visualizar Projeto por ID")
            print("2 - Visualizar todos os Projetos")
            print("3 - Criar Projeto")
            print("4 - Atualizar Projeto")
            print("5 - Deletar Projeto")
            print("6 - Exportar Projetos para JSON")
            print("7 - Exportar Projetos para Excel")
            print("0 - Sair")
            verif_projeto_op = input("\nSelecione uma opção: ")
            if not verif_projeto_op.isdigit() or int(verif_projeto_op) > 7 or int(verif_projeto_op) < 0:
                print("\nSelecione uma opção válida.")
                continue
            verif_projeto_op = int(verif_projeto_op)
            if verif_projeto_op == 0:
                break
            elif verif_projeto_op == 1:
                id = input("Digite o ID do projeto sustentável que deseja visualizar: ")
                read_projeto(id)
            elif verif_projeto_op == 2:
                read_all_projetos()
            elif verif_projeto_op == 3:
                criar_projeto()
            elif verif_projeto_op == 4:
                id = input("Digite o ID do projeto sustentável que deseja atualizar: ")
                atualizar_projeto(id)
            elif verif_projeto_op == 5:
                id = input("Digite o ID do projeto sustentável que deseja deletar: ")
                deletar_projeto(id)
            elif verif_projeto_op == 6:
                exportar_projetos_json()
            elif verif_projeto_op == 7:
                exportar_projetos_excel()

# verifica existencia do projeto   
def verificar_projeto(id):
    try:
        if isinstance(id, float):
            raise ValueError("Digite um valor inteiro para o ID, não um número com ponto decimal.")
        if not id.isdigit():
            raise ValueError("Digite um valor numérico válido.")
        id = int(id)
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM projetos_sustentaveis WHERE id_projeto = :id", {"id": id})
            projeto_existe = cursor.fetchone()[0] > 0
            cursor.close()
            return projeto_existe
    except ValueError as e:
            if "could not convert string" in str(e) or "invalid literal" in str(e):
                print("Digite um valor numérico válido para o ID.")
            else:
                print(e)

# FUNÇÕES DA EMISSÃO DE CARBONO
# cria uma emissão
def criar_emissao():
    emissao = {}
    try:
        fontes = verificar_fontes()
    except ValueError as e:
        print(e)
    else:
        print("\nIniciando Criação de Emissão de Carbono...\n")
        while True:
            try:
                id = input("Digite o ID da emissão de carbono (Valor numérico, sem ponto decimal): ")
                if not id.isdigit():
                    raise ValueError("Digite um valor numérico válido.")
                id_repetido = verificar_emissao(id)
                if id_repetido:
                    raise ValueError("O ID inserido já foi cadastrado.")
            except ValueError as e:
                print(e) 
            else: 
                emissao['id_emissao'] = int(id)
                print('ID registrado com sucesso.')
                break
        while True:
            try:
                if fontes:
                    print("\n==============[ TIPOS DE FONTES DE ENERGIA ]==============\n")
                    for i in range(len(list(fontes))):
                        print(f"{i} - {fontes[i][1]}")
                    op_fonte = input("\nQual tipo de fonte gera a emissão de carbono?: ")
                    if not op_fonte.isdigit() or int(op_fonte) > (len(list(fontes)) - 1) or int(op_fonte) < 0:
                        raise ValueError("\nSelecione uma opção válida.")
            except ValueError as e:
                print(e)
            else: 
                op_fonte = int(op_fonte)
                emissao['id_tipo_fonte'] = fontes[op_fonte][0]
                print('Tipo de fonte registrada com sucesso.')
                break
        while True:
            try:
                emissao_valor = float(input("Qual a quantidade de emissão de carbono?.....: "))
                if emissao_valor <= 0:
                    raise ValueError("Digite um valor maior que zero.")
                emissao_valor = str(emissao_valor)
                if re.match(regexValor, emissao_valor) is None:
                        raise ValueError("Digite uma emissão válida (10 dígitos no máximo, 2 casas decimais no máximo)") 
                emissao_valor = float(emissao_valor)
            except ValueError as e:
                if "could not convert string" in str(e):
                    print("Digite um valor numérico válido.")
                else:
                    print(e)
            else:
                print("Quantidade de emissão registrada com sucesso.")
                emissao['emissao'] = emissao_valor
                break

        with conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO emissoes_carbono (id_emissao, id_tipo_fonte, emissao) 
                    VALUES (:id_emissao, :id_tipo_fonte, :emissao)""", 
                    emissao)
                conn.commit()
                print(f"\nEmissão de ID: {id} cadastrada com sucesso! ✅​") 
            except oracledb.DatabaseError as e:
                error, = e.args 
                print("\nErro ao cadastrar a Emissão no SQL!")
                print("Código do erro:", error.code)
                print("Mensagem do erro:", error.message)
                print("Contexto do erro:", error.context)
            finally:
                cursor.close()
    finally:
        print('\nRetornando ao menu de emissões...')

# atualiza a emissão
def atualizar_emissao(id):
    try:
        if not verificar_emissao(id):
            raise ValueError("Emissão não encontrada.")
        fontes = verificar_fontes()
    except ValueError as e:
        print(e)
    else:
        id = int(id)
        with conectar() as conn:
            with conn.cursor() as cursor:                 
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DA EMISSÃO ]==============\n")
                    print("1 - Atualizar Tipo de Fonte")
                    print("2 - Atualizar Quantidade de Emissão")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 2 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        break
                    match op_atualizar:
                        case 1:
                            while True:
                                try:
                                    if fontes:
                                        print("\n==============[ TIPOS DE FONTES DE ENERGIA ]==============\n")
                                        for i in range(len(list(fontes))):
                                            print(f"{i} - {fontes[i][1]}")
                                        op_fonte = input("\nQual novo tipo de fonte gera a emissão de carbono?: ")
                                        if not op_fonte.isdigit() or int(op_fonte) > (len(list(fontes)) - 1) or int(op_fonte) < 0:
                                            raise ValueError("\nSelecione uma opção válida.")
                                except ValueError as e:
                                    print(e)
                                else:
                                    id_fonte = fontes[int(op_fonte)][0]
                                    cursor.execute("UPDATE emissoes_carbono SET id_tipo_fonte = :id_fonte WHERE id_emissao = :id", {"id_fonte": id_fonte, "id": id})
                                    conn.commit()
                                    print("\nFonte atualizada com sucesso. ✅")
                                    break

                        case 2:
                            while True:
                                try:
                                    emissao_valor = float(input("Qual a nova quantidade de emissão de carbono?.....: "))
                                    if emissao_valor <= 0:
                                        raise ValueError("Digite um valor maior que zero.")
                                    emissao_valor = str(emissao_valor)
                                    if re.match(regexValor, emissao_valor) is None:
                                        raise ValueError("Digite uma emissão válida (10 dígitos no máximo, 2 casas decimais no máximo)") 
                                    emissao_valor = float(emissao_valor)
                                except ValueError as e:
                                    if "could not convert string to float" in str(e):
                                        print("Digite um valor numérico válido.")
                                    else:
                                        print(e)
                                else:
                                    cursor.execute("UPDATE emissoes_carbono SET emissao = :emissao_valor WHERE id_emissao = :id", {"emissao_valor": emissao_valor, "id": id})
                                    conn.commit()
                                    print('\nCusto atualizado com sucesso. ✅')
                                    break
                        
    finally:
        print('\nRetornando ao menu de emissões...')

# deleta uma emissão
def deletar_emissao(id):
    try:
        if not verificar_emissao(id):
            raise ValueError("Emissão não encontrada.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente deletar a Emissão de ID {id}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM emissoes_carbono WHERE id_emissao = :id", {"id": id})
                        conn.commit()
                        print("\nEmissão removido com sucesso. ✅​")
                        break
                    elif op_delete.upper() == "N":
                        print("\nEmissão não foi removido.")
                        break
    except ValueError as e:
        print(e)   
    finally:
        print('\nRetornando ao menu de Emissões...') 

# get emissao
def read_emissao(id):
    try:
        if not verificar_emissao(id):
            raise ValueError("\nEmissão não encontrada.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_emissao, id_tipo_fonte, emissao FROM emissoes_carbono WHERE id_emissao = :id", {"id": id})
                emissao_atual = cursor.fetchone()
    except ValueError as e:
        print(e)
    else:
        imprimir_emissao(emissao_atual)
        input("Pressione ENTER para voltar ao menu: ")
    finally:
        print("\nRetornando ao menu de emissão...")

# get * emissoes
def read_all_emissoes():
        emissoes = select_registros("SELECT * FROM emissoes_carbono ORDER BY 1")
        if emissoes:
            imprimir_multiplas_emissoes(emissoes)
        else:
            print("\nNenhum registro encontrado de emissão.\n")
        input("\nPressione ENTER para voltar ao menu: ")
        print("\nRetornando ao menu de emissão...")

# imprime uma emissao
def imprimir_emissao(emissao_atual):
    print(f"\n==============[ INFORMAÇÕES DA EMISSÃO DE ID {emissao_atual[0]} ]==============\n") 
    print(f"ID...................: {emissao_atual[0]}")
    print(f"Tipo de Fonte........: {obter_fonte(emissao_atual[1])[0]}")
    print(f"Quantidade de Emissão: {emissao_atual[2]}\n")

# imprime multiplas emissoes
def imprimir_multiplas_emissoes(emissoes):
    df = pd.DataFrame(emissoes, columns=['ID da Emissão', 'ID do Tipo de Fonte', 'Quantidade de Emissão'])
    print(f"\n======================[ INFORMAÇÕES DAS EMISSÕES ]======================\n") 
    print(df)

# exporta os registros de emissao em JSON
def exportar_emissoes_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM emissoes_carbono") == False:
            raise ValueError("\nNenhuma emissão cadastrada.")
        emissoes, colunas = select_registros("SELECT * FROM emissoes_carbono ORDER BY 1", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de emissões para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                emissoes_json = [dict(zip(colunas, emissao)) for emissao in emissoes]
                exportar_para_json(emissoes_json, 'emissoes.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de emissões...')

# exporta os registros de emissao em Excel
def exportar_emissoes_excel():
    try:
        if existem_registros("SELECT COUNT(1) FROM emissoes_carbono") == False:
            raise ValueError("\nNenhuma emissão cadastrada.")
        emissoes, colunas = select_registros("SELECT * FROM emissoes_carbono ORDER BY 1", None, True)
        while True:
            export_opt = input("\nDeseja exportar os registros de emissões para Excel (.xlsx)? (S ou N): ").upper()
            if export_opt == 'S':
                emissoes_excel = [dict(zip(colunas, emissao)) for emissao in emissoes]
                exportar_para_excel(emissoes_excel, 'emissoes.xlsx')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de emissões...')

# verifica se a emissao já existe  
def verificar_emissao(id):
    try:
        if isinstance(id, float):
            raise ValueError("Digite um valor inteiro para o ID, não um número com ponto decimal.")
        if not id.isdigit():
            raise ValueError("Digite um valor numérico válido.")
        id = int(id)
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM emissoes_carbono WHERE id_emissao = :id", {"id": id})
            emissao_existe = cursor.fetchone()[0] > 0
            cursor.close()
            return emissao_existe
    except ValueError as e:
            if "could not convert string" in str(e) or "invalid literal" in str(e):
                print("Digite um valor numérico válido para o ID.")
            else:
                print(e)

# gerenciamento projeto sustentavel
def gerenciar_emissoes():
        print("\nIniciando menu de gerenciamento de emissões...") 
        while True:
            print("\n==============[ GERENCIAMENTO DE EMISSÕES DE CARBONO​ ]==============\n")
            print("1 - Cadastrar Emissão de Carbono")
            print("2 - Visualizar Emissão de Carbono por ID")
            print("3 - Visualizar todas as Emissões de Carbono")
            print("4 - Atualizar Emissão de Carbono")
            print("5 - Deletar Emissão de Carbono")
            print("6 - Exportar Emissões de Carbono para JSON")
            print("7 - Exportar Emissões de Carbono para Excel")
            print("0 - Sair")
            verif_emissao_op = input("\nSelecione uma opção: ")
            if not verif_emissao_op.isdigit() or int(verif_emissao_op) > 7 or int(verif_emissao_op) < 0:
                print("\nSelecione uma opção válida.")
                continue
            verif_emissao_op = int(verif_emissao_op)
            if verif_emissao_op == 0:
                break
            elif verif_emissao_op == 1:
                criar_emissao()
            elif verif_emissao_op == 2:
                id = input("Digite o ID da emissão que deseja visualizar: ")
                read_emissao(id)
            elif verif_emissao_op == 3:
                read_all_emissoes()
            elif verif_emissao_op == 4:
                id = input("Digite o ID da emissão que deseja atualizar: ")
                atualizar_emissao(id)
            elif verif_emissao_op == 5:
                id = input("Digite o ID da emissão que deseja deletar: ")
                deletar_emissao(id)
            elif verif_emissao_op == 6:
                exportar_emissoes_json()
            elif verif_emissao_op == 7:
                exportar_emissoes_excel()

#FUNÇÕES TIPO FONTE
#cria um tipo de fonte
def criar_tipo_fonte():
        tipo_fonte = {}
        print("\nIniciando Criação de Tipo de Fonte...\n")
        while True:
            try:
                id = input("Digite o ID do tipo de fonte (Valor numérico, sem ponto decimal): ")
                if not id.isdigit():
                    raise ValueError("Digite um valor numérico válido.")
                id_repetido = verificar_fonte(id)
                if id_repetido:
                    raise ValueError("O ID inserido já foi cadastrado.")
            except ValueError as e:
                print(e) 
            else: 
                tipo_fonte['id_tipo_fonte'] = int(id)
                print('ID registrado com sucesso.')
                break
        while True:
            try:
                nome = input("Digite o nome da fonte..................................: ").strip()
                if re.match(regexNome, nome) is None:
                    raise ValueError("Digite um nome válido.") 
                if len(nome) > 50:
                    raise ValueError("Digite um nome com até 50 caracteres.") 
                if verificar_nome_fonte(nome):
                    raise ValueError("Nome já existente no banco de dados.")   
            except ValueError as e:
                print(e)  
            else:
                tipo_fonte['nome'] = nome
                print('Nome da fonte registrado com sucesso.')
                break

        with conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO tipo_fontes (id_tipo_fonte, nome) 
                    VALUES (:id_tipo_fonte, :nome)""", 
                    tipo_fonte)
                conn.commit()
                print(f"\nTipo de Fonte de ID: {id} cadastrado com sucesso! ✅​") 
            except oracledb.DatabaseError as e:
                error, = e.args 
                print("\nErro ao cadastrar o Tipo de Fonte no SQL!")
                print("Código do erro:", error.code)
                print("Mensagem do erro:", error.message)
                print("Contexto do erro:", error.context)
            finally:
                print("Retornando ao Menu de Tipos de Fonte...")
                cursor.close()

# atualiza o tipo de fonte
def atualizar_tipo_fonte(id):
    try:
        if not verificar_fonte(id):
            raise ValueError("Tipo de fonte não encontrado.")
        id = int(id)
        with conectar() as conn:
            with conn.cursor() as cursor:                 
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DA EMISSÃO ]==============\n")
                    print("1 - Atualizar Tipo de Fonte")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 1 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        break
                    match op_atualizar:
                        case 1:
                             while True:
                                try:
                                    nome = input("Digite o nome da fonte..................................: ").strip()
                                    if re.match(regexNome, nome) is None:
                                        raise ValueError("Digite um nome válido.") 
                                    if len(nome) > 50:
                                        raise ValueError("Digite um nome com até 50 caracteres.") 
                                    if verificar_nome_fonte(nome):
                                        raise ValueError("Nome já existente no banco de dados.")  
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE tipo_fontes SET nome = :nome WHERE id_tipo_fonte = :id", {"nome": nome, "id": id})
                                    conn.commit()
                                    print('\nNome do Tipo de Fonte atualizado com sucesso. ✅')
                                    break
    except ValueError as e:
        print(e)                    
    finally:
        print('\nRetornando ao menu de tipos de fonte...')

# deleta um tipo de fonte
def deletar_tipo_fonte(id):
    try:
        if not verificar_fonte(id):
            raise ValueError("Tipo de Fonte não encontrado.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente deletar o Tipo de Fonte de ID {id}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM tipo_fontes WHERE id_tipo_fonte = :id", {"id": id})
                        conn.commit()
                        print("\nTipo de Fonte removido com sucesso. ✅​")
                        break
                    elif op_delete.upper() == "N":
                        print("\nTipo de Fonte não foi removido.")
                        break
    except ValueError as e:
        print(e)   
    finally:
        print('\nRetornando ao menu de Tipos de fonte...') 

# get fonte
def read_tipo_fonte(id):
        try:
            if not verificar_fonte(id):
                raise ValueError("\nTipo de Fonte não encontrado.")
            with conectar() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id_tipo_fonte, nome FROM tipo_fontes WHERE id_tipo_fonte = :id", {"id": id})
                    fonte_atual = cursor.fetchone()
        except ValueError as e:
            print(e)
        else:
            imprimir_tipo_fonte(fonte_atual)
            input("Pressione ENTER para voltar ao menu: ")
        finally:
            print("\nRetornando ao menu de fontes...")

# get * fontes
def read_all_fontes():
    fontes = select_registros("SELECT * FROM tipo_fontes")
    if fontes:
        for fonte in fontes:
            imprimir_tipo_fonte(fonte)
    else:
        print("\nNenhum registro encontrado de tipo de fonte.\n")
    input("Pressione ENTER para voltar ao menu: ")
    print("\nRetornando ao menu de fontes...")

# imprime uma fonte
def imprimir_tipo_fonte(fonte_atual):
    print(f"\n==============[ INFORMAÇÕES DO TIPO DE FONTE DE ID {fonte_atual[0]} ]==============\n") 
    print(f"ID...........: {fonte_atual[0]}")
    print(f"Tipo de Fonte: {fonte_atual[1]}\n") 

# exporta os registros de tipos de fontes em JSON
def exportar_fontes_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM tipo_fontes") == False:
            raise ValueError("\nNenhuma fonte cadastrada.")
        fontes, colunas = select_registros("SELECT * FROM tipo_fontes ORDER BY 1", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de tipos de fontes para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                fontes_json = [dict(zip(colunas, fonte)) for fonte in fontes]
                exportar_para_json(fontes_json, 'fontes.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de fontes...')

# exporta os registros de tipos de fontes em Excel
def exportar_fontes_excel():
    try:
        if existem_registros("SELECT COUNT(1) FROM tipo_fontes") == False:
            raise ValueError("\nNenhum tipo de fonte cadastrado.")
        fontes, colunas = select_registros("SELECT * FROM tipo_fontes ORDER BY 1", None, True)
        while True:
            export_opt = input("\nDeseja exportar os registros de tipos de fontes para Excel (.xlsx)? (S ou N): ").upper()
            if export_opt == 'S':
                fontes_excel = [dict(zip(colunas, fonte)) for fonte in fontes]
                exportar_para_excel(fontes_excel, 'fontes.xlsx')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de fontes...')

# gerenciador de fonte
def gerenciar_tipos_fontes():
        print("\nIniciando menu de gerenciamento de Fontes...") 
        while True:
            print("\n==============[ GERENCIAMENTO DE TIPOS DE FONTE DE ENERGIA​ ]==============\n")
            print("1 - Cadastrar Tipo de Fonte")
            print("2 - Visualizar Tipo de Fonte por ID")
            print("3 - Visualizar todos os Tipos de Fonte")
            print("4 - Atualizar Tipo de Fonte")
            print("5 - Deletar Tipo de Fonte")
            print("6 - Exportar Tipos de Fonte para JSON")
            print("7 - Exportar Tipos de Fonte para Excel")
            print("0 - Sair")
            verif_fonte_op = input("\nSelecione uma opção: ")
            if not verif_fonte_op.isdigit() or int(verif_fonte_op) > 7 or int(verif_fonte_op) < 0:
                print("\nSelecione uma opção válida.")
                continue
            verif_fonte_op = int(verif_fonte_op)
            if verif_fonte_op == 0:
                break
            elif verif_fonte_op == 1:
                criar_tipo_fonte()
            elif verif_fonte_op == 2:
                id = input("Digite o ID do tipo de fonte que deseja visualizar: ")
                read_tipo_fonte(id)
            elif verif_fonte_op == 3:
                read_all_fontes()
            elif verif_fonte_op == 4:
                id = input("Digite o ID do tipo de fonte que deseja atualizar: ")
                atualizar_tipo_fonte(id)
            elif verif_fonte_op == 5:
                id = input("Digite o ID do tipo de fonte que deseja deletar: ")
                deletar_tipo_fonte(id)
            elif verif_fonte_op == 6:
                exportar_fontes_json()
            elif verif_fonte_op == 7:
                exportar_fontes_excel()

# verifica se a fonte já existe
def verificar_fonte(id):
    if not id.isdigit():
        raise ValueError("Digite um valor numérico válido.")
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tipo_fontes WHERE id_tipo_fonte = :id", {"id": id})
        fonte_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return fonte_existe

# verifica se o nome já existe
def verificar_nome_fonte(nome):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tipo_fontes WHERE nome = :nome", {"nome": nome})
        centro_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return centro_existe

# obtem o tipo de fonte com base no ID
def obter_fonte(id):
    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT nome FROM tipo_fontes WHERE id_tipo_fonte = :id", {"id": id})
            fonte_nome = cursor.fetchone()
    return fonte_nome

# verifica se alguma fonte existe. Caso exista, retorna todas.
def verificar_fontes():
    fontes = select_registros('SELECT * FROM tipo_fontes order by 1')
    if fontes:
        return fontes
    else:
        raise ValueError('É necessário ao menos 1 fonte para cadastrar uma emissão.')

# FUNÇÕES REGIÕES SUSTENTÁVEIS
# criar região 
def criar_regiao():
        regiao = {}
        print("\nIniciando Criação de Região Sustentável...\n")
        while True:
            try:
                id = input("Digite o ID da região (Valor numérico, sem ponto decimal): ")
                if not id.isdigit():
                    raise ValueError("Digite um valor numérico válido.")
                id_repetido = verificar_regiao(id)
                if id_repetido:
                    raise ValueError("O ID inserido já foi cadastrado.")
            except ValueError as e:
                print(e) 
            else: 
                regiao['id_regiao'] = int(id)
                print('ID registrado com sucesso.')
                break
        while True:
            try:
                nome = input("Digite o nome da região..................................: ").strip()
                if re.match(regexNome, nome) is None:
                    raise ValueError("Digite um nome válido.") 
                if len(nome) > 50:
                    raise ValueError("Digite um nome com até 50 caracteres.") 
                if verificar_nome_regiao(nome):
                    raise ValueError("Nome já existente no banco de dados.")   
            except ValueError as e:
                print(e)  
            else:
                regiao['nome'] = nome
                print('Nome da região registrada com sucesso.')
                break

        with conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO regioes_sustentaveis (id_regiao, nome) 
                    VALUES (:id_regiao, :nome)""", 
                    regiao)
                conn.commit()
                print(f"\nRegião Sustentável de ID: {id} cadastrada com sucesso! ✅​") 
            except oracledb.DatabaseError as e:
                error, = e.args 
                print("\nErro ao cadastrar o Região Sustentável no SQL!")
                print("Código do erro:", error.code)
                print("Mensagem do erro:", error.message)
                print("Contexto do erro:", error.context)
            finally:
                print("Retornando ao Menu de Regiões...")
                cursor.close()

# get regiao
def read_regiao(id):
        try:
            if not verificar_regiao(id):
                raise ValueError("\nRegião sustentável não encontrada.")
            with conectar() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id_regiao, nome FROM regioes_sustentaveis WHERE id_regiao = :id", {"id": id})
                    regiao_atual = cursor.fetchone()
        except ValueError as e:
            print(e)
        else:
            imprimir_regiao(regiao_atual)
            input("Pressione ENTER para voltar ao menu: ")
        finally:
            print("\nRetornando ao menu de Regiões sustentáveis...")

# get * regioes
def read_all_regioes():
    regioes = select_registros("SELECT * FROM regioes_sustentaveis")
    if regioes:
        for regiao in regioes:
            imprimir_regiao(regiao)
    else:
        print("\nNenhum registro encontrado de Região sustentável.\n")
    input("Pressione ENTER para voltar ao menu: ")
    print("\nRetornando ao menu de regiões sustentáveis...")  

# imprime uma região sustentável
def imprimir_regiao(regiao_atual):
    print(f"\n==============[ INFORMAÇÕES DA REGIÃO SUSTENTÁVEL DE ID {regiao_atual[0]} ]==============\n") 
    print(f"ID............: {regiao_atual[0]}")
    print(f"Nome da região: {regiao_atual[1]}\n") 

# atualiza uma região
def atualizar_regiao(id):
    try:
        if not verificar_regiao(id):
            raise ValueError("Região sustentável não encontrada.")
        id = int(id)
        with conectar() as conn:
            with conn.cursor() as cursor:                 
                while True:
                    print("\n==============[ ATUALIZAÇÃO DOS DADOS DA REGIÃO SUSTENTÁVEL ]==============\n")
                    print("1 - Atualizar Nome da Região")
                    print("0 - Sair")
                    op_atualizar = input("\nSelecione uma opção: ")
                    if not op_atualizar.isdigit() or int(op_atualizar) > 1 or int(op_atualizar) < 0:
                        print("\nSelecione uma opção válida.")
                        continue
                    op_atualizar = int(op_atualizar)
                    if op_atualizar == 0:
                        break
                    match op_atualizar:
                        case 1:
                             while True:
                                try:
                                    nome = input("Digite o novo nome da região..................................: ").strip()
                                    if re.match(regexNome, nome) is None:
                                        raise ValueError("Digite um nome válido.") 
                                    if len(nome) > 50:
                                        raise ValueError("Digite um nome com até 50 caracteres.") 
                                    if verificar_nome_regiao(nome):
                                        raise ValueError("Nome já existente no banco de dados.")  
                                except ValueError as e:
                                    print(e)
                                else:
                                    cursor.execute("UPDATE regioes_sustentaveis SET nome = :nome WHERE id_regiao = :id", {"nome": nome, "id": id})
                                    conn.commit()
                                    print('\nNome da região atualizado com sucesso. ✅')
                                    break
    except ValueError as e:
        print(e)                    
    finally:
        print('\nRetornando ao menu de regiões sustentáveis...')

# deleta uma região
def deletar_regiao(id):
    try:
        if not verificar_regiao(id):
            raise ValueError("Região sustentável não encontrada.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente deletar a Região Sustentável de ID {id}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM regioes_sustentaveis WHERE id_regiao = :id", {"id": id})
                        conn.commit()
                        print("\nRegião Sustentável removida com sucesso. ✅​")
                        break
                    elif op_delete.upper() == "N":
                        print("\nRegião Sustentável não foi removida.")
                        break
    except ValueError as e:
        print(e)   
    finally:
        print('\nRetornando ao menu de regiões sustentáveis...') 

# obtem a regiao com base no ID
def obter_regiao(id):
    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT nome FROM regioes_sustentaveis WHERE id_regiao = :id", {"id": id})
            regiao_nome = cursor.fetchone()
    return regiao_nome

# verifica se a região existe
def verificar_regiao(id):
    if not id.isdigit():
        raise ValueError("Digite um valor numérico válido.")
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM regioes_sustentaveis WHERE id_regiao = :id", {"id": id})
        regiao_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return regiao_existe
    
# verifica se ao menos 1 fonte e 1 região existem para que o projeto possa ser cadastrado.
def verificar_fontes_regioes():
    fontes = select_registros('SELECT * FROM tipo_fontes order by 1')
    regioes = select_registros('SELECT * FROM regioes_sustentaveis order by 1')
    if fontes and regioes:
        return fontes, regioes
    else: 
        raise ValueError('É necessário ao menos 1 fonte e 1 região para cadastrar um projeto.')

# verifica se o nome ja foi inserido
def verificar_nome_regiao(nome):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM regioes_sustentaveis WHERE nome = :nome", {"nome": nome})
        nome_regiao_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return nome_regiao_existe

# exporta os registros de tipos de regioes em JSON
def exportar_regioes_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM regioes_sustentaveis") == False:
            raise ValueError("\nNenhuma região cadastrada.")
        regioes, colunas = select_registros("SELECT * FROM regioes_sustentaveis ORDER BY 1", None, True)
        while True:
            export_opt = input("Deseja exportar os registros de Regiões Sustentáveis para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                regioes_json = [dict(zip(colunas, regiao)) for regiao in regioes]
                exportar_para_json(regioes_json, 'regioes.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de regiões...')

# exporta os registros de tipos de regioes em Excel
def exportar_regioes_excel():
    try:
        if existem_registros("SELECT COUNT(1) FROM regioes_sustentaveis") == False:
            raise ValueError("\nNenhuma região cadastrada.")
        regioes, colunas = select_registros("SELECT * FROM regioes_sustentaveis ORDER BY 1", None, True)
        while True:
            export_opt = input("\nDeseja exportar os registros de Regiões Sustentáveis para Excel (.xlsx)? (S ou N): ").upper()
            if export_opt == 'S':
                regioes_excel = [dict(zip(colunas, regiao)) for regiao in regioes]
                exportar_para_excel(regioes_excel, 'regioes.xlsx')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de regiões...')

# gerencia as regiões
def gerenciar_regiao():
        print("\nIniciando menu de gerenciamento de Regiões...") 
        while True:
            print("\n==============[ GERENCIAMENTO DE REGIÕES SUSTENTÁVEIS​ ]==============\n")
            print("1 - Cadastrar Região Sustentável")
            print("2 - Visualizar Região Sustentável por ID")
            print("3 - Visualizar todas as Regiões Sustentáveis")
            print("4 - Atualizar Região Sustentável")
            print("5 - Deletar Região Sustentável")
            print("6 - Exportar Regiões Sustentáveis para JSON")
            print("7 - Exportar Regiões Sustentáveis para Excel")
            print("0 - Sair")
            verif_regiao_op = input("\nSelecione uma opção: ")
            if not verif_regiao_op.isdigit() or int(verif_regiao_op) > 7 or int(verif_regiao_op) < 0:
                print("\nSelecione uma opção válida.")
                continue
            verif_regiao_op = int(verif_regiao_op)
            if verif_regiao_op == 0:
                break
            elif verif_regiao_op == 1:
                criar_regiao()
            elif verif_regiao_op == 2:
                id = input("Digite o ID da região que deseja visualizar: ")
                read_regiao(id)
            elif verif_regiao_op == 3:
                read_all_regioes()
            elif verif_regiao_op == 4:
                id = input("Digite o ID da região que deseja atualizar: ")
                atualizar_regiao(id)
            elif verif_regiao_op == 5:
                id = input("Digite o ID da região que deseja deletar: ")
                deletar_regiao(id)
            elif verif_regiao_op == 6:
                exportar_regioes_json()
            elif verif_regiao_op == 7:
                exportar_regioes_excel()

# mostra tabela energetica
def visualizar_tabela_energetica():
    try:
        usuarios = select_registros("SELECT nome_usuario, gasto_mensal FROM usuario WHERE gasto_mensal != 0 ORDER BY gasto_mensal")
        if not usuarios:
            raise ValueError("Nenhum usuário encontrado.")
    except ValueError as e:
        print(e)
    else:
        nome_tabela = "LEADERBOARD"
        print(f"\n{nome_tabela:^47}\n")
        print("=" * 51)
        print(f"{'Posição':<14}{'Nome':<24}{'Gasto Mensal':<10}")
        print("-" * 51)
        for i, usuario in enumerate(usuarios, start=1):
            match i:
                case 1:
                    print(f"{i:>2}°🥇{'':<8} {usuario[0]:<20} {usuario[1]:>9.2f}KWh")
                case 2:
                    print(f"{i:>2}°🥈{'':<8} {usuario[0]:<20} {usuario[1]:>9.2f}KWh")
                case 3:
                    print(f"{i:>2}°🥉{'':<8} {usuario[0]:<20} {usuario[1]:>9.2f}KWh")
                case _:
                    print(f"{i:>2}°{'':<10} {usuario[0]:<20} {usuario[1]:>9.2f}KWh")
        input("\nPressione ENTER para voltar ao menu: ")
        print("\nRetornando ao menu principal...")

# FUNÇÕES PREVISÃO ENERGETICA
# gerenciador de previsao
def gerenciar_previsao():
    print("\nIniciando menu de gerenciamento de previsão energética...") 
    while True:
            print("\n==============[ GERENCIAMENTO DE PREVISÕES ENERGÉTICAS​ ]==============\n")
            print("1 - Cadastrar Previsão Energética")
            print("2 - Visualizar Previsão Energética por ID")
            print("3 - Visualizar todas as Previsões Energéticas")
            print("4 - Atualizar Status Previsão Energética")
            print("5 - Deletar Previsão Energética")
            print("6 - Exportar Previsões Energéticas para JSON")
            print("7 - Exportar Previsões Energéticas para Excel")
            print("0 - Sair")
            verif_previsao_op = input("\nSelecione uma opção: ")
            if not verif_previsao_op.isdigit() or int(verif_previsao_op) > 7 or int(verif_previsao_op) < 0:
                print("\nSelecione uma opção válida.")
                continue
            verif_previsao_op = int(verif_previsao_op)
            if verif_previsao_op == 0:
                break
            elif verif_previsao_op == 1:
                cpf = input("Digite o CPF do Usuário que fez a Previsão Energética: ")
                criar_previsao(cpf)
            elif verif_previsao_op == 2:
                id = input("Digite o ID da Previsão Energética que deseja visualizar: ")
                read_previsao(id)
            elif verif_previsao_op == 3:
                read_all_previsoes()
            elif verif_previsao_op == 4:
                id = input("Digite o ID da Previsão Energética que deseja atualizar: ")
                atualizar_previsao(id)
            elif verif_previsao_op == 5:
                id = input("Digite o ID da Previsão Energética que deseja deletar: ")
                deletar_previsao(id)
            elif verif_previsao_op == 6:
                exportar_previsoes_json()
            elif verif_previsao_op == 7:
                exportar_previsoes_excel()

# criar previsão energética 
def criar_previsao(cpf):
        previsao = {}
        try:
            if not verificar_usuario(cpf):
                raise ValueError('Usuário não encontrado.')
            cpf = re.sub(r"[.-]", "", cpf) 
        except ValueError as e:
            print(e)
        else:
            previsao['cpf_usuario'] = cpf
            previsao['previsao_id'] = str(uuid.uuid4())
            print("\nIniciando Criação de Região Sustentável...\n")
            while True:
                try:
                    data = input("Qual a Data que a Previsão foi feita? (Ex: DD-MON-YYYY. OBS.: Mês no formato americano)....: ")
                    # Verifica se a entrada corresponde ao formato esperado
                    if re.match(regexData, data) is None:
                        raise ValueError("Digite uma data válida no formato DD-MON-YYYY.")          
                    # Converte a data fornecida para o formato datetime
                    data_previsao = datetime.strptime(data, "%d-%b-%Y")
                    data_hoje = datetime.now()
                    # Verifica se a data fornecida pertence ao mês e ano atuais
                    if data_previsao.year != data_hoje.year or data_previsao.month != data_hoje.month:
                        raise ValueError("A data deve pertencer ao mês e ano atuais.") 
                except ValueError as e:
                    print(e)
                else:
                    previsao['previsao_data'] = data
                    print("Data registrada com sucesso.")
                    break
            while True:
                try:
                    gasto = float(input("Qual o gasto obtido na previsão (Em KWh)?.....: "))
                    if gasto <= 0:
                        raise ValueError("Digite um valor maior que zero.")
                    gasto = str(gasto)
                    if re.match(regexValor, gasto) is None:
                            raise ValueError("Digite um gasto válido (10 dígitos no máximo, 2 casas decimais no máximo)") 
                    gasto = float(gasto)
                except ValueError as e:
                    if "could not convert string" in str(e):
                        print("Digite um valor numérico válido.")
                    else:
                        print(e)
                else:
                    print("Gasto registrado com sucesso.")
                    previsao['previsao_gasto'] = gasto
                    break
            while True:
                try:
                    status_previsao = input("Qual o status da Previsão Energética ('PENDENTE' ou 'CONCLUIDO')?: ").strip().upper()
                    if status_previsao != "PENDENTE" and status_previsao != "CONCLUIDO":
                        raise ValueError("Digite uma opção válida.")
                except ValueError as e:
                    print(e)
                else:
                    print("Status registrado com sucesso.")
                    previsao['previsao_status'] = status_previsao
                    break
                    
            with conectar() as conn:
                cursor = conn.cursor()
                try:
                    previsoes = obter_previsoes_usuario(cpf)
                    if previsoes:
                        data_mais_recente = previsoes[0][1] 

                        if data_mais_recente < data_previsao or data_mais_recente == data_previsao:
                            gasto_mais_recente = previsoes[0][2]
                            print(f"Atualizando gasto do Usuário de CPF {cpf}. Gasto anterior: {gasto_mais_recente}KWh")
                            atualizar_gasto_usuario(cpf, gasto)

                    cursor.execute("""
                        INSERT INTO previsao_energetica 
                        (previsao_id, previsao_data, previsao_gasto, previsao_status, cpf_usuario)
                        VALUES (:previsao_id, :previsao_data, :previsao_gasto, :previsao_status, :cpf_usuario)
                    """, previsao)
                    conn.commit()
                    print(f"\nPrevisão Energética de ID: {previsao['previsao_id']} cadastrada com sucesso! ✅")
                except oracledb.DatabaseError as e:
                    error, = e.args
                    print("Erro ao processar a Previsão Energética:", error.message)
                finally:
                    cursor.close()
                    print("Retornando ao Menu de previsões...")

# get previsão
def read_previsao(id):
        try:
            if not verificar_previsao(id):
                raise ValueError("\nPrevisão energética não encontrada.")
            with conectar() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM previsao_energetica WHERE previsao_id = :id", {"id": id})
                    previsao_atual = cursor.fetchone()
        except ValueError as e:
            print(e)
        else:
            imprimir_previsao(previsao_atual)
            input("Pressione ENTER para voltar ao menu: ")
        finally:
            print("\nRetornando ao menu de Previsões Energéticas...")

# get * previsoes
def read_all_previsoes():
    previsoes = select_registros("SELECT * FROM previsao_energetica")
    if previsoes:
        for previsao in previsoes:
            imprimir_previsao(previsao)
    else:
        print("\nNenhum registro encontrado de Previsão Energética.\n")
    input("Pressione ENTER para voltar ao menu: ")
    print("\nRetornando ao menu de previsões energéticas...")  

# imprime uma previsão
def imprimir_previsao(previsao):
    print(f"\n==============[ INFORMAÇÕES DA PREVISÃO ENERGÉTICA DE ID {previsao[0]} ]==============\n") 
    print(f"ID..............: {previsao[0]}")
    print(f"Data............: {previsao[1]}") 
    print(f"Gasto...........: {previsao[2]}KWh") 
    print(f"Status..........: {previsao[3]}") 
    print(f"CPF do Usuário..: {previsao[4]}\n")

# atualiza uma previsão
def atualizar_previsao(id):
    try:
        if not verificar_previsao(id):
            raise ValueError('\nPrevisão não encontrada.')
    except ValueError as e:
        print(e)
    else:
        with conectar() as conn:
            with conn.cursor() as cursor: 
                while True:
                    try:
                        status_previsao = input("Qual o novo Status da Previsão Energética ('PENDENTE' ou 'CONCLUIDO')?: ").strip().upper()
                        if status_previsao == "PENDENTE" or status_previsao == "CONCLUIDO":
                            cursor.execute("UPDATE previsao_energetica SET previsao_status = :status_previsao WHERE previsao_id = :previsao_id", {"status_previsao": status_previsao, "previsao_id": id})
                            conn.commit()
                            print('\nStatus atualizado com sucesso. ✅​')
                            print("\nRetornando ao menu de previsão energética...") 
                            break
                        else:
                            raise ValueError('Opção inválida.')
                    except ValueError as e:
                        print(e) 

# deleta uma previsão
def deletar_previsao(id):
    try:
        if not verificar_previsao(id):
            raise ValueError("Previsão energética não encontrada.")
        with conectar() as conn:
            with conn.cursor() as cursor:
                while True:
                    op_delete = input(f"\nDeseja realmente deletar a Previsão Energética de ID {id}? S ou N: ")
                    if op_delete.upper() != "S" and op_delete.upper() != "N":
                        print("\nDigite uma opção válida.")
                        continue
                    elif op_delete.upper() == "S":
                        cursor.execute("DELETE FROM previsao_energetica WHERE previsao_id = :id", {"id": id})
                        conn.commit()
                        print("\nPrevisão Energética removida com sucesso. ✅​")
                        break
                    elif op_delete.upper() == "N":
                        print("\nPrevisão Energética não foi removida.")
                        break
    except ValueError as e:
        print(e)   
    finally:
        print('\nRetornando ao menu de regiões sustentáveis...') 

# exporta os registros de previsões energéticas em JSON
def exportar_previsoes_json():
    try:
        if existem_registros("SELECT COUNT(1) FROM previsao_energetica") == False:
            raise ValueError("\nNenhuma previsão energética cadastrada.")
        previsoes, colunas = select_registros("SELECT * FROM previsao_energetica ORDER BY 2", None, True)
        while True:
            export_opt = input("\nDeseja exportar os registros de Previsões Energéticas para JSON? (S ou N): ").upper()
            if export_opt == 'S':
                previsoes_json = [dict(zip(colunas, previsao)) for previsao in previsoes]
                dados_serializados = serialize_data(previsoes_json)
                exportar_para_json(dados_serializados, 'previsoes.json')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de previsões energéticas...')

# exporta os registros de previsões energéticas em Excel
def exportar_previsoes_excel():
    try:
        if existem_registros("SELECT COUNT(1) FROM previsao_energetica") == False:
            raise ValueError("\nNenhuma previsão energética cadastrada.")
        previsoes, colunas = select_registros("SELECT * FROM previsao_energetica ORDER BY 2", None, True)
        while True:
            export_opt = input("\nDeseja exportar os registros de Previsões Energéticas para Excel (.xlsx)? (S ou N): ").upper()
            if export_opt == 'S':
                previsoes_excel = [dict(zip(colunas, previsao)) for previsao in previsoes]
                exportar_para_excel(previsoes_excel, 'previsoes.xlsx')
                break
            elif export_opt == 'N':
                print('\nRegistro não exportado.')
                break
            else:
                print('Digite uma opção válida.') 
                continue  
    except ValueError as e:
        print(e)
    finally:
        print('\nRetornando ao menu de previsões energéticas...')

# verifica se a previsão existe
def verificar_previsao(id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM previsao_energetica WHERE previsao_id = :id", {"id": id})
        previsao_existe = cursor.fetchone()[0] > 0
        cursor.close()
        return previsao_existe

# obtem as previsoes feitas pelo usuario
def obter_previsoes_usuario(cpf):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM previsao_energetica WHERE cpf_usuario = :cpf ORDER BY previsao_data DESC", {"cpf": cpf})
        previsoes = cursor.fetchall()
        cursor.close()
        return previsoes

# menu inicial
while True:
    print("\n==============[ MENU DO SISTEMA SMARTENERGY ]==============\n")
    print("1  - Gerenciar Usuário")
    print("2  - Gerenciar Residência")
    print("3  - Gerenciar Regiões Sustentáveis")
    print("4  - Gerenciar Tipos de Fontes")
    print("5  - Gerenciar Projetos Sustentáveis")
    print("6  - Gerenciar Emissões de Carbono")
    print("7  - Gerenciar Previsão Energética")
    print("8  - Visualizar Tabela Energética")
    print("0  - Sair \n")
    option = input("Opção: ")
    if not option.isdigit() or (int(option) > 8 or int(option) < 0):
        print("\nSelecione uma opção válida.")
        continue
    option = int(option)
    if option == 0:
        print("\nSolicitação encerrada.\n")
        break
    elif option == 1:
        gerenciar_usuario()
    elif option == 2:
        gerenciar_residencia()
    elif option == 3:
        gerenciar_regiao()
    elif option == 4:
        gerenciar_tipos_fontes()
    elif option == 5:
        gerenciar_projetos()
    elif option == 6:
        gerenciar_emissoes() 
    elif option == 7:
        gerenciar_previsao() 
    elif option == 8:
        visualizar_tabela_energetica()   