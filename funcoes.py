# -*- coding: utf-8 -*-

import csv
import math
import pandas as pd
import numpy as np


def jouletowatthora(valor):
    return ((valor * (10**3))/3600)

def selecaolistaunica(id, listaunica):
    lista = pd.read_csv(listaunica, sep='\t', header=None, usecols=[4 , 6, 9], encoding="latin-1")
    select = lista.iloc[np.where(lista[4].values == id)]
    select = select.iloc[np.where(select[6].values != '-999')]
    select = select.iloc[np.where(select[9].values == 'Brasil')]
    select = select[6].values.tolist()
    return select

def diames(ano, mes):
    diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]
    if(int(ano) % 4 == 0): diasmes[1] += 1
    return diasmes[int(mes)-1]

# Retorna o numero de dias de determinado mes            
def numerodiasmes(mes):
    return diasmes[mes-1]

def diajuliano(dia, mes, ano):
    diasmes = [31 , 28 , 31 , 30 , 31, 30, 31, 31, 30, 31,30, 31]
    if(int(ano) % 4 == 0): diasmes[1] += 1
    for i in range(mes-1): dia += diasmes[i]
    return dia


# Encontra um Elemento em uma Lista
def findElement(elemento, lista):
    for i in range(len(lista)):
        if(elemento == lista[i]):
            return i

# Pega o ID da Estacao	
def getID(sigla, listaunica):
    lista = pd.read_csv(listaunica, sep='\t', header=None, encoding="latin-1")
    select = lista.iloc[np.where(lista[6].values == sigla)]
    select = select[0].values.tolist()
    return select[0]

# Pega a localizacao da Estacao
def getLoc(sigla, listaunica):
    lista = pd.read_csv(listaunica, sep='\t', header=None, encoding="latin-1")
    select = lista.iloc[np.where(lista[6].values == sigla)]
    lat = select[1].values.tolist()
    long = select[2].values.tolist()
    return (lat[0], long[0])

def contarelemento(array):
    count = 0
    for i in range(len(array)):
        if(array[i] != None): count += 1
    return(count)

# Soma todos os elementos de um array
def somararray(array):
    soma = 0
    for i in range(len(array)):
        if(array[i] != None):
            soma += array[i]
    return soma

# Formata determinado numero para duas casas.    
def formatn(numero):
    if(numero == None): return -999
    else: return float("%.2f" % numero)

# Calcula o desvio padrao
def desviopadrao(array): 
    new=[]
    for i in range(len(array)):
        if(array[i] != None): new.append(array[i])

    if(len(new) != 0):
        media = np.sum(new) / len(new)
        for i in range(len(new)):
            new[i] = (new[i] - media)**2
        dp= np.sum(new) / (len(new)-1)
        dp = math.sqrt(dp)
    else: dp = 0
    return float(round(dp, 3))

def erropadrao(dsp, array):
    new=0
    for i in range(len(array)):
        if(array[i] != None): new += 1
    if(new == 0): new = 1
    final = float(dsp) / math.sqrt(new)
    return round(final, 3)

def diferenca(a, b):
    final = []
    for i in range(len(a)):
        if(a[i] != None and b[i] != None): final.append(a[i]-b[i])
        else: final.append(None)
    return final

# Media do dia, usando o metodo dos trapezios

def integral(x, y):
    i = 0
    total = 0
    ant = '-999'
    prox = '-999'
    tant = '-999'
    tprox = '-999'

    while i < len(y):
        if(i+1 < len(y)) :
            if(y[i] == None):
                if(ant == '-999'):  
                    ant = 0
                    tant = int(x[i])
            else: 
                if(ant == '-999'):  
                    ant = y[i]
                    tant = int(x[i])
                else:
                    # faz o calculo
                    prox = y[i]
                    tprox = int(x[i])

                    intervalo = tprox - tant                    
                    if(intervalo == 0): intervalo=1
                    S = (ant+prox) * intervalo / 2
                    S = S/intervalo

                    b = np.trapz([ant, prox], x=[tant, tprox])

                    #print(S, b)
                    ant = y[i]
                    tant = int(x[i])
                    total += S
                    #print(b)                 
        else:
            if(y[i] != None): 
                prox = y[i]
                tprox = int(x[i])
                #print(ant, prox, tant, tprox)
                b = np.trapz([ant, prox], x=[tant, tprox])
                total += S
            #print(b)
        i+=1
    return (total)
