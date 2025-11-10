# Sensor de sujeira (ou aspirador guloso)
- Implemente um sensor no aspirador que permita identificar a sujeira mais próxima e então desloca-se até ela para realizar a limpeza.
- Esse sensor opera da localização do agente até os limites da sala: primeiro são avaliadas as localidades que são acessíveis com um único movimento do agente, depois aquelas acessíveis com dois movimentos, depois aquelas acessíveis com três movimentos e assim por diante.
- Dessa forma, a primeira sujeira a ser encontrada torna-se o alvo e o agente move-se até ela. No meio do caminho, o sensor é desligado e outras sujeiras não são identificadas até que a limpeza do alvo atual seja feita.
- Cuidado com a bateria!!

---

## Uma discussão sobre custo
É claro que, quando a quantidade sujeira é pouca, é muito melhor possuir um sensor em termos de minimizar o deslocamento. Porém, se a quantidade de sujeira for muito grande, o benefício do sensor pode desaparecer. Será que conseguimos pensar em um modelo simples para determinar quão melhor é possuir um sensor em função da quantidade de sujeira? Talvez pensando em um espaço contínuo?

---

# Trabalho
## Ambientes dinâmicos, defeitos e transições de fase
1. Implemente um ambiente no qual, a cada movimento do aspirador, uma nova sujeira é criada com probabilidade $p$ em um local limpo escolhido aleatoriamente.
2. Implemente um aspirador que possui um defeito e, com probabilidade p, deposite uma sujeira na sua localização atual caso esta esteja limpa.
3. Agora que a quantidade de sujeira é alterada dinamicamente, seu aspirador deve operar em um modo de patrulha. Utilize o aspirador com sensor em ambas as situações para tentar limpar totalmente a sala.
4. A depender do valor escolhido de $p$, pode ser impossível limpar totalmente a sala, o que faria seu programa rodar infinitamente. Implemente um limite de $5hw$ movimentos para o aspirador, de forma que, se ainda houver sujeira após este limite, a sala é considerada impossível de limpar.

---

- Deve haver um valor crítico pc tal que, se $p > pc$ , será sempre impossível limpar a sala.
- Para identificar esse comportamento, uma boa estratégia pode ser variar $p$ exponencialmente, fazendo, por exemplo,

    $p = 10−t,t ∈ [−3, 0]. (2)$

- Isto é apenas uma sugestão. Faça experimentos e teste diferentes intervalos para ver como o aspirador se comporta.
- Se for fazer gráficos com $p$ no eixo das abscissas, utilize a escala logarítmica para este eixo.

---

## Análise

- Escolha 5 dimensões para a sala com $h > 5$ e $w > 5$.
5- Para cada dimensão, identifique uma faixa de valores de $p$ onde seja possível ver a transição de limpeza possível para limpeza impossível em cada uma das duas situações propostas. Para cada valor de $p$ e tamanho de sala, realize 10 experimentos e calcule a média e desvio padrão dos seus resultados. Utilize no mínimo 10 valores distintos de $p$ para ilustrar suas conclusões.
- Você pode observar essa transição também analisando quantos movimentos o aspirador leva para limpar totalmente a sala (ou encerrar a execução) em função de $p$, caso tenha dificuldade em visualizar a transição de comportamento.
- Apresente seus resultados na forma de gráficos e/ou tabelas.
- Compare o desempenho do aspirador nas duas situações.
