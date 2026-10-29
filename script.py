import os


locais_cadastrados = ["Estúdio Belém", "Estúdio Arapiraca"]

servicos_cadastrados = [
    {"nome": "Design de Sobrancelhas", "preco": 45.00},
    {"nome": "Tratamento de Estrias", "preco": 120.00},
    {"nome": "Depilação do Buço", "preco": 25.00},
    {"nome": "Hidratação Labial", "preco": 50.00}
]

agenda_estudio = []


ARQUIVO_DADOS = "agenda_admin_estetica.txt"

def salvar_dados_arquivo(lista_agenda):
   
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            for item in lista_agenda:
                
                servicos_str = ",".join(item["servicos"])
                linha = f"{item['cliente']};{item['estudio']};{item['data']};{item['horario']};{servicos_str};{item['valor']};{item['fidelidade']}\n"
                arquivo.write(linha)
    except IOError:
        print("[ERRO] Falha ao salvar os dados no arquivo.")

def carregar_dados_arquivo():
    
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    
    carregados = []
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
           
            partes = linha.strip().split(";")
            if len(partes) == 7:
                cliente, estudio, data, horario, servicos_str, valor, fidelidade = partes
                
                item = {
                    "cliente": cliente,
                    "estudio": estudio,
                    "data": data,
                    "horario": horario,
                    "servicos": servicos_str.split(","),
                    "valor": float(valor),
                    "fidelidade": fidelidade == "True"
                }
                carregados.append(item)
    return carregados


def cadastrar_local():
    print("\n--- CADASTRO DE NOVO LOCAL ---")
    novo_local = input("Nome do novo local: ").strip()
    
    
    if not novo_local:
        print("[ERRO] O nome do local não pode estar vazio.")
        return
        
    locais_cadastrados.append(novo_local)
    print(f"[SUCESSO] Local '{novo_local}' cadastrado com sucesso!")


def cadastrar_servico():
    print("\n--- CADASTRO DE NOVO SERVIÇO ---")
    nome_servico = input("Nome do procedimento: ").strip()
    
    if not nome_servico:
        print("[ERRO] O nome do serviço não pode estar vazio.")
        return
        
    preco_str = input("Preço do serviço (Ex: 50.00): ").strip()
    
   
    try:
        preco = float(preco_str)
        if preco <= 0:
            print("[ERRO] O preço deve ser maior que zero.")
            return
    except ValueError:
        print("[ERRO] Valor de preço inválido.")
        return

    novo_serv = {"nome": nome_servico, "preco": preco}
    servicos_cadastrados.append(novo_serv)
    print(f"[SUCESSO] Serviço '{nome_servico}' por R$ {preco:.2f} cadastrado!")

def verificar_conflito(lista_agenda, estudio, data, horario):
    
    
    for item in lista_agenda:
        
        if item["estudio"] == estudio and item["data"] == data and item["horario"] == horario:
            return True
    return False

def selecionar_servicos():
    servicos_escolhidos = []
    total_valor = 0.0
    
    print("\n--- Catálogo de Serviços Disponíveis ---")
   
    for idx, serv in enumerate(servicos_cadastrados, start=1):
        print(f"{idx}. {serv['nome']} - R$ {serv['preco']:.2f}")
        
    
    continuando = True
    while continuando:
        escolha = input("\nDigite o número do serviço (ou '0' para encerrar): ").strip()
        
        if escolha == '0':
            continuando = False
            continue
            
        
        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(servicos_cadastrados):
                serv_selecionado = servicos_cadastrados[indice]
                servicos_escolhidos.append(serv_selecionado["nome"])
                total_valor += serv_selecionado["preco"]
                print(f"-> Adicionado: {serv_selecionado['nome']} | Subtotal: R$ {total_valor:.2f}")
            else:
                print("[ERRO] Número inválido no catálogo.")
        except ValueError:
            print("[ERRO] Digite um número válido.")
            
    return servicos_escolhidos, total_valor


def cadastrar_novo_atendimento(lista_agenda):
    print("\n--- PAINEL ADMIN: NOVO AGENDAMENTO ---")
    if not locais_cadastrados or not servicos_cadastrados:
        print("[AVISO] Cadastre locais e serviços antes de agendar.")
        return

    cliente = input("Nome da cliente: ").strip()
    if not cliente:
        print("[ERRO] O nome da cliente é obrigatório.")
        return

    print("\nSelecione o Estúdio:")
    for idx, local in enumerate(locais_cadastrados, start=1):
        print(f"{idx}. {local}")
        
    op_estudio = input("Digite o número do estúdio: ").strip()
    
    
    try:
        idx_local = int(op_estudio) - 1
        if 0 <= idx_local < len(locais_cadastrados):
            estudio_escolhido = locais_cadastrados[idx_local]
        else:
            print("[ERRO] Estúdio inválido.")
            return
    except ValueError:
        print("[ERRO] Opção inválida.")
        return

    data = input("Data do atendimento (DD/MM/AAAA): ").strip()
    horario = input("Horário (Ex: 14:00): ").strip()

    if verificar_conflito(lista_agenda, estudio_escolhido, data, horario):
        print(f"[ERRO] O {estudio_escolhido} já possui atendimento marcado para {data} às {horario}!")
        return

    servicos, valor_bruto = selecionar_servicos()
    if len(servicos) == 0:
        print("[AVISO] Nenhum serviço selecionado. Operação cancelada.")
        return

    resp_fidelidade = input("Aplicar desconto de pacote ou fidelidade (10%)? (S/N): ").strip().lower()
    fidelizado = False
    valor_final = valor_bruto

   
    if resp_fidelidade == "s":
        fidelizado = True
        valor_final = valor_bruto * 0.90
        print("[INFO] Desconto de 10% aplicado.")
    else:
        print("[INFO] Valor integral aplicado.")

    
    novo_registro = {
        "cliente": cliente,
        "estudio": estudio_escolhido,
        "data": data,
        "horario": horario,
        "servicos": servicos,
        "valor": valor_final,
        "fidelidade": fidelizado
    }
    
    lista_agenda.append(novo_registro)
    salvar_dados_arquivo(lista_agenda)
    print(f"\n[SUCESSO] Agendado para {cliente} no {estudio_escolhido} em {data} às {horario}!")

