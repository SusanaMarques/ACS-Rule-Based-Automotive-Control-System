#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import logging
import datetime

#leitura do ficheiro .csv para o dataframe df
df= pd.read_csv('anexo.csv')

#remove linhas duplicadas
df.drop_duplicates()

#altera o display para uma melhor percepção
#de todo o ficheiro de logs
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.width',1000)



if __name__ == "__main__":
    #criação do ficheiro de logs 
    logging.basicConfig(level=logging.DEBUG, filename="file", filemode="w",format="%(message)s")
                        
##CRIAÇÃO DAS COLUNAS ADICIONAIS DO FICHEIRO DE LOGS##

#criação de um array que determinará a estação a 
#que pertence cada linha
estacao =[]

#criação de arrays que apresentam o resultado 
#do cálculo da temperatura de conforto e da humidade 
#através da estação
temp_conforto = []
humid_conforto = []

#criação de array que apresentam o output pedido
#da temperatura e da humidade consoante os valores calculados
output_temp =[]
output_humid =[]


# calcula a estação através da data e do hemisfério em que se encontra
def estacaoo(dataa, hemisferio):
    md = dataa.month * 100 + dataa.day

    if ((md > 320) and (md < 621)):
        s = 0 #primavera
    elif ((md > 620) and (md < 923)):
        s = 1 #verao
    elif ((md > 922) and (md < 1223)):
        s = 2 #outono
    else:
        s = 3 #inverno

    if hemisferio != "norte":
        if s < 2:
            s += 2 
        else:
            s -= 2

    return s
   

for value, value1 in zip(df["dt_iso"],df["lat"]):
    datee = datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
    #calcula o hemisfério onde se encontra através da
    #coordenada altitude
    if value1 >=0: 
        hemisferio ="norte"    
    else:
        hemisferio ="sul"
    #calcula a estação
    s=estacaoo(datee,hemisferio)
    if s==0:
        est="Primavera"
    elif s==1:
        est="Verao"
    elif s==2:
        est="Outono"
    else:
        est="Inverno"
    #adiciona a estação ao array de estação criado antes
    estacao.append(est)    

#adiciona o array ao dataframe df como coluna
df["Estacao"]=estacao 

#encontrar a temperatura e a humidade adequada de
#acordo com a estação do ano e a
#noite: entre as 00:00:00 e as 06:00:00

##TEMPERATURA##
#Primavera: 23 graus / 25 (à noite)
#Verão: 26 graus / 28 (à noite)
#Outono: 20 graus  / 18 (à noite)
#Inverno: 17 graus / 15 (à noite)

##HUMIDADE##
#Primavera: 39%
#Verão: 45%
#Outono: 33 %
#Inverno: 27%

#verifica se um certo tempo se encontra
#entre um e outro tempo mencionado
def time_in_range(start, end, x):
    #return true if x is in the range [start,end]
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


#calcula o tempo de conforto e a temperatura de conforto 
#através da estação

#não faz sentido calcular a temperatura com referência
#à humidade nem vice-versa uma vez que as duas variáveis
#se interligam e ao alterarmos
#um o outro também é alterado
for val, estac in zip(df["dt_iso"],df["Estacao"]):
    time = datetime.datetime.strptime(val,"%Y-%m-%d %H:%M:%S")
    #tempo que ocorre naquela dia da data 
    timee= datetime.time(time.hour,time.minute,time.second)
    start = datetime.time(23,0,0)
    end = datetime.time(6,0,0)

    #verifica qual estação é
    if estac == "Primavera":
        #verifica se é de noite
        if time_in_range(start, end, timee):
            temp_conforto.append(25)
            humid_conforto.append(39)
        else:
            temp_conforto.append(23)
            humid_conforto.append(39)
    elif estac == "Verao":
        if time_in_range(start, end, timee):
            temp_conforto.append(28)
            humid_conforto.append(45)
        else:
            temp_conforto.append(26)
            humid_conforto.append(45)
    elif estac == "Outono":
        if time_in_range(start, end, timee):
            temp_conforto.append(18)
            humid_conforto.append(33)
        else:
            temp_conforto.append(20)
            humid_conforto.append(33)
    elif estac == "Inverno":
        if time_in_range(start, end, timee):
            temp_conforto.append(15)
            humid_conforto.append(27)
        else:
            temp_conforto.append(17)
            humid_conforto.append(27)
    
# adição dos arrays de temperatura de conforto e 
#humidade de conforto já criados e preenchidoas 
#acima ao dataframe que estamos a utilizar como colunas
df["Temp_conforto"]=temp_conforto
df["Humid_conforto"]=humid_conforto

#cálculo do output que deverá ser colocado na coluna de 
#outputs de temperatura do ficheiro logs 
for val1, val2 in zip(df["temp"],df["Temp_conforto"]):
    if val1 > val2:
        diferenca = val1-val2
        output_temperatura = "AIRCONDITIONING -{:.2f}ºC".format(diferenca)
    elif val1 < val2:
        diferenca = val2-val1
        output_temperatura = "AIRCONDITIONING +{:.2f}ºC".format(diferenca)
    else: output_temperatura = "NO NEED TO CHANGE"
    output_temp.append(output_temperatura)

#adição do array de output da temperatura ao dataframe como coluna
df["Output_Temp"]= output_temp

#cálculo do output que deverá ser colocado na coluna
#de outputs de humidade do ficheiro logs
for val1, val2 in zip(df["humidity"],df["Humid_conforto"]):
    if val1 > val2:
        diferenca = val1-val2
        output_humidade = "HUMIDIFYING -{:.2f} %".format(diferenca)
    elif val1 < val2:
        diferenca = val2-val1
        output_humidade = "HUMIDIFYING +{:.2f} %".format(diferenca)
    else: output_humidade = "NO NEED TO CHANGE"
    output_humid.append(output_humidade)

#adição  do array de output da humidade ao dataframe como coluna
df["Output_Humid"]= output_humid

#adição de todo o dataframe (toda a informação contida 
#no csv, mais toda a informação obtida neste SBR)
#ao ficheiro de logs
logging.info(df)
