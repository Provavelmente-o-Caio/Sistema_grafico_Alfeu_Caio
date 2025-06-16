# Sistema Gráfico Alfeu Caio

Um sistema básico de computação gráfica 2D implementado em Python utilizando PyQt6.

## Descrição

Este sistema implementa conceitos fundamentais de computação gráfica 3D, incluindo:
-Implemente uma classe Ponto3D capaz de realizar as 3 transformações básicas.
-Implemente uma Classe Objeto3D para representar um Modelo de Arame com as seguintes características:
  - Possui uma lista de segmentos de reta constituídos por um par de Pontos3D.
  - É capaz de realizar as 3 operações básicas e também a rotação em torno de um eixo arbitrário.
- Implemente as operações de navegação da window no espaço 3D.
- Implemente o que foi visto hoje sobre Projeção Paralela Ortogonal.
- O primeiro ponto pode ser o VRP.
- Lembre-se que ao final do algoritmo o VPN deve ser (0, 0, 1), ou seja, paralelo ao eixo Z.
## Exemplos de Objetos

### Pontos
Para criar um ponto, insira uma única coordenada:
- (0, 0)

### Linhas
Para criar uma linha, insira duas coordenadas:
- (-5, -5), (5, 5)

### Polígonos
Para criar um polígono, insira três ou mais coordenadas:

Triângulo:
- (0, 0), (5, 8), (-5, 8)

Quadrado:
- (-5, -5), (5, -5), (5, 5), (-5, 5)

## Exemplos de Transformações

### Translação
A translação consiste em adicionar (ou subtrair) valores às coordenadas dos objetos.
Exemplo:
- Objeto original: `[(1, 1)]`
- Parâmetros de translação: `dx = -3` e `dy = 4`
- Nova posição: `[(1 + (-3), 1 + 4)]` resultando em `[(-2, 5)]`
Utilize o método [`translate_objects`](ui/canvas.py#L? "translation method in Canvas") para aplicar essa transformação.

### Transformação (Escala)
A transformação (ou escala) multiplica as coordenadas para alterar o tamanho do objeto.
Exemplo:
- Objeto original: `[(2, 3)]`
- Parâmetros de escala: `sx = 2` e `sy = 3`
- Nova forma: `[(2 * 2, 3 * 3)]` resultando em `[(4, 9)]`
Esta funcionalidade é aplicada via [`transform_objects`](ui/canvas.py#L? "transformation method in Canvas").

### Rotação
A rotação utiliza funções trigonométricas para recalcular as coordenadas dos objetos.
Exemplo:
- Objeto original: `[(1, 0)]`
- Parâmetro: `angle = 90°`
- Nova posição: Aproximadamente `[(0, 1)]`
Para rotacionar objetos, utilize o método [`rotate_objects`](ui/canvas.py#L? "rotation method in Canvas").

## Como usar

1. Selecione o tipo de objeto (Ponto, Linha ou Polígono)
2. Digite um nome para o objeto
3. Insira as coordenadas no formato adequado
4. Clique em "Add Object" para adicionar ao canvas

Use os botões de navegação para explorar o espaço:
- Setas para movimentação (panning)
- Zoom In (+) e Zoom Out (-) para aumentar ou diminuir o zoom

## Uso de IA na entrega
Para essa entrega não foi feito uso significativo de IA.
