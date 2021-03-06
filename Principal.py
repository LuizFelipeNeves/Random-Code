import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from funcoes import integral, jouletowatthora, diajuliano, formatn, diferenca, desviopadrao, erropadrao, getLoc, contarelemento, diames#, findElement, selecaolistaunica
from module import GL, binario, getir, regiao, gerarhoras, escalatemp2#, validar_diaria, GL, plotmensal, plotanual

#select = selecaolistaunica(14, listaunica)

# TODO: rede, plotmensal

def plotgeral(mes, ano, estacoes):
    opcao = 0
    diainicial = 1
    diafinal = diames(ano, mes)
    listaunica = 'ListaUnicaCompleta_201606.txt'
    header = []
    dataestacoes = []
    posicoes = []
    
    for i in range(len(estacoes)):
        try:
            sigla = estacoes[i]
            temploc = getLoc(sigla , listaunica)
            idd= temploc[0]
            lat = formatn(temploc[1])
            long = formatn(temploc[2])
            rede = temploc[3]
            readdata = lermes(diafinal, mes, ano, sigla, rede)

            latfinal = 22-0.04
            loninicial = -100
            linha = int(((latfinal - lat)/.04+0.5))
            coluna = int((long - loninicial)/.04+0.5)

            posicoes.append([linha, coluna])
            header.append([idd, lat, long])

            dataestacoes.append([sigla, rede, readdata])
        except FileNotFoundError: pass

    dataallestacoes = len(dataestacoes) * [diafinal * [24 * [None]]]
    dataallgl1x = len(dataestacoes) * [diafinal * [24 * [None]]]
    dataallgl3x = len(dataestacoes) * [diafinal * [24 * [None]]]
    dataallgl5x = len(dataestacoes) * [diafinal * [24 * [None]]]

    # Para apenas um dia, set dia inicial e final para o dia, aqui!
    for dia in range(diainicial, diafinal+1):
        anomesdia = ano * 10000 + mes * 100 + dia
        minutonovo = gerarhoras()
        minutonovo = [i * 60 for i in minutonovo]

        datagl = GLbinarios(dia, mes, ano, posicoes)
        for i in range(len(datagl)): # 1x 3x 5x
            for x in range(len(datagl[i])): # estacoes
                datagl[i][x] = escalatemp2(minutonovo, datagl[i][x])

        datasp = len(posicoes) * [24* [None]]
        for i in range(len(dataestacoes)):
            sigla = dataestacoes[i][0]
            rede = dataestacoes[i][1]
            datasp[i] = formatadia(dia, dataestacoes[i][2], rede)
            
            # datagl[0][estacao]
            gl1x = datagl[0][i] 
            gl3x = datagl[1][i]
            gl5x = datagl[2][i]
          
            
            csp = contarelemento(datasp[i])
            cgl1x = contarelemento(gl1x)
            cgl3x = contarelemento(gl3x)
            cgl5x = contarelemento(gl5x)
            
            if(cgl1x < 7): gl1x = len(gl1x) * [None]
            if(cgl3x < 7): gl3x = len(gl1x) * [None]
            if(cgl5x < 7): gl5x = len(gl1x) * [None]

            dataallgl1x[i][dia-1] = gl1x
            dataallgl3x[i][dia-1] = gl3x
            dataallgl5x[i][dia-1] = gl5x

            hora = [*range(24)]

            mediasp = integral(hora, datasp[i], len(datasp[i]))
            mediagl1x = integral(hora, gl1x, len(gl1x))
            mediagl3x = integral(hora, gl3x, len(gl3x))
            mediagl5x = integral(hora, gl5x, len(gl5x))
            
            if(csp > 7):
                dataallestacoes[i][dia-1] = datasp[i]
                figuradiaria(dia, sigla, ano, mes, opcao, hora, datasp[i], gl1x, gl3x, gl5x, mediasp, mediagl1x, mediagl3x, mediagl5x, rede)


        if(contarelemento(datagl[0][0]) > 7):
            gravardados(anomesdia, header, datasp,'SP')
            gravardados(anomesdia, header, datagl[0],'GL1X')
            gravardados(anomesdia, header, datagl[1],'GL3X')
            gravardados(anomesdia, header, datagl[2],'GL5X')
            #gerargraficodiferenca(dia, 'SOLRADNET', ano, mes, opcao, dataallestacoes, dataallgl1x) # gerar figura com dados das varias estacoes

    # salvar arquivo
    for p in range(len(dataestacoes)):
        sigla = dataestacoes[p][0]
        G = arraymedias(dataallestacoes[p])
        GLir = GL(sigla, listaunica, mes, ano)
        DIAS = [*range(1, diafinal + 1)]
        gravartexto(ano, mes, sigla, DIAS, G, GLir)

    # load tabela GL. >> plotmensal(opcao, rede, sigla, mes, ano)
    dataestacoes.clear() # limpa da memoria
    print('Concluido: ' + format(mes, '02d') + '-' + str(ano))

