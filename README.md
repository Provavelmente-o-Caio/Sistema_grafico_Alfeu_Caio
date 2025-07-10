# Sistema Gráfico Alfeu Caio

Um sistema básico de computação gráfica 3D implementado em Python utilizando PyQt6.

## Descrição

Este sistema implementa conceitos fundamentais de computação gráfica 3D, incluindo:

### Funcionalidades Básicas
- Implemente uma classe Ponto3D capaz de realizar as 3 transformações básicas.
- Implemente uma Classe Objeto3D para representar um Modelo de Arame com as seguintes características:
  - Possui uma lista de segmentos de reta constituídos por um par de Pontos3D.
  - É capaz de realizar as 3 operações básicas e também a rotação em torno de um eixo arbitrário.
- Implemente as operações de navegação da window no espaço 3D.
- Implemente o que foi visto hoje sobre Projeção Paralela Ortogonal.
- O primeiro ponto pode ser o VRP.
- Lembre-se que ao final do algoritmo o VPN deve ser (0, 0, 1), ou seja, paralelo ao eixo Z.

### Superfícies Bicúbicas
O sistema suporta três tipos de superfícies bicúbicas:

#### 1. Superfícies Bézier (4x4)
Superfícies paramétricas utilizando funções de base de Bézier com 16 pontos de controle em uma grade 4x4.

#### 2. Superfícies B-Spline (4x4)
Superfícies suaves utilizando funções de base B-spline com 16 pontos de controle em uma grade 4x4.

#### 3. Superfícies B-Spline com Diferenças Adiante (4x4 até 20x20)
**Nova funcionalidade implementada:** Superfícies bicúbicas B-spline utilizando o Método das Diferenças Adiante (Forward Differences) para geração eficiente do desenho.

**Características especiais:**
- Suporte para matrizes de pontos de controle de 4x4 até 20x20
- Subdivisão automática em submatrizes 4x4 para processamento
- Algoritmo otimizado baseado no método de Forward Differences de Foley & van Dam
- Formato de entrada flexível para definição de superfícies complexas

## Tipos de Objetos Suportados

### Objetos 2D
- **Pontos**: Elementos básicos no plano
- **Linhas**: Segmentos de reta definidos por dois pontos
- **Polígonos**: Formas fechadas com três ou mais vértices
- **Curvas Bézier**: Curvas paramétricas suaves
- **Curvas B-Spline**: Curvas suaves com controle local

### Objetos 3D
- **Polígonos 3D**: Modelos de arame tridimensionais
- **Superfícies Bézier**: Superfícies paramétricas bicúbicas
- **Superfícies B-Spline**: Superfícies suaves bicúbicas
- **Superfícies B-Spline FD**: Superfícies com Forward Differences (4x4 a 20x20)

## Exemplos de Uso (Baseados nos Objetos de Demonstração)

### Objetos 2D

#### Pontos
Exemplo simples de ponto na origem:
```
(0, 0)
```

#### Linhas
Linha diagonal que vai do quadrante inferior esquerdo ao superior direito:
```
(-5, -5), (5, 5)
```

#### Polígonos
Triângulo com preenchimento, posicionado acima da origem:
```
(0, 0), (5, 8), (-5, 8)
```

Quadrado centrado na origem:
```
(-5, -5), (5, -5), (5, 5), (-5, 5)
```

#### Curvas Bézier Contínuas
Exemplo de curva com múltiplos segmentos garantindo continuidade G0:
```
(0, 0), (2, 2), (4, -2), (6, 0), (6, 0), (8, 2), (10, -2), (12, 0), (12, 0), (14, 2), (16, -2), (18, 0)
```
**Nota**: Os pontos repetidos garantem a continuidade entre segmentos.

#### Curvas B-Spline
Exemplo de curva suave com 5 pontos de controle:
```
(-10, 0), (-5, 10), (0, -10), (5, 10), (10, 0)
```

### Objetos 3D

#### Cubo/Paralelepípedo
Exemplo de cubo básico:
```
Pontos: (-5, -5, 0), (5, -5, 0), (5, 5, 0), (-5, 5, 0), (-5, -5, 5), (5, -5, 5), (5, 5, 5), (-5, 5, 5)
Arestas: (0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7)
```

#### Prisma Hexagonal
Exemplo complexo de polígono 3D com formato hexagonal:
```python
# Pontos gerados matematicamente para um hexágono regular
center = (0, 0)
radius = 4
height = 4

# Base inferior e superior
for z in [-height/2, height/2]:
    for i in range(6):
        angle = 2 * math.pi * i / 6
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append(Point3D((x, y, z)))

# Arestas conectando as faces
edges = []
for i in range(6):
    # Arestas da face superior
    edges.append((i, (i + 1) % 6))
    # Arestas da face inferior
    edges.append((i + 6, ((i + 1) % 6) + 6))
    # Arestas verticais conectando as faces
    edges.append((i, i + 6))
```

