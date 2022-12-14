import numpy as np
from redeneural import Rede_Neural
import tkinter as tk
from random import randint, uniform

def cor_aleatoria():
    r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
    return f'#{r:02x}{g:02x}{b:02x}'

class Individuo():

    def __init__(self, id, x0, y0, w, h, deslocamento, neural_config, window_w, cor):
        self.id = id
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h
        self.deslocamento = deslocamento
        self.neural_config = neural_config
        self.rede_neural = Rede_Neural(self.neural_config)
        self.window_w = window_w
        self.cor = cor
        self.ativa = True
        self.rebatidas = 0
    
    def __str__(self):
        return str({
            'id': self.id, 'x0': self.x0, 'y0': self.y0, 
            'w': self.w, 'h': self.h, 'config': self.neural_config, 
            'cor': self.cor, 'deslocamento': self.deslocamento
        })
    
    def decidir(self, posicao_bola: tuple):
        decisao = self.rede_neural.forward(np.hstack([list(posicao_bola), self.x0, self.y0, self.x0+self.w])/1000)
        self.x0 += (-1*self.deslocamento if decisao < 0 else self.deslocamento)
        
        self.x0 = max(0, self.x0)
        self.x0 = min(self.window_w-self.w, self.x0)

    def herdar(self, nova_rede_neural):
        for k, (novos_pesos, novos_bias) in enumerate(nova_rede_neural):
            self.rede_neural.camadas[k] = (novos_pesos, novos_bias)
    
    def mutacao(self, fator=0.05):
        for k, (peso, bias) in enumerate(self.rede_neural.camadas):
            novo_peso = uniform(1-fator, 1+fator) * peso
            novo_bias = uniform(1-fator, 1+fator) * bias
            self.rede_neural.camadas[k] = (novo_peso, novo_bias)

def test1():
    individuo = Individuo(1, 45, 600, 100, 10, 10, [7, 2, 1], 600, cor_aleatoria())
    print (individuo)

def test2():
    individuo = Individuo(1, 45, 600, 100, 10, 10, [7, 2, 1], 600, cor_aleatoria())
    print (individuo.decidir((10, 20, 30, 40)))

def teste_heranca():
    print ('teste herança ===================================================')
    individuo1 = Individuo(1, 45, 600, 100, 10, 10, [2, 2, 1], 600, cor_aleatoria())
    print ('Pesos e bias da rede antes da herança.')
    print (individuo1.rede_neural.camadas)
    print (100*'=')
    individuo_nova = Individuo(1, 45, 600, 100, 10, 10, [2, 2, 1], 600, cor_aleatoria())
    print ('Pesos e bias da individuo vencedora.')
    print (individuo_nova.rede_neural.camadas)
    print (100*'=')

    individuo1.herdar(individuo_nova.rede_neural.camadas)

    print ('Pesos e bias da rede antes da herança.')
    print (individuo1.rede_neural.camadas)
    print (100*'=')

def teste_mutacao():
    individuo = Individuo(1, 45, 600, 100, 10, 10, [2, 2, 1], 600, cor_aleatoria())
    print (individuo.rede_neural.camadas)
    individuo.mutacao(fator=0.02)
    print (individuo.rede_neural.camadas)

if __name__ == '__main__':
    test1()
    test2()
    teste_mutacao()
    teste_heranca()