import datetime
import json
import os

ARQUIVO_JSON = "Deposito.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_JSON):
        try:
            with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return dados.get("inventario", []), dados.get("lixeira", [])
        except json.JSONDecodeError:
            print("\n[ERRO] Arquivo de dados corrompido. Iniciando inventário vazio.")
            return [], []
        except Exception as e:
            print(f"\n[ERRO] Falha inesperada ao carregar: {e}")
            return [], []
    return [], []
def salvar_dados(inventario, lixeira):
    try:
        dados = {"inventario": inventario, "lixeira": lixeira}   # salva em formato legível
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"\n[ERRO] Falha ao salvar dados: {e}")

def obter_data_hora():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

inventario_deposito, lixeira = carregar_dados()  # Inicialização

while True:
    print("""
    --------------------------------------------------------
              BEM-VINDO À Fool of a Took V2.0 LTDA.  
        Especialistas em Organização de Materiais
    --------------------------------------------------------
    Comandos: 
    [ADD] Cadastrar 
    [LIST] Ver tudo 
    [MOVE] Movimentar         
    [SEARCH] Buscar 
    [RECOVER] Restaurar 
    [DELETE] Remover
    [STATS] Relatório [ABOUT] Sobre | [QUIT] Sair
    --------------------------------------------------------
    """)  #  mudei um pouco achei que ficou melhor

    comando = input("Digite um comando: ").strip().upper()

    if comando == "QUIT":
        salvar_dados(inventario_deposito, lixeira)
        print("Encerrando aplicação !......... Até logo!")
        break

    elif comando == "ABOUT":
        print("\n***[ SOBRE O SISTEMA ]***")
        print("Desenvolvedor: Gustavo Luis De Oliveira")
        print("Versão: 2.0 ")
        print("Projeto simula um app de organização de deposito ,agora com histórico salvo em json  __ #filhosdaPUC\n")

    elif comando == "ADD":
        try:
            n = int(input("Quantos equipamentos deseja cadastrar? "))
            if n < 0:
                print("[ERRO] A quantidade não pode ser negativa.")
                continue
            for i in range(n):
                print(f"\nCadastro do {i + 1}º item:")
                nome = input("Nome do equipamento: ").strip()
                qtd_ini = int(input("Quantidade inicial: "))
                if qtd_ini < 0:
                    print("[Atenção!!] Quantidade negativa detectada. Definindo como 0.")
                    qtd_ini = 0

                local = input("Local: ").strip()
                item = {
                    "nome": nome,
                    "quantidade_atual": qtd_ini,
                    "local_deposito": local,
                    "historico": []
                }
                inventario_deposito.append(item)
            salvar_dados(inventario_deposito, lixeira)
            print(f"\n{n} equipamento(s) cadastrado(s)!")
        except ValueError:
            print("[ERRO] Formato inválido. Digite números inteiros para quantidades.")

    elif comando == "LIST":
        if not inventario_deposito:
            print("\nO armazém está vazio.")
        else:
            print("\n--- ESTOQUE ATUAL ---")
            for idx, item in enumerate(inventario_deposito, start=1):
                print(f"{idx}. {item['nome']} | Local: {item['local_deposito']} | Qtd: {item['quantidade_atual']}")

    elif comando == "SEARCH":
        termo = input("Digite o termo de busca: ").strip().lower()
        resultados = [i for i in inventario_deposito if termo in i['nome'].lower()]

        if not resultados:
            print(f"\nNenhum item encontrado com '{termo}'.")
        else:
            print(f"\n--- RESULTADOS PARA '{termo}' ---")
            for item in resultados:
                print(f"- {item['nome']} | Qtd: {item['quantidade_atual']} | Local: {item['local_deposito']}")

    elif comando == "STATS":
        if not inventario_deposito:
            print("\nSem dados suficientes para estatísticas.")
        else:
            total_itens = len(inventario_deposito)
            soma_unidades = sum(item['quantidade_atual'] for item in inventario_deposito)
            maior_estoque = max(inventario_deposito, key=lambda x: x['quantidade_atual'])

            print("\n--- RELATÓRIO DE INTELIGÊNCIA ---")
            print(f"Total de produtos distintos: {total_itens}")
            print(f"Total de unidades em estoque: {soma_unidades}")
            print(f"Produto em maior volume: {maior_estoque['nome']} ({maior_estoque['quantidade_atual']} unidades)")

    elif comando == "MOVE":
        busca = input("Nome do equipamento: ").strip()
        encontrado = False
        for equipamento in inventario_deposito:
            if equipamento['nome'].lower() == busca.lower():
                encontrado = True
                try:
                    tipo = input("Tipo (1-Retirada / 2-Devolução): ")
                    qtd = int(input("Quantidade: "))
                    if qtd < 0:
                        print("[ERRO !!!] Quantidade de movimento deve ser positiva.")
                        break

                    resp = input("Responsável: ").strip()
                    tipo_txt = "RETIRADA" if tipo == "1" else "DEVOLUÇÃO"

                    if tipo == "1":
                        if qtd > equipamento['quantidade_atual']:
                            print("[ERRO !!!] Saldo insuficiente para retirada.")
                            break
                        equipamento['quantidade_atual'] -= qtd
                    else:
                        equipamento['quantidade_atual'] += qtd

                    registro = [obter_data_hora(), tipo_txt, qtd, resp]
                    equipamento['historico'].append(registro)
                    salvar_dados(inventario_deposito, lixeira)
                    print("Movimentação registrada com sucesso!")
                except ValueError:
                    print("[ERRO] Digite um número válido para a quantidade.")
        if not encontrado:
            print("Equipamento não encontrado.")

    elif comando == "DELETE":
        if not inventario_deposito:
            print("Nada para remover.")
        else:
            for idx, item in enumerate(inventario_deposito, start=1):
                print(f"{idx}. {item['nome']}")
            try:
                escolha = int(input("Número do item para remover: "))
                item_removido = inventario_deposito.pop(escolha - 1)
                lixeira.append(item_removido)
                salvar_dados(inventario_deposito, lixeira)
                print(f"'{item_removido['nome']}' movido para a lixeira.")
            except (ValueError, IndexError):
                print("[ERRO] Escolha inválida.")

    elif comando == "RECOVER":
        if not lixeira:
            print("Lixeira vazia.")
        else:
            for idx, item in enumerate(lixeira, start=1):
                print(f"{idx}. {item['nome']}")
            try:
                escolha = int(input("Número do item para recuperar: "))
                item_recuperado = lixeira.pop(escolha - 1)
                inventario_deposito.append(item_recuperado)
                salvar_dados(inventario_deposito, lixeira)
                print(f"'{item_recuperado['nome']}' restaurado!")
            except (ValueError, IndexError):
                print("[ERRO] Escolha inválida.")

    else:
        print(f"Comando '{comando}' desconhecido.")