### Superfícies 3D

#### Superfície Bézier (4x4)
Exemplo com função matemática senoidal para criar ondulações:
```python
# Matriz 4x4 de pontos de controle
bezier_control_points = []
for i in range(4):
    row = []
    for j in range(4):
        x = (j - 1.5) * 3
        y = (i - 1.5) * 3
        z = np.sin(j * np.pi / 3) * np.cos(i * np.pi / 3) * 2
        row.append(Point3D([(x, y, z)]))
    bezier_control_points.append(row)
```

Formato de entrada manual equivalente:
```
(-4.5,-4.5,0),(1.5,-4.5,1.732),(-1.5,-4.5,-1.732),(4.5,-4.5,0);(-4.5,-1.5,0),(-1.5,-1.5,0.866),(1.5,-1.5,-0.866),(4.5,-1.5,0);(-4.5,1.5,0),(-1.5,1.5,-0.866),(1.5,1.5,0.866),(4.5,1.5,0);(-4.5,4.5,0),(-1.5,4.5,-1.732),(1.5,4.5,1.732),(4.5,4.5,0)
```

#### Superfície B-Spline FD (Forward Differences)
Exemplo 5x5 com função matemática complexa criando padrões de ondas:
```python
# Matriz 5x5 de pontos de controle
bspline_fd_control_points = []
for i in range(5):
    row = []
    for j in range(5):
        x = (j - 2) * 2.5
        y = (i - 2) * 2.5
        z = np.sin(j * np.pi / 4) * np.cos(i * np.pi / 4) * 1.5 + \
            0.3 * np.sin(j * np.pi / 2) * np.sin(i * np.pi / 2)
        row.append(Point3D([(x, y, z)]))
    bspline_fd_control_points.append(row)
```

Formato de entrada manual equivalente:
```
(-5,-5,-1.061),(-2.5,-5,-1.5),(0,-5,-1.061),(2.5,-5,-1.5),(5,-5,-1.061);(-5,-2.5,-0.75),(-2.5,-2.5,-1.061),(0,-2.5,-0.75),(2.5,-2.5,-1.061),(5,-2.5,-0.75);(-5,0,1.061),(-2.5,0,1.5),(0,0,1.061),(2.5,0,1.5),(5,0,1.061);(-5,2.5,0.75),(-2.5,2.5,1.061),(0,2.5,0.75),(2.5,2.5,1.061),(5,2.5,0.75);(-5,5,1.061),(-2.5,5,1.5),(0,5,1.061),(2.5,5,1.5),(5,5,1.061)
```

#### Exemplos de Superfícies Variadas

**Superfície ondulada simples (4x4):**
```
(0,0,0),(1,0,1),(2,0,1),(3,0,0);(0,1,1),(1,1,2),(2,1,2),(3,1,1);(0,2,1),(1,2,2),(2,2,2),(3,2,1);(0,3,0),(1,3,1),(2,3,1),(3,3,0)
```

**Superfície em forma de sela (5x5):**
```
(-2,-2,4),(-1,-2,1),(0,-2,0),(1,-2,1),(2,-2,4);(-2,-1,1),(-1,-1,0.25),(0,-1,0),(1,-1,0.25),(2,-1,1);(-2,0,0),(-1,0,0),(0,0,0),(1,0,0),(2,0,0);(-2,1,1),(-1,1,0.25),(0,1,0),(1,1,0.25),(2,1,1);(-2,2,4),(-1,2,1),(0,2,0),(1,2,1),(2,2,4)
```

**Superfície cilíndrica (6x4):**
```
(0,0,0),(2,0,0),(4,0,0),(6,0,0);(0,1,2),(2,1,3),(4,1,3),(6,1,2);(0,2,3),(2,2,4),(4,2,4),(6,2,3);(0,3,3),(2,3,4),(4,3,4),(6,3,3);(0,4,2),(2,4,3),(4,4,3),(6,4,2);(0,5,0),(2,5,0),(4,5,0),(6,5,0)
```

## Transformações Geométricas

### Translação
A translação move objetos adicionando valores às suas coordenadas.
Exemplo:
- Objeto original: `[(1, 1, 0)]`
- Parâmetros: `dx = -3`, `dy = 4`, `dz = 2`
- Nova posição: `[(-2, 5, 2)]`

### Escala
A transformação de escala altera o tamanho dos objetos.
Exemplo:
- Objeto original: `[(2, 3, 1)]`
- Parâmetros: `sx = 2`, `sy = 3`, `sz = 1.5`
- Nova forma: `[(4, 9, 1.5)]`