def arraymedias(array):
    hora = [*range(len(array))]
    newarray = []
    for i in range(len(array)):
        
        newarray.append(integral(hora, array[i], len(array[i])))
    return newarray

def checkdir(diretorio):
    try: os.stat(diretorio)
    except: os.mkdir(diretorio)

def createdir(ano, mes, sigla, rede):
    diretorio = './DADOS/IMAGENS/' + rede + '/'
    checkdir(diretorio)
    diretorio += str(ano) + '/'
    checkdir(diretorio)
    diretorio += sigla + '/'
    checkdir(diretorio)
    diretorio += format(mes, '02d') + '/'
    checkdir(diretorio)    

def figuradiaria(dia, sigla, ano, mes, opcao, hora, ir, gl1x, gl3x, gl5x, mediasp, mediagl1x, mediagl3x, mediagl5x, rede):
##    temp_da(dia, mes, ano)
##    ir_anual_gl1x[temp_day-1] = mediagl1x
##    ir_anual_gl3x[temp_day-1] = mediagl3x
##    ir_anual_gl5x[temp_day-1] = mediagl5x

##    if(mediasp != 0.0): intSP.append(formatn(mediasp))
##    else: intSP.append(None)
##
##    if(mediagl1x != 0.0): intGL1x.append(formatn(mediagl1x))
##    else: intGL1x.append(None)
##
##    intDia.append(dia)

    # Superficie
    dp_sp = str(formatn(desviopadrao(ir)))
    err_sp = str(formatn(erropadrao(dp_sp, ir)))

    # GL 1x
    dp_gl1x = str(formatn(desviopadrao(gl1x)))
    err_gl1x = str(formatn(erropadrao(dp_gl1x, gl1x)))

    # GL 3x
    dp_gl3x = str(formatn(desviopadrao(gl3x)))
    err_gl3x = str(formatn(erropadrao(dp_gl3x, gl3x)))

    # GL 5x
    dp_gl5x = str(formatn(desviopadrao(gl5x)))
    err_gl5x = str(formatn(erropadrao(dp_gl5x, gl5x)))


    labelsp = 'Média SP Min: ' + str(formatn(mediasp)) + '\n' + 'DP SP: ' + dp_sp + '\n' + 'EP SP: ' + err_sp
    labelgl1x = 'Média GL 1x: ' + str(formatn(mediagl1x)) + '\n' + 'DP GL 1x: ' + dp_gl1x + '\n' + 'EP GL 1x: ' + err_gl1x
    labelgl3x = 'Média GL 3x: ' + str(formatn(mediagl3x)) + '\n' + 'DP GL 3x: ' + dp_gl3x + '\n' + 'EP GL 3x: ' + err_gl3x
    labelgl5x = 'Média GL 5x: ' + str(formatn(mediagl5x)) + '\n' + 'DP GL 5x: ' + dp_gl5x + '\n' + 'EP GL 5x: ' + err_gl5x

    #labelsp = 'SP'
    #labelgl1x = 'GL 1X'
    #labelgl3x = 'GL 3X'
    #labelgl5x = 'GL 5X'

    ## Plot figura
    
    plt.figure(dia)
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura

    plt.plot(hora, ir, 'k-', label=labelsp) # , label=labelsp preto
    plt.plot(hora, gl1x, 'r-', label=labelgl1x)  # , label=labelgl1x GL vermelho
    plt.plot(hora, gl3x, 'g-', label=labelgl3x) # , label=labelgl3x GL 3x verde
    plt.plot(hora, gl5x, 'y-', label=labelgl5x) # , label=labelgl5x GL 5x amarelo

    plt.title('Rede ' + rede + ' - ' + sigla + str(ano) + format(mes, '02d') + format(dia, '02d') + " - Dia [" + str(diajuliano(dia, mes, ano)) + "]")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Tempo (Hora UTC)')
    plt.legend(loc='upper left')
    plt.ylim(0, 1000)
    plt.xlim(9, 23)
    plt.grid()
    createdir(ano, mes, sigla, rede)
    diretorio = './DADOS/IMAGENS/' + rede + '/' + str(ano) + '/' + sigla + '/' + format(mes, '02d')
    plt.savefig(diretorio + '/' + str(dia) + '.png')
    plt.close() #if opcao == 0: plt.close()
    plt.cla() # Limpa os eixos
    plt.clf() # Limpa a figura


