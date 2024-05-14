import oracledb
from colorama import init, Fore, Back, Style
init()

# importar "colorama" e "oracledb"
# mudar informações do BD
# Tirar comentários do CREATE TABLE caso ainda não possua a tabela criada, depois, o CREATE é inútil

Connection = oracledb.connect(
    user = "BD150224214",
    password = "Fbxfk9",
    dsn = "172.16.12.14/xe"
)
cursor = Connection.cursor()

comando = 0

#inserção de dados

def cadastro():
    print(Fore.RED + '''
================================================
            Cadastro de Produtos
================================================
    ''')
 #   cod = int(input("Digite o código do produto: "))
    nome = input("Digite o nome do produto: ")
    desc = input("Digite a descrição do produto: ")
    cp = float(input("Digite o custo do produto: "))
    cf = float(input("Digite o custo fixo/administrativo: "))
    cv = float(input("Digite o valor da comissão de vendas: "))
    iv = float(input("Digite o valor do imposto sobre o produto: "))
    ml = float(input("Digite o valor da rentabilidade: "))

    print(Fore.RESET + Fore.YELLOW + '''\n
================================================
        Cáculo Preço de Venda (PV)
================================================ 
    \n''')
    #cálculo pv
    PV=(cp/(1-((cf+cv+iv+ml)/100)))
    print(f'''
    Descrição ----------------- Valor - % 
    A.Preço de venda            {round(PV,2)}   100%
    B.Custo de Aquisição        {round(cp,2)}   {round(((cp*100)/PV),2)}%
    C.Receita Bruta             {round((PV-cp),2)}  {round((100-(cp*100)/PV),2)}% 
    D.Custo fixo/Administrativo {round((PV*(cf/100)),2)}  {cf}%
    E.Comisão de vendas         {round(((cv/100)*PV),2)}  {cv}% 
    F.Impostos                  {round(PV*(iv/100),2)}  {iv}% 
    G.Outros custos             {round(((PV*(cf/100))+((cv/100)*PV)+((iv/100)*PV)),2)}  {cf+cv+iv}%
    H.Rentabilidade             {round((PV-cp)-((PV*(cf/100))+((cv/100)*PV)+((iv/100)*PV)),2)}  {round(((100-(cp*100)/PV) -(cf+cv+iv)),2)}%\n
    ''')



    if ((100-(cp*100)/PV) -(cf+cv+iv) < 0):
        print("------- PREJUIZO -------\n")
    elif((100-(cp*100)/PV) -(cf+cv+iv) == 0):
        print("------- EQUILÍBRIO -------\n")
    elif(((100-(cp*100)/PV) -(cf+cv+iv) > 0) and ((100-(cp*100)/PV) -(cf+cv+iv) <= 10)):
        print("------- LUCRO BAIXO -------\n")
    elif(((100-(cp*100)/PV) -(cf+cv+iv) > 10) and ((100-(cp*100)/PV) -(cf+cv+iv) <= 20)):
        print("------- LUCRO MÉDIO -------\n")
    else:
        print("------- LUCRO ALTO -------\n")
    print(f"O lucro do(a) {nome} é de {round((100-(cp*100)/PV) -(cf+cv+iv), 2)}% (R${round((PV-cp)-((PV*(cf/100))+((cv/100)*PV)+((iv/100)*PV)),2)})\n" + Fore.RESET)

    # AUTO_INCREMENT MANUAL
    # recuperando o último código de produto da tabela

    # Verificando se há linhas na tabela
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total_linhas = cursor.fetchone()[0]

    # se não houver linhas, cod será 1
    if total_linhas == 0:
        novo_codigo = 1
    # se houver, vai ser o valor do ultimo codigo_produto + 1
    else:
        cursor.execute("""
        SELECT MAX(Codigo_produto)
        FROM produtos
        """)
        ultimo_codigo = cursor.fetchone()[0] # obtendo o valor da consulta em integer para realizar a soma

        # somando 1 para obter o próximo código de produto
        novo_codigo = ultimo_codigo + 1

    # Adicionando a nova linha à tabela 'Produtos'
    cursor.execute("insert into Produtos values (:1, :2, :3, :4, :5, :6, :7, :8)", (novo_codigo, nome, desc, cp, cf, cv, iv, ml))
    Connection.commit()

def tabela():
    print(Fore.GREEN + '''
================================================
     Aqui esão os produtos já cadastrados:
================================================
CÓD. | NOME | DESCRIÇÃO | CP | CF | CV | IV | ML
''')
    for row in cursor.execute("SELECT * FROM produtos ORDER BY codigo_produto ASC"):
        print(row)
    print(Fore.RESET)

def alterar():
    print(Fore.GREEN + '''
================================================
     Aqui esão os produtos já cadastrados:
================================================
CÓD. | NOME | DESCRIÇÃO | CP | CF | CV | IV | ML
''')
    for row in cursor.execute("SELECT * FROM produtos ORDER BY codigo_produto ASC"):
        print(row)
    print(Fore.RESET)

    codAlterar = int(input("Digite o código do produto que deseja alterar: "))

    print(Fore.RED + '''
================================================
              Alterar Produto
================================================
    ''')
    #   cod = int(input("Digite o código do produto: "))
    nome = input("Digite o novo nome do produto: ")
    desc = input("Digite a nova descrição do produto: ")
    cp = float(input("Digite o novo custo do produto: "))
    cf = float(input("Digite o novo custo fixo/administrativo: "))
    cv = float(input("Digite o novo valor da comissão de vendas: "))
    iv = float(input("Digite o novo valor do imposto sobre o produto: "))
    ml = float(input("Digite o novo valor da rentabilidade: "))
    print(Fore.RESET)

    cursor.execute(f"""
                    UPDATE produtos
                    SET codigo_produto = {codAlterar}, nome_produto = '{nome}', Descrição_produto = '{desc}', custo_produto = {cp}, custo_fixo = {cf}, comissão_vendas = {cv}, impostos = {iv}, rentabilidade = {ml}
                    WHERE codigo_produto = {codAlterar}
                    """)
    cursor.execute("COMMIT")

    print(Fore.LIGHTMAGENTA_EX + "Produto alterado com sucesso!" + Fore.RESET)