### Rotação
Rotação 3D utilizando ângulos de Euler para os eixos X, Y e Z.
- **Rotação em torno do centro**: Rotaciona o objeto em torno de seu centro geométrico
- **Rotação em torno de ponto arbitrário**: Permite especificar um ponto customizado como centro de rotação

## Projeções 3D

### Projeção Paralela Ortogonal
Projeta objetos 3D mantendo as proporções, ideal para visualização técnica.

### Projeção Perspectiva
Simula a visão humana com ponto de fuga, criando efeito de profundidade realista.

## Navegação 3D

### Modos de Movimento
- **Modo Mover**: Translação da câmera no espaço 3D
- **Modo Rotação**: Rotação da câmera para diferentes ângulos de visualização

### Controles
- **Setas direcionais**: Movimento horizontal e vertical
- **↥/↧**: Movimento para frente/trás no eixo Z
- **Zoom In/Out**: Aproxima ou afasta a visualização
- **Rotação da Window**: Rotação manual com ângulo específico

## Algoritmos de Recorte (Clipping)

### Para Linhas
- **Cohen-Sutherland**: Algoritmo clássico para recorte de linhas
- **Liang-Barsky**: Algoritmo parametrizado para recorte eficiente

### Para Polígonos
- **Sutherland-Hodgman**: Recorte de polígonos contra janela retangular

## Formato de Arquivos

### Importação/Exportação OBJ
O sistema suporta arquivos Wavefront OBJ para:
- Importação de modelos externos
- Exportação de objetos criados
- Preservação de materiais e cores

### Exemplo de arquivo OBJ exportado:
```obj
# Sistema Gráfico Alfeu e Caio
mtllib material.mtl

o Surface_BSpline_FD
v 0.000000 0.000000 0.000000
v 1.000000 0.000000 1.000000
v 2.000000 0.000000 1.000000
v 3.000000 0.000000 0.000000
# ... mais vértices
usemtl darkCyan
# B-Spline FD surface - 5x5 control points
```

## Como Usar

### Criando Objetos
1. Selecione o tipo de objeto no dropdown
2. Digite um nome único para o objeto
3. Insira as coordenadas no formato apropriado
4. Para objetos 3D, adicione também as arestas se necessário
5. Escolha a cor e configure preenchimento se desejado
6. Clique em "Add Object"

### Transformações
1. Selecione objeto(s) na lista
2. Clique em "Open Transformations"
3. Configure os parâmetros desejados
4. Aplique a transformação

### Navegação
- Use os controles de navegação na barra lateral
- Alterne entre modo "Move" e "Rotate"
- Configure algoritmos de clipping e projeção

## Recursos Avançados

### Forward Differences para Superfícies
- Implementação otimizada do algoritmo de Foley & van Dam
- Correção dos erros conhecidos do algoritmo original
- Suporte para matrizes grandes com subdivisão automática
- Renderização eficiente de superfícies complexas

### Verificação de Continuidade em Curvas
O sistema automaticamente verifica a continuidade G0 em curvas Bézier, alertando sobre descontinuidades:
```
Found discontinuous points: (6, 0), (7, 1)
```

### Visualização de Pontos de Controle
- Opção para mostrar/ocultar pontos de controle de curvas
- Facilita a edição e compreensão da geometria
- Pontos de controle aparecem em magenta quando habilitados

### Sistema de Cores Avançado
- Cores predefinidas para cada tipo de objeto:
  - Pontos: Vermelho
  - Linhas: Verde
  - Polígonos: Azul
  - Curvas Bézier: Laranja
  - Curvas B-Spline: Roxo
  - Objetos 3D: Ciano
  - Superfícies Bézier: Magenta
  - Superfícies B-Spline FD: Ciano Escuro

## Objetos de Demonstração Incluídos

O sistema carrega automaticamente os seguintes objetos para demonstração:

1. **Dot Example**: Ponto vermelho na origem
2. **Line Example**: Linha verde diagonal
3. **Triangle Example**: Triângulo azul preenchido
4. **Square Example**: Cubo ciano em wireframe
5. **Continuous Curve**: Curva Bézier laranja com múltiplos segmentos
6. **B-Spline Example**: Curva B-spline roxa ondulada
7. **Hexagonal Prism**: Prisma hexagonal vermelho
8. **Bézier Surface Example**: Superfície Bézier magenta ondulada
9. **B-Spline FD Surface Example**: Superfície B-Spline FD ciano escuro com padrão complexo

## Uso de IA na Implementação

Para essa entrega não foi feito uso significativo de IA.