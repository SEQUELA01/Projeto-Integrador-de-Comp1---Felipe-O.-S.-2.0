from math import acos, tan, pi

""" 
------------------------------------------------------------
----------------------- FUNCOES ----------------------------
------------------------------------------------------------
"""

circuitos = [
    # nome, tipo, tensão, corrente, fator de potência, frequência, data da medicao
    ["Iluminação Corredor 3", "iluminacao", 127.0, 4.2, 0.93, 60.0, "06/11/2025"],
    ["Tomadas Laboratório 1", "tomada", 127.0, 12.5, 0.85, 60.0, "06/11/2025"],
    ["Circuito 1", "iluminacao", 220.0, 8.5, 0.95, 60.0, "05/11/2025"],
    ["Motor Bomba", "motor", 220.0, 14.0, 0.78, 60.0, "05/11/2025"],
    ["Alimentador Principal", "alimentador", 220.0, 25.0, 0.92, 60.0, "05/11/2025"],
    ["Banco Tomadas Sala 2", "tomada", 127.0, 9.5, 0.88, 60.0, "03/11/2025"],
    ["Exaustor Cozinha", "motor", 220.0, 6.8, 0.81, 60.0, "06/11/2025"]
]

def resumo_eletrico():
    menor_fp = min(circuitos, key=lambda x: x[4])
    fora = [c for c in circuitos if not dentro_da_faixa(c)]
    print("Circuito com menor fator de potência:", menor_fp[0], "-", menor_fp[4])
    print("Total de circuitos fora da faixa:", len(fora))

def salvar_circuitos(nome_arquivo="circuitos.txt"):
    with open(nome_arquivo, "w") as arq:
        for c in circuitos:
            linha = f"{c[0]};{c[1]};{c[2]};{c[3]};{c[4]};{c[5]};{c[6]}\n"
            arq.write(linha)
    print("Circuitos salvos em", nome_arquivo)

def gerar_relatorio_nao_conforme(nome_arquivo="relatorio_nao_conforme.txt"):
    with open(nome_arquivo, "w") as arq:
        arq.write("RELATÓRIO DE NÃO CONFORMIDADE\n\n")
        for c in circuitos:
            if not dentro_da_faixa(c):
                arq.write(f"Circuito: {c[0]}\n")
                arq.write(
                    f"  Tipo: {c[1]} | V={c[2]} V | I={c[3]} A | fp={c[4]} | f={c[5]} Hz\n\n"
                )
    print("Relatório gerado.")

def registrar_medicao(linha):
    partes = linha.split(";")
    nome = partes[0].strip()
    medidas = {}
    for pedaco in partes[1:]:
        pedaco = pedaco.strip()
        if "=" in pedaco:
            k, v = pedaco.split("=")
            medidas[k.strip().lower()] = v.strip()

    for c in circuitos:
        if c[0] == nome:
            if "v" in medidas:
                c[2] = float(medidas["v"])
            if "i" in medidas:
                c[3] = float(medidas["i"])
            if "fp" in medidas:
                c[4] = float(medidas["fp"]) 
            if "f" in medidas:
                c[5] = float(medidas["f"])
            break

limites = {
    "iluminacao": {"i_max": 10.0, "fp_min": 0.9, "tensao_nom": 220},
    "motor": {"i_max": 20.0, "fp_min": 0.75, "tensao_nom": 220},
    "tomada": {"i_max": 15.0, "fp_min": 0.8, "tensao_nom": 127},
    "alimentador": {"i_max": 40.0, "fp_min": 0.92, "tensao_nom": 220},
}



def dentro_da_faixa(circuito):
    
    tolerancia_tensao = 0.05  # 5%, aproximadamente como a abnt manda
    
    nome, tipo, v, i, fp, f, data = circuito
    regra = limites.get(tipo, None)
    if not regra:
        return True
    if not (
        regra["tensao_nom"] * (1 - tolerancia_tensao)
        <= v
        <= regra["tensao_nom"] * (1 + tolerancia_tensao)
    ):
        return False
    if i > regra["i_max"]:
        return False
    if fp < regra["fp_min"]:
        return False
    return True

def corrigir_fator_de_potencia(nome_circuito):
    """
    Retorna o valor do capacitor necessário (em kvar)
    para corrigir o fator de potência do circuito com nome especificado.
    """
    # Buscar circuito pelo nome
    circuito = None
    for c in circuitos:
        if c[0].lower() == nome_circuito.lower():
            circuito = c
            break
    
    if circuito is None: #testa se o circuito está correto
        print("Circuito não encontrado")
        return
                
    nome, tipo, V, I, fp, f, data = circuito

    if fp >= 0.92: #testa se o fator de potencia está adequado
        print("Nenhuma correção necessaria para o cricuito", nome_circuito)
        
    else:
        # Potência ativa
        P = V * I * fp  # watts

        # Potência reativa atual
        Q_atual = P * tan(acos(fp))

        # Potência reativa desejada
        Q_alvo = P * 0.426      # P * tg(arccos(0.92))

        # Potência reativa necessária (capacitor) em kvar
        Qc = format((Q_atual - Q_alvo)/1000 , ".2f") 

        print("Para correção, use um capacitor de", Qc,"kvar")

    return 

"""
------------------------------------------------------------
--------------------------- MAIN ---------------------------
------------------------------------------------------------
"""

while True:
    print("=== Sistema de Monitoramento Elétrico ===")
    print("1 - Registrar medição")
    print("2 - Salvar circuitos")
    print("3 - Gerar relatório de não conformidade")
    print("4 - Resumo elétrico")
    print("5 - Encontrar capacitancia para corrigir fator de potencia")
    print("6 - Encerrar execução")
    opc = input("Escolha: ")
    if opc == "1":
        linha = input("Digite: Nome; V=...; I=...; fp=...; f=...\n")
        registrar_medicao(linha)
    elif opc == "2":
        salvar_circuitos()
        print("")
    elif opc == "3":
        gerar_relatorio_nao_conforme()
        print("")
    elif opc == "4":
        resumo_eletrico()
        print("")
    elif opc == "5":
        linha = input("Digite o nome do circuito:\n")
        print("")
        corrigir_fator_de_potencia(linha)
        print("")
    elif opc == "6":
        break
    else:
        print("Opção inválida\n")