def gerargraficodiferenca(dia, rede, ano, mes, opcao, dataallestacoes, dataallgl1x):
    diferencas = [] # dataallestacoes = mes inteiro
    
    # para um dia,
    for i in range(len(dataallestacoes)): # numero d estacoes
        d = diferenca(dataallgl1x[i][dia-1], dataallestacoes[i][dia-1], 0) # (a - b)-c
        diferencas.append(d)

    arraysoma = 24 * [0]
    arrayvalido = 24 * [0]
    final = 24  * [None]
    
    for i in range(len(diferencas)): # estacoes
        for x in range(len(diferencas[i])): # hora
            if(diferencas[i][x] != None):
                arraysoma[x] += diferencas[i][x]
                arrayvalido[x] += 1
                
    for i in range(24):
        if(arrayvalido[i] != 0): final[i] = arraysoma[i]/arrayvalido[i]
        
    hora = [*range(24)]
    plt.figure('difereca')
    plt.plot(hora, final, 'r-', label='Diferença')  # GL vermelho
    plt.title('Rede ' + rede + ' - Diferença - ' + str(ano) + format(mes, '02d') + format(dia, '02d') + " - Dia [" + str(diajuliano(dia, mes, ano)) + "]")
    plt.ylabel('Irradiância (Wm-2)')
    plt.xlabel('Tempo (Hora UTC)')
    plt.legend(loc='upper left')
    plt.ylim(-500, 500)
    plt.xlim(0, 25)
    plt.grid()
    createdir(ano, mes, 'Diferenca', 'Diferenca')
    diretorio = './DADOS/IMAGENS/Diferenca/' + str(ano) + '/Diferenca/' + format(mes, '02d')
    plt.savefig(diretorio + '/' + str(dia) + '.png')
    plt.close() #if opcao == 0: plt.close()
 
def GLbinarios(dia, mes, ano, estacoes):
    diretorio = './DADOS/GLGOESbin_horarios/' + str(ano) + format(mes, '02d') + '/'
    minutos = [0, 15, 30, 45]
    final1x = len(estacoes) * [len(minutos) * 24 * [None]]
    final3x = len(estacoes) * [len(minutos) * 24 * [None]]
    final5x = len(estacoes) * [len(minutos) * 24 * [None]]

    final1x = np.array(final1x)
    final3x = np.array(final3x)
    final5x = np.array(final5x)
    
    for h in range(8, 24):
        for m in range(len(minutos)):
            try:
                file = 'S11636057_' + str(ano) + format(mes, '02d') + format(dia, '02d') + format(h, '02d') + format(minutos[m], '02d') + '.bin'
                matriz = binario(diretorio + file, ano)
                for i in range(len(estacoes)):
                    lat = estacoes[i][0]
                    long = estacoes[i][1]
                    
                    p = (h) * len(minutos) + m
                    
                    final1x[i, p] = getir(matriz, lat, long, 0 , 0)
                    final3x[i, p] = regiao(matriz, lat , long, 1)
                    final5x[i, p] = regiao(matriz, lat , long, 2)
                    
            except FileNotFoundError: pass
            
    final1x = final1x.tolist()
    final3x = final3x.tolist()
    final5x = final5x.tolist()
            
    return [final1x, final3x, final5x]

