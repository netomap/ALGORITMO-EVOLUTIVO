# ALGORITMO EVOLUTIVO

- Este repositório mostra o desenvolvimento de um algoritmo evolutivo, onde é criado um jogo muito simples de "ping-pong" e os indivíduos devem rebater a bola.

- O objetivo desses indivíduos é rebater a bola indefinidademente. Para isso os indivíduos são dotados de uma rede neural que recebe as coordenadas da bola e as próprias coordenadas para tomar a decisão de movimento para esquerda ou direita.

- Quando todos os indivíduos são eliminados (quando a bola atravessa toda a tela para baixo), é criada uma nova população, onde uma parcela recebe como herança a rede neural do melhor indivíduo da última geração. Depois que cada indivíduo herda a rede neural, esta sofre uma pequena "mutação" (leve alteração nos valores de pesos e bias), para que eles não tenham movimentos idênticos.

- O processo se repete até alcançar o objetivo, que no caso foi estabelecido em rebater a bola em mais de 100 vezes.  

- Neste [link](https://medium.com/@manuel_neto/algoritmo-evolutivo-dfeff7f07999) você tem uma explicação melhor do repositório e da ideia de Algoritmos Evolutivos.  

# Resultado

- A animação abaixo mostra o resultado das simulações:

![gif](./images/gif2.gif)

- O indivíduo já passou a meta estabelecida e continua rebatendo a bola por muito tempo.