# 3. SUBPROGRAMAS: Listar agenda
def listar_agenda(lista_agenda):
    print("\n--- LISTA DE AGENDAMENTOS CADASTRADOS ---")
    if not lista_agenda:
        print("Nenhum atendimento cadastrado.")
        return

    # 2. FOR loop
    for idx, item in enumerate(lista_agenda, start=1):
        servicos_formatados = ", ".join(item["servicos"])
        status_fid = "Sim" if item["fidelidade"] else "Não"
        print(f"\n[{idx}] Cliente: {item['cliente']}")
        print(f"    Local: {item['estudio']} | Data/Hora: {item['data']} às {item['horario']}")
        print(f"    Serviços: {servicos_formatados} | Valor: R$ {item['valor']:.2f}")


def excluir_agendamento(lista_agenda):
    print("\n--- EXCLUIR AGENDAMENTO ---")
    if not lista_agenda:
        print("Não há agendamentos para excluir.")
        return

    listar_agenda(lista_agenda)
    
    escolha = input("\nDigite o número do agendamento que deseja excluir: ").strip()
    
   
    try:
        indice = int(escolha) - 1
        if 0 <= indice < len(lista_agenda):
            removido = lista_agenda.pop(indice) # 4. Remove da lista/matriz
            salvar_dados_arquivo(lista_agenda)   # 7. Atualiza o arquivo
            print(f"[SUCESSO] Atendimento da cliente '{removido['cliente']}' foi removido.")
        else:
            print("[ERRO] Número de agendamento inválido.")
    except ValueError:
        print("[ERRO] Digite um número válido.")


def atualizar_agendamento(lista_agenda):
    print("\n--- ATUALIZAR AGENDAMENTO ---")
    if not lista_agenda:
        print("Não há agendamentos para atualizar.")
        return

    listar_agenda(lista_agenda)
    
    escolha = input("\nDigite o número do agendamento que deseja atualizar: ").strip()
    
    try:
        indice = int(escolha) - 1
        if 0 <= indice < len(lista_agenda):
            item_atual = lista_agenda[indice]
            print(f"\nEditando agendamento de: {item_atual['cliente']}")
            
            novo_cliente = input(f"Novo nome da cliente [{item_atual['cliente']}]: ").strip()
          
            if novo_cliente:
                item_atual['cliente'] = novo_cliente
                
            nova_data = input(f"Nova data [{item_atual['data']}]: ").strip()
            if nova_data:
                item_atual['data'] = nova_data
                
            novo_horario = input(f"Novo horário [{item_atual['horario']}]: ").strip()
            if novo_horario:
                item_atual['horario'] = novo_horario
                
            salvar_dados_arquivo(lista_agenda) 
            print("[SUCESSO] Agendamento atualizado com sucesso!")
        else:
            print("[ERRO] Número inválido.")
    except ValueError:
        print("[ERRO] Entrada inválida.")


def iniciar_sistema():
    global agenda_estudio
    agenda_estudio = carregar_dados_arquivo()

   
    executando = True
    while executando:
        print("\n==========================================")
        print("   SISTEMA BeautyAgenda ")
        print("==========================================")
        print("1. Cadastrar Novo Local")
        print("2. Cadastrar Novo Serviço no Catálogo")
        print("3. Cadastrar Novo Agendamento")
        print("4. Listar Agendamentos")
        print("5. Atualizar Agendamento")
        print("6. Excluir Agendamento")
        print("7. Sair do Sistema")
        
        opcao = input("Escolha uma opção (1-7): ").strip()
        
        
        if opcao == "1":
            cadastrar_local()
        elif opcao == "2":
            cadastrar_servico()
        elif opcao == "3":
            cadastrar_novo_atendimento(agenda_estudio)
        elif opcao == "4":
            listar_agenda(agenda_estudio)
        elif opcao == "5":
            atualizar_agendamento(agenda_estudio)
        elif opcao == "6":
            excluir_agendamento(agenda_estudio)
        elif opcao == "7":
            print("Saindo do sistema administrativo. Bom trabalho!")
            executando = False
        else:
            print("[ERRO] Opção inválida. Digite de 1 a 7.")

if __name__ == "__main__":
    iniciar_sistema()