def formatadia(dia, data, rede):
    temp = selectdia(dia, data, rede)
    minuto = temp[0]
    ir = temp[1]
    final = 24 * [None]
    if(contarelemento(ir) > (len(ir)/ 24) * 8):
        m = minuto[1]-minuto[0]
        media = integral(minuto, ir, 1440/m)
        if(media != None):
            final = escalatemp2(minuto, ir)            
    return final

def lermes(diafinal, mes, ano, sigla, rede):
    diainicial = 1
    if(rede == 'SOLRADNET'):
        planilha = './DADOS/' + rede + '/' + str(ano) + '/' + sigla + '/' + str(ano) + format(mes, '02d') + format(diainicial, '02d')+ '_' + str(ano) + format(mes, '02d') + format(diafinal, '02d') + '_' + sigla + '_py_ALLPOINTS.lev10'
        return pd.read_csv(planilha, header=None, sep=',', skiprows=4, usecols=[0, 1 , 3])
    if(rede == 'SONDA'):
        planilha = './DADOS/SONDA/' + str(ano) + '/' + sigla + '/' + sigla + str(ano)[-2:] + format(mes, '02d') + 'ED.csv'
        return pd.read_csv(planilha, header=None, sep=';', usecols=[*range(6)])

def selectdia(dia, data, rede):
    if(rede == 'SOLRADNET'):
        col_dia = 0
        col_min = 1
        col_ir = 3
        select_dia = format(dia, '02d') + ':' + format(mes, '02d') + ':' + str(ano)
        select_ir = data.iloc[np.where(data[col_dia].values == select_dia)]
        ir = select_ir[col_ir].values.tolist()
        minuto = select_ir[col_min].values.tolist()

        for i in range(len(minuto)):
            h = int(str(minuto[i])[:2])
            m = int(str(minuto[i])[3:5])
            minuto[i] = ((h*30) + (m/2)) / 30

            if(ir[i] > 1600 or ir[i] < 0 or np.isnan(ir[i])): ir[i] = None

        minutonovo = [i * 60 for i in minuto]
        
        return [minutonovo, ir]

    if(rede == 'SONDA'):
        if str(data.loc[0, 3]).isdigit() == True:
            # Sonda Novo
            col_dia = 2
            col_min = 3
            col_ir = 4
        else:
            # Sonda Antigo
            col_dia = 2
            col_min = 4
            col_ir = 5

        select = data.iloc[np.where(data[col_dia].values == diajuliano(dia, mes, ano))]
        minuto = select[col_min].values.tolist()


        ir = select[col_ir].values.tolist()

        for i in range(len(ir)):
            if(ir[i] > 1600 or ir[i] < 0 or np.isnan(ir[i])): ir[i]=None
            #minuto[i] = minuto[i]/60
        return [minuto, ir]

def gravardados(anomesdia, header, matriz, nome):
    diretorio = './DADOS/TXT/ANOMESDIA/' + nome
    #checkdir(diretorio)
    arquivotxt = diretorio + '/' + nome +'_'  + str(anomesdia) + '.txt'
    
    with open(arquivotxt,'w+') as f:
        for linha in range(len(header)):
            for data in header[linha]:
                f.write(str((data)) +'\t')
                
            for i in range(len(matriz[linha])-1):
                f.write(str(formatn(matriz[linha][i]))+ '\t')
            f.write(str(formatn(matriz[linha][-1]))+ '\n')

def gravartexto(ano, mes, sigla, DIAS, G, GL):
    diretorio = './DADOS/TXT/' + str(ano) + '/' + sigla
    checkdir(diretorio)
    arquivotxt = diretorio + '/' + sigla + str(ano)[-2:] + format(mes, '02d') + '.txt'
    arquivo = open(arquivotxt, 'w+', encoding="ansi")
    
    for i in range(len(G)):
        string = str(DIAS[i])+ '\t' + str(formatn(G[i]))+ '\t' + str(formatn(GL[i])) + '\n'
        arquivo.write(string)
    arquivo.close()

ano = 2018
string_estacaoes = ['Alta_Floresta', 'CUIABA-MIRANDA', 'Ji_Parana_SE', 'Rio_Branco', 'BRB', 'CPA']


mes = 7
plotgeral(mes, ano, ['Alta_Floresta'])

##for i in range(1, 12+1):
##   mes = i
##   plotgeral(mes, ano, string_estacaoes)       


#plotanual(ano, , sigla)
#plt.show()
