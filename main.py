from math import acos, tan, pi



"""
FUNCOES
"""

circuitos = [
    #nome, tipo, tensão, corrente, fator de potência, frequência, data da medição
    ["Circuito 1", "iluminacao", 220.0, 8.5, 0.95, 60.0, "05/11/2025"],
    ["Motor Bomba", "motor", 220.0, 14.0, 0.78, 60.0, "05/11/2025"],
    ["Alimentador Principal", "alimentador", 220.0, 25.0, 0.92, 60.0, "05/11/2025"],
    ["Banco Tomadas Sala 2", "tomada", 127.0, 9.5, 0.88, 60.0, "03/11/2025"]
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
                arq.write(f"  Tipo: {c[1]} | V={c[2]} V | I={c[3]} A | fp={c[4]} | f={c[5]} Hz\n\n")
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




tolerancia_tensao = 0.10  # 10%

def dentro_da_faixa(circuito):
    nome, tipo, v, i, fp, f, data = circuito
    regra = limites.get(tipo, None)
    if not regra:
        return True
    if not (regra["tensao_nom"] * (1 - tolerancia_tensao) <= v <= regra["tensao_nom"] * (1 + tolerancia_tensao)):
        return False
    if i > regra["i_max"]:
        return False
    if fp < regra["fp_min"]:
        return False
    return True




def corrigir_fator_de_potencia(circuitos, fp_alvo=0.9):
    """
    Recebe uma lista de circuitos no formato:
    [nome, tipo, V, I, fp, f, data]
    Retorna uma lista com sugestões de correção de fator de potência.
    """
    sugestoes = []

    for c in circuitos:
        nome, tipo, V, I, fp, f, data = c
        
        # Só processar se fp < fp_alvo
        if fp < fp_alvo:
            
            # Potência ativa
            P = V * I * fp  # watts

            # Potência reativa atual
            Q_atual = P * tan(acos(fp))

            # Potência reativa desejada (fp_alvo)
            Q_alvo = P * tan(acos(fp_alvo))

            # Potência reativa necessária (capacitor)
            Qc = Q_atual - Q_alvo  # var

            # Capacitância necessária
            omega = 2 * pi * f
            C = Qc / (V**2 * omega)  # Farads
            C_uF = C * 1e6           # microfarads

            sugestoes.append({
                "nome": nome,
                "tipo": tipo,
                "V": V,
                "I": I,
                "fp_atual": fp,
                "fp_alvo": fp_alvo,
                "P_W": round(P, 2),
                "Q_atual_VAR": round(Q_atual, 2),
                "Q_alvo_VAR": round(Q_alvo, 2),
                "Qc_necessario_VAR": round(Qc, 2),
                "C_F": C,
                "C_uF": C_uF,
                "frequencia_Hz": f,
                "data": data
            })

    return sugestoes



"""
MAIN
"""

print("=== Sistema de Monitoramento Elétrico ===")
print("1 - Registrar medição")
print("2 - Salvar circuitos")
print("3 - Gerar relatório de não conformidade")
print("4 - Resumo elétrico")
print("5 - Encontrar capacitancia para corrigir fator de potencia")
opc = input("Escolha: ")
if opc == "1":
    linha = input("Digite: Nome; V=...; I=...; fp=...; f=...\n")
    registrar_medicao(linha)
elif opc == "2":
    salvar_circuitos()
elif opc == "3":
    gerar_relatorio_nao_conforme()
elif opc == "4":
    resumo_eletrico()
elif opc == "5":
    corrigir_fator_de_potencia()
else:
    print("Opção inválida")