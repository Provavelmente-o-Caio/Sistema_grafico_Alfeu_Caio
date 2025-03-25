# Sistema Gráfico Alfeu Caio

Um sistema básico de computação gráfica 2D implementado em Python utilizando PyQt6.

## Descrição

Este sistema implementa conceitos fundamentais de computação gráfica 2D, incluindo:
- Display file (representação de pontos, linhas e polígonos)
- Transformação de viewport
- Funções de panning (navegação 2D)
- Funções de zooming

## Exemplos de Objetos

### Pontos
Para criar um ponto, insira uma única coordenada:
- [(0, 0)]

### Linhas
Para criar uma linha, insira duas coordenadas:
- (-5, -5), (5, 5)

### Polígonos
Para criar um polígono, insira três ou mais coordenadas:

Triângulo:
- (0, 0), (5, 8), (-5, 8)

Quadrado:
- (-5, -5), (5, -5), (5, 5), (-5, 5)


## Como usar

1. Selecione o tipo de objeto (Ponto, Linha ou Polígono)
2. Digite um nome para o objeto
3. Insira as coordenadas no formato adequado
4. Clique em "Add Object" para adicionar ao canvas

Use os botões de navegação para explorar o espaço:
- Setas para movimentação (panning)
- Zoom In (+) e Zoom Out (-) para aumentar e diminuir o zoom