import oracledb
from colorama import init, Fore, Back, Style
init()

Connection = oracledb.connect(
    user = "BD150224214",
    password = "Fbxfk9",
    dsn = "172.16.12.14/xe"
)
cursor = Connection.cursor()

comando = 0

def criptografia(descricaoEscrita):
    desc = descricaoEscrita
    desc=desc.lower()
    alfa=['z','a', 'b', 'c','d', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',]
    A={'cima':[5,3],'baixo':[7,8]}
    res=[]
    di=[]
    a=[]
    c=[]
    for d in range(len(desc)):
        al=desc[d]
        c.append(al)
        x=alfa.index(al)
        di.append(x)
        if d%2!=0:
            x=((di[d]*A['cima'][1])+(di[d-1]*A['cima'][0]))%26
            y=((di[d]*A['baixo'][1])+(di[d-1]*A['baixo'][0]))%26
            a.append(x)
            a.append(y)
            res.append(alfa[x])
            res.append(alfa[y])
    desc=''
    for k in res:
        desc+=k
    return desc

def descriptografar(desc):  
    desc=desc.lower()
    alfa=['z','a', 'b', 'c','d', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',]
    A={'cima':[88,-33],'baixo':[-77,55]}
    res=[]
    res=[]
    di=[]
    a=[]
    c=[]
    for d in range(len(desc)):
        al=desc[d]
        c.append(al)
        x=alfa.index(al)
        di.append(x)
        if d%2!=0:
            x=((di[d]*A['cima'][1])+(di[d-1]*A['cima'][0]))%26
            y=((di[d]*A['baixo'][1])+(di[d-1]*A['baixo'][0]))%26
            a.append(x)
            a.append(y)
            res.append(alfa[x])
            res.append(alfa[y])
    desc=''
    for k in res:
        desc+=k
    return desc

def cadastro():
    print(Fore.RED + '''
================================================
            Cadastro de Produtos
================================================
    ''')

    # GUARDA INFORMAÇÕES EM VARIÁVEIS
    nome = input("Digite o nome do produto: ")
    descricaoEscrita = input("Digite a descrição do produto: ")
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

    # CALCULA O PV COM AS VARIÁVEIS
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

    #CÁLCULO DE MARGEM E PERCENTUAL DE LUCRO
    clucro = (100-(cp*100)/PV) -(cf+cv+iv)
    if (clucro < 0):
        print("------- PREJUIZO -------\n")
    elif(clucro == 0):
        print("------- EQUILÍBRIO -------\n")
    elif((clucro > 0) and (clucro <= 10)):
        print("------- LUCRO BAIXO -------\n")
    elif((clucro > 10) and (clucro <= 20)):
        print("------- LUCRO MÉDIO -------\n")
    else:
        print("------- LUCRO ALTO -------\n")
    print(f"O lucro do(a) {nome} é de {round(clucro, 2)}% (R${round((PV-cp)-((PV*(cf/100))+((cv/100)*PV)+((iv/100)*PV)),2)})\n" + Fore.RESET)
    # AUTO_INCREMENT MANUAL
    
    cursor.execute("SELECT COUNT(*) FROM produtos")    #  verificando se há linhas na tabela
    total_linhas = cursor.fetchone()[0]     # recuperando o último código de produto da tabela

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
    cursor.execute("insert into Produtos values (:1, :2, :3, :4, :5, :6, :7, :8)", (novo_codigo, nome, criptografia(descricaoEscrita), cp, cf, cv, iv, ml))
    Connection.commit()

def tabela():
    print(f'''{Fore.GREEN}
================================================
     Aqui estão os produtos já cadastrados:
================================================
{Fore.BLUE}CÓD. {Fore.GREEN}| {Fore.LIGHTMAGENTA_EX}NOME {Fore.GREEN}| {Fore.YELLOW}DESCRIÇÃO {Fore.GREEN}| {Fore.RED}CP {Fore.GREEN}| {Fore.CYAN}CF {Fore.GREEN}| {Fore.LIGHTBLACK_EX}CV {Fore.GREEN}| {Fore.MAGENTA}IV {Fore.GREEN}| {Fore.LIGHTGREEN_EX}ML
{Fore.RESET}''')
    for row in cursor.execute("SELECT * FROM produtos ORDER BY codigo_produto ASC"):    # CADA LINHA É GUARDADA EM UMA VARIÁVEL ROW
        desc_descripto = descriptografar(row[2])    # DESCRIPTOGRAFA A TERCEIRA COLUNA DA TABELA (DESC)
        print(Fore.BLUE, row[0], Fore.LIGHTMAGENTA_EX, row[1], Fore.YELLOW, desc_descripto, Fore.RED, row[3], Fore.CYAN, row[4], Fore.LIGHTBLACK_EX, row[5],Fore.MAGENTA, row[6], Fore.LIGHTGREEN_EX, row[7])
    print(Fore.RESET)

def alterar():
    # CONSULTA DA TABELA
    print(f'''{Fore.GREEN}
================================================
     Aqui estão os produtos já cadastrados:
================================================
{Fore.BLUE}CÓD. {Fore.GREEN}| {Fore.LIGHTMAGENTA_EX}NOME {Fore.GREEN}| {Fore.YELLOW}DESCRIÇÃO {Fore.GREEN}| {Fore.RED}CP {Fore.GREEN}| {Fore.CYAN}CF {Fore.GREEN}| {Fore.LIGHTBLACK_EX}CV {Fore.GREEN}| {Fore.MAGENTA}IV {Fore.GREEN}| {Fore.LIGHTGREEN_EX}ML
{Fore.RESET}''')
    for row in cursor.execute("SELECT * FROM produtos ORDER BY codigo_produto ASC"):
        desc_descripto = descriptografar(row[2])    # DESCRIPTOGRAFA A TERCEIRA COLUNA PARA CONSULTA DA TABELA
        print(Fore.BLUE, row[0], Fore.LIGHTMAGENTA_EX, row[1], Fore.YELLOW, desc_descripto, Fore.RED, row[3], Fore.CYAN, row[4], Fore.LIGHTBLACK_EX, row[5],Fore.MAGENTA, row[6], Fore.LIGHTGREEN_EX, row[7])
    print(Fore.RESET)

    codAlterar = int(input("Digite o código do produto que deseja alterar: ")) # USUÁRIO ESCOLHE O ID DO PRODUTO PARA ALTERAR

    print(Fore.RED + '''
================================================
              Alterar Produto
================================================
    ''')
    # CÓDIGO É O MESMO QUE O QUE O USUÁRIO ESCOLHEU PARA ALTERAR
    nome = input("Digite o novo nome do produto: ")
    descricaoEscrita = input("Digite a descrição do produto: ")
    cp = float(input("Digite o novo custo do produto: "))
    cf = float(input("Digite o novo custo fixo/administrativo: "))
    cv = float(input("Digite o novo valor da comissão de vendas: "))
    iv = float(input("Digite o novo valor do imposto sobre o produto: "))
    ml = float(input("Digite o novo valor da rentabilidade: "))
    print(Fore.RESET)

    cursor.execute(f"""
                    UPDATE produtos
                    SET codigo_produto = {codAlterar}, nome_produto = '{nome}', Descrição_produto = '{criptografia(descricaoEscrita)}', custo_produto = {cp}, custo_fixo = {cf}, comissão_vendas = {cv}, impostos = {iv}, rentabilidade = {ml}
                    WHERE codigo_produto = {codAlterar}
                    """)    # USA A FUNÇÃO UPDATE PARA SOBRESCREVER AS INFORMAÇÕES DA LINHA QUE CONTÉM O CÓDIGO_PRODUTO IGUAL AO CÓDIGO QUE O USUÁRIO QUIS ALTERAR
    cursor.execute("COMMIT")    # ATUALIZA O BD

    print(Fore.LIGHTMAGENTA_EX + "Produto alterado com sucesso!" + Fore.RESET)

def excluir():
    # CONSULTA DA TABELA
    print(f'''{Fore.GREEN}
================================================
     Aqui estão os produtos já cadastrados:
================================================
{Fore.BLUE}CÓD. {Fore.GREEN}| {Fore.LIGHTMAGENTA_EX}NOME {Fore.GREEN}| {Fore.YELLOW}DESCRIÇÃO {Fore.GREEN}| {Fore.RED}CP {Fore.GREEN}| {Fore.CYAN}CF {Fore.GREEN}| {Fore.LIGHTBLACK_EX}CV {Fore.GREEN}| {Fore.MAGENTA}IV {Fore.GREEN}| {Fore.LIGHTGREEN_EX}ML
{Fore.RESET}''')
    for row in cursor.execute("SELECT * FROM produtos ORDER BY codigo_produto ASC"):
        desc_descripto = descriptografar(row[2])
        print(Fore.BLUE, row[0], Fore.LIGHTMAGENTA_EX, row[1], Fore.YELLOW, desc_descripto, Fore.RED, row[3], Fore.CYAN, row[4], Fore.LIGHTBLACK_EX, row[5],Fore.MAGENTA, row[6], Fore.LIGHTGREEN_EX, row[7])
    print(Fore.RESET)

    codExcluir = int(input("Digite o código do produto que deseja excluir: "))  # PERGUNTA QUAL O CÓDIGO DO PRODUTO QUE O USUÁRIO DESEJA EXCLUIR

    cursor.execute(f"""
                    DELETE FROM produtos WHERE codigo_produto = {codExcluir}
                    """)    # USA A FUNÇÃO DELETE PARA EXCLUIR A LINHA A QUAL CONTÉM O CÓDIGO QUE O USUÁRIO ESCOLHEU
    cursor.execute("COMMIT")    # ATUALIZA O BD
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
    # MOSTRA O PREÇO DE VENDA E CÁLCULO DE LUCRO DE CADA LINHA DO BANCO
    cursor.execute('SELECT * FROM produtos ORDER BY codigo_produto ASC')
    for row in cursor:
        nome = row[1]
        cp = row[3]
        cf = row[4]
        cv = row[5]
        iv = row[6]
        ml = row[7]

        PV=(cp/(1-((cf+cv+iv+ml)/100)))

        print(Fore.YELLOW)
        desc_descripto = descriptografar(row[2])
        print(Fore.BLUE, row[0], Fore.LIGHTMAGENTA_EX, row[1], Fore.YELLOW, desc_descripto, Fore.RED, row[3], Fore.CYAN, row[4], Fore.LIGHTBLACK_EX, row[5],Fore.MAGENTA, row[6], Fore.LIGHTGREEN_EX, row[7])
        print(Fore.RESET)
        print(f'''
    Descrição ----------------- Valor - % 
    A. Preço de venda            {round(PV,2)}   100%
    '''+Fore.BLUE+'''B. '''+Fore.RESET+f'''Custo de Aquisição        {round(cp,2)}   {round(((cp*100)/PV),2)}%
    C. Receita Bruta             {round((PV-cp),2)}  {round((100-(cp*100)/PV),2)}% 
    '''+Fore.CYAN+'''D. '''+Fore.RESET+f'''Custo fixo/Administrativo {round((PV*(cf/100)),2)}  {cf}%
    '''+Fore.LIGHTBLACK_EX+'''E. '''+Fore.RESET+f'''Comisão de vendas         {round(((cv/100)*PV),2)}  {cv}% 
    '''+Fore.MAGENTA+'''F. '''+Fore.RESET+f'''Impostos                  {round(PV*(iv/100),2)}  {iv}% 
    G. Outros custos             {round(((PV*(cf/100))+((cv/100)*PV)+((iv/100)*PV)),2)}  {cf+cv+iv}%
    '''+Fore.LIGHTGREEN_EX+'''H. '''+Fore.RESET+f'''Rentabilidade             {round((PV-cp)-((PV*(cf/100))+((cv/100)*PV)+((iv/100)*PV)),2)}  {round(((100-(cp*100)/PV) -(cf+cv+iv)),2)}%\n
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