def excluir():
    print(Fore.GREEN + '''
================================================
     Aqui esão os produtos já cadastrados:
================================================
CÓD. | NOME | DESCRIÇÃO | CP | CF | CV | IV | ML
''')
    for row in cursor.execute("SELECT * FROM produtos ORDER BY codigo_produto ASC"):
        print(row)
    print(Fore.RESET)

    codExcluir = int(input("Digite o código do produto que deseja excluir: "))

    cursor.execute(f"""
                    DELETE FROM produtos WHERE codigo_produto = {codExcluir}
                    """)
    cursor.execute("COMMIT")
    print(Fore.LIGHTMAGENTA_EX + "\nProduto excluido com sucesso!" + Fore.RESET)

def criarTabela():
    cursor.execute("""
                CREATE TABLE Produtos (
                Codigo_produto INTEGER PRIMARY KEY NOT NULL,
                Nome_produto VARCHAR2 (20) not null,
                Descrição_produto VARCHAR2 (50) not null,
                Custo_produto INTEGER not null,
                Custo_fixo INTEGER not null,
                Comissão_vendas INTEGER not null,
                Impostos INTEGER not null,
                Rentabilidade INTEGER not null
                )""")
    
def zerarTabela():
    cursor.execute("DROP TABLE produtos")
    cursor.execute("""
                CREATE TABLE Produtos (
                Codigo_produto INTEGER PRIMARY KEY NOT NULL,
                Nome_produto VARCHAR2 (20) not null,
                Descrição_produto VARCHAR2 (50) not null,
                Custo_produto INTEGER not null,
                Custo_fixo INTEGER not null,
                Comissão_vendas INTEGER not null,
                Impostos INTEGER not null,
                Rentabilidade INTEGER not null
                )""")

    print(Fore.LIGHTMAGENTA_EX + "\nTabela zerada com sucesso!" + Fore.RESET)

def ClassificarLucro():
    # print(Fore.LIGHTMAGENTA_EX + "\nAinda trabalhando nisso!" + Fore.RESET)

    cursor.execute('SELECT * FROM produtos ORDER BY codigo_produto ASC')
    for row in cursor:
        cod = row[0]
        nome = row[1]
        desc = row[2]
        cp = row[3]
        cf = row[4]
        cv = row[5]
        iv = row[6]
        ml = row[7]

        PV=(cp/(1-((cf+cv+iv+ml)/100)))

        print(Fore.YELLOW)
        print(row)
        print(Fore.RESET)

        print(f'''
    Descrição ----------------- Valor - % 
    A.Preço de venda            {round(PV,2)}   100%
    B.Custo de Aquisição        {round(cp,2)}   {round(((cp*100)/PV),2)}%
    C.Receita Bruta             {round((PV-cp),2)}  {round((100-(cp*100)/PV),2)}% 
    D.Custo fixo/Administrativo {round((PV*(cf/100)),2)}  {cf}%
    E.Comisão de vendas         {round(((cv/100)*PV),2)}  {cv}% 
    F.Impostos                  {round(PV*(iv/100),2)}  {iv}% 
    G.Outros custos             {round(((PV*(cf/100))+((cv/100)*PV)+((iv/100)*PV)),2)}  {cf+cv+iv}%
    H.Rentabilidade             {round((PV-cp)-((PV*(cf/100))+((cv/100)*PV)+((iv/100)*PV)),2)}  {round(((100-(cp*100)/PV) -(cf+cv+iv)),2)}%\n
    ''')
        
        if ((100-(cp*100)/PV) -(cf+cv+iv) < 0):
            print("------- PREJUIZO -------\n")
        elif((100-(cp*100)/PV) -(cf+cv+iv) == 0):
            print("------- EQUILÍBRIO -------\n")
        elif(((100-(cp*100)/PV) -(cf+cv+iv) > 0) and ((100-(cp*100)/PV) -(cf+cv+iv) <= 10)):
            print("------- LUCRO BAIXO -------\n")
        elif(((100-(cp*100)/PV) -(cf+cv+iv) > 10) and ((100-(cp*100)/PV) -(cf+cv+iv) <= 20)):
            print("------- LUCRO MÉDIO -------\n")
        else:
            print("------- LUCRO ALTO -------\n")
        print(f"O lucro do(a) {nome} é de {round((100-(cp*100)/PV) -(cf+cv+iv), 2)}% (R${round((PV-cp)-((PV*(cf/100))+((cv/100)*PV)+((iv/100)*PV)),2)})\n" + Fore.RESET)

while comando != 8:
    comando = int(input('''
================================================
                Bem-vindo(a)!
================================================
| [1] Cadastro de produtos                     |
| [2] Visualização da tabela                   |
| [3] Alterar produto                          |
| [4] Excluir produto                          |
| [5] Criar tabela produtos                    |
| [6] Zerar tabela                             |
| [7] Classificar Lucro                        |
| [8] Sair                                     |
================================================

Digite o número do comando: '''))

    if comando == 1:
        cadastro()
    elif comando == 2:
        tabela()
    elif comando == 3:
        alterar()
    elif comando == 4:
        excluir()
    elif comando == 5:
        criarTabela()
    elif comando == 6:
        zerarTabela()
    elif comando == 7:
        ClassificarLucro()
    else:
        break