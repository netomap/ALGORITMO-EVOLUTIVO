from datetime import datetime as dt
import os

class Logger():

    def __init__(self, nome_arquivo):

        self.LOGDIR = './logs'
        if (not(os.path.exists(self.LOGDIR))):
            os.mkdir(self.LOGDIR)

        tempo_criacao = dt.strftime(dt.now(), '%d_%m_%y_%H_%M_%S')
        self.nome_arquivo = f'{self.LOGDIR}/{nome_arquivo}_{tempo_criacao}.txt'
    
    def log(self, titulo, texto):
        tempo = dt.strftime(dt.now(), '%H:%M:%S')
        arquivo = open(self.nome_arquivo, 'a', encoding='utf-8')
        cabecalho_ini = f'[{tempo}] == {titulo} '
        n = 100 - len(cabecalho_ini)
        cabecalho = cabecalho_ini + n*'='
        arquivo.write(cabecalho + '\n')
        arquivo.write(str(texto) + '\n\n')
        arquivo.close()
    
    def log_variaveis(self, vetor_variaveis, _globals):
        
        texto = '\n'.join([f'{cada_variavel}={_globals[cada_variavel]}' for cada_variavel in vetor_variaveis])
        self.log('Variáveis', texto)

def test():
    import numpy as np
    logger = Logger('teste')
    logger.log('agora depuração dos melhores', 'explicação do primeiro texto')
    logger.log('vetor dos melhores pesos.', np.random.random((2, 4)))

if __name__ == '__main__':
    test()