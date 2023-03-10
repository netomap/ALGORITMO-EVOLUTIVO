import numpy as np
import tkinter as tk
from random import random, randint, uniform, choice
from time import time
from individuos import Individuo, cor_aleatoria
from logger import Logger
import pickle

INTERVAL = .001
LAST_TIME = time()
WINDOW_W, WINDOW_H = 500, 700
Y0 = 10
DIAMETER = 30
X0 = uniform(0, WINDOW_W-DIAMETER)
X1 = X0 + DIAMETER
Y1 = Y0 + DIAMETER
VX, VY = uniform(2, 3), uniform(2, 3)
DX, DY = choice([-1, 1]), 1

GET_WINNER = False
N_INDIVIDUOS = 100
Y0_INDIVIDUOS = 670
W_INDIVIDUO = 150
H_INDIVIDUO = 12
DESLOCAMENTO_INDIVIDUO = 3
GENERATION = 0
GENERATION_MAX = 1_000
MUTATION = 0.05
MAX_REBATIDAS = 100

logger = Logger('log')
variaveis = ['WINDOW_W', 'WINDOW_H', 'DIAMETER', 'N_INDIVIDUOS', 'W_INDIVIDUO', 'DESLOCAMENTO_INDIVIDUO', 'MUTATION']
logger.log_variaveis(variaveis, globals())

win = tk.Tk()
win.geometry(f'{WINDOW_W}x{WINDOW_H}+0+0')
canvas = tk.Canvas(win, width=WINDOW_W, height=WINDOW_H)
canvas.pack(fill='both')
ball = canvas.create_oval(X0, Y0, X1, Y1, fill='black')

def criar_individuos(N_INDIVIDUOS, y0_individuos, individuo_padrao = None):
    individuos = []
    for n in range(N_INDIVIDUOS):
        X0 = (WINDOW_W-W_INDIVIDUO)/2 # uniform(0, WINDOW_W-W_INDIVIDUO)
        Y0 = y0_individuos
        X1 = X0 + W_INDIVIDUO
        Y1 = Y0 + H_INDIVIDUO
        COR_ALEATORIA = cor_aleatoria()
        id_ = canvas.create_rectangle(X0, Y0, X1, Y1, fill=COR_ALEATORIA)
        
        novo_individuo = Individuo(id_, X0, Y0, W_INDIVIDUO, H_INDIVIDUO, DESLOCAMENTO_INDIVIDUO, [4+3, 4, 1], WINDOW_W, COR_ALEATORIA)
        
        if (individuo_padrao and n <= int(N_INDIVIDUOS/2)):
            novo_individuo.herdar(individuo_padrao.rede_neural.camadas)
            if (not(GET_WINNER)): novo_individuo.mutacao(fator=MUTATION)

        individuos.append(novo_individuo)
    
    return individuos

def atualizacao_dados(individuos_, salvar_pesos = False):

    rebatidas = [individuo.rebatidas for individuo in individuos_ if individuo.ativa]
    individuos_ativas = len(rebatidas)
    max_rebatidas = max(rebatidas)

    if (salvar_pesos and max_rebatidas == MAX_REBATIDAS):
        melhores = [individuo for individuo in individuos_ if (individuo.rebatidas == max_rebatidas)]
        melhor = choice(melhores)
        logger.log(
            f'N??mero m??ximo de rebatidas atingido. {max_rebatidas}',
            str(melhor.rede_neural.camadas)
        )

        arquivo = open('winner.pk', 'wb')
        pickle.dump(melhor, arquivo)
        arquivo.close()
        
    return f'Gera????o {GENERATION}, individuos ativas: {individuos_ativas}, rebatidas: {max_rebatidas}'

def novo_ciclo():
    
    canvas.moveto(ball, uniform(0, WINDOW_W-DIAMETER), 10) # move a bola para o topo da tela novamente

    if (GENERATION == 1): # SE FOR A PRIMEIRA GERA????O
        if (GET_WINNER):
            with open('winner.pk','rb') as file:
                winner = pickle.load(file)
                novas_individuos = criar_individuos(1, Y0_INDIVIDUOS, individuo_padrao=winner)
        else:
            novas_individuos = criar_individuos(N_INDIVIDUOS, Y0_INDIVIDUOS, individuo_padrao=None)

    else:
        rebatidas = []
        for cada_individuo in individuos:
            rebatidas.append(cada_individuo.rebatidas)
            canvas.delete(cada_individuo.id)
        
        total_rebatidas = max(rebatidas)

        ultimas_individuos = [b for b in individuos if b.ativa]
        melhor_individuo = choice(ultimas_individuos)
        
        novas_individuos = criar_individuos(N_INDIVIDUOS, Y0_INDIVIDUOS, individuo_padrao=melhor_individuo)

        logger.log(titulo=f'Gera????o {GENERATION}', texto=f'individuos vencedoras: {len(ultimas_individuos)}, rebatidas: {total_rebatidas}')
        if (GENERATION % 10 == 0):
            logger.log(titulo=f'Pesos da gera????o {GENERATION}', texto=str(melhor_individuo.rede_neural.camadas))

    return novas_individuos

individuos = None

while (GENERATION <= GENERATION_MAX):

    GENERATION += 1
    individuos = novo_ciclo()
    win.title(atualizacao_dados(individuos, False))
    CONDITION_GENERATION = True
    while (CONDITION_GENERATION):

        canvas.move(ball, DX*VX, DY*VY)

        position_ball = canvas.coords(ball)
        x0, y0, x1, y1 = position_ball

        # deci????es de cada individuo
        for cada_individuo in individuos:
            if (cada_individuo.ativa):
                cada_individuo.decidir(position_ball)
                canvas.moveto(cada_individuo.id, cada_individuo.x0, cada_individuo.y0)
        
        # tratamento de colis??es
        colisoes = list(canvas.find_overlapping(x0, y0, x1, y1)) # objetos que colidem com as coordenadas da bola
        if len(colisoes) > 1: # se tiver mais de uma colis??o, pois sempre ter?? uma lista de no m??nimo valor 1 (posi????o da bola)
            DY = -1*DY
            canvas.move(ball, 0, -DESLOCAMENTO_INDIVIDUO)
            for cada_individuo in individuos: # para cada individuo
                if (cada_individuo.id not in colisoes):
                    cada_individuo.ativa = False
                    canvas.delete(cada_individuo.id)
                else:
                    cada_individuo.rebatidas += 1
            
            win.title(atualizacao_dados(individuos, True))

        if (y1 >= WINDOW_H):
            CONDITION_GENERATION = False

        if (x0 <= 0 or x1 >= WINDOW_W):
            DX = -1*DX
            VY = uniform(2, 3)
        
        if (y0 <= 0):
            DY = -1*DY
            VX = uniform(2, 3)

        canvas.update()

        while (time() - LAST_TIME <= INTERVAL):
            pass
        LAST_TIME = time()