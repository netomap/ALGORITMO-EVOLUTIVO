import numpy as np

class Rede_Neural():
    
    def __init__(self, layers_config):
        self.layes_config = layers_config
        self.camadas = []
        for k in range(len(self.layes_config)-1):
            self.camadas.append(self.criar_camada(self.layes_config[k], self.layes_config[k+1]))
        self.total_de_camadas = len(self.camadas)
    
    def criar_camada(self, k_1, k):
        return (np.random.randn(k_1, k), np.random.randn(k))
    
    def forward(self, input):
        for k, (pesos, bias) in enumerate(self.camadas):
            input = np.dot(input, pesos) + bias
            input = np.maximum(input, 0) if k < self.total_de_camadas-1 else input
        return input[0]
    
    def __str__(self):
        texto = ''
        for k, (pesos, bias) in enumerate(self.camadas):
            texto += f'camada [{k}] pesos: {pesos.shape}, bias: {bias.shape}\n'
        return texto

def test1():
    # criação de rede neural e impressão
    rede = Rede_Neural([4, 3, 1])
    print (rede)
    print ('ok!')

def test2():
    # Forward test
    rede = Rede_Neural([8, 4, 1])
    input = np.random.randn(8)
    print (f'input.shape: {input.shape}')
    output = rede.forward(input)
    print (f'output: {output}')
    print ('ok!')


if __name__ == '__main__':
    test1()
    test2()