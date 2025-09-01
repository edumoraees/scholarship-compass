# 📝 Exercício

## 1️⃣ Código do exercício 3 - ETL com Python

- Dado a base de dados [actors.csv](Exercicios/actors.csv) foi solicitado para fazer querys divididas em etapas neste arquivo e armazenar cada uma em um arquivo .txt.
 
### Código para resolução
 [code.py](Exercicios/code.py)

### Etapa 1

#### Apresentar o ator/atriz com maior número de filmes e a respectiva quantidade

[Resposta etapa 1](Exercicios/Etapa-1.txt)

### Etapa 2

#### Apresentar a média de receita de bilheteria bruta dos principais filmes, considerando todos os atores

[Resposta etapa 2](Exercicios/Etapa-2.txt)

### Etapa 3

#### Apresentar o ator/atriz com a maior média de receita de bilheteria bruta por filme do conjunto de dados

[Resposta etapa 3](Exercicios/Etapa-3.txt)

### Etapa 4

#### Realizar a contagem de aparições dos filmes no dataset, listando-os pela quantidade de vezes em que estão presentes. Considerando a ordem decrescente e, em segundo nível, o nome do filme.

[Resposta etapa 4](Exercicios/Etapa-4.txt)

### Etapa 5

#### Apresentar a lista dos atores ordenada pela receita bruta de bilheteria de seus filmes (coluna Total Gross), em ordem decrescente.

[Resposta etapa 5](Exercicios/Etapa-5.txt)

# 🔍 Evidências

- Algumas linhas da base de dados [actors.csv](Exercicios/actors.csv) contiam `,` no nome dos atores e gerava os dados de forma incorreta. Mas, nas linhas que ocorriam isso estavam dentro de aspas dupla, como o exemplo abaixo:

```
"Robert Downey, Jr.",3947.30 ,53,74.50 ,The Avengers,623.40
```

- Para resolver isso, utilizei a seguinte lógica:

```
def parse_csv_line(s: str):
    out, field, in_quotes, i = [], [], False, 0
    while i < len(s):
        c = s[i]
        if c == '"':
            # se estamos dentro de aspas e vier outra aspas, é escape: "" -> "
            if in_quotes and i + 1 < len(s) and s[i+1] == '"':
                field.append('"')
                i += 1
            else:
                in_quotes = not in_quotes
        elif c == ',' and not in_quotes:
            # só separa no vírgula se NÃO estiver entre aspas
            out.append(''.join(field)); field = []
        elif c not in '\r\n':
            field.append(c)
        i += 1
    out.append(''.join(field))
    return out
```
## 2️⃣ Exercícios básicos

[Comando utilizado no Ex1.](./Evidencias/Ex01Parte1.png)

[Comando utilizado no Ex2.](./Evidencias/Ex02Parte1.png)

[Comando utilizado no Ex3.](./Evidencias/Ex03Parte1.png)

[Comando utilizado no Ex4.](./Evidencias/Ex04Parte1.png)

[Comando utilizado no Ex6.](./Evidencias/Ex06Parte1.png)

[Comando utilizado no Ex7.](./Evidencias/Ex07Parte1.png)

[Comando utilizado no Ex8.](./Evidencias/Ex08Parte1.png)

[Comando utilizado no Ex9.](./Evidencias/Ex09Parte1.png)

[Comando utilizado no Ex10.](./Evidencias/Ex10Parte1.png)

[Comando utilizado no Ex12.](./Evidencias/Ex12Parte1.png)

[Comando utilizado no Ex13.](./Evidencias/Ex13Parte1.png)

[Comando utilizado no Ex14.](./Evidencias/Ex14Parte1.png)

## 3️⃣ Exercícios Avançados I 
[Comando utilizado no Ex15.](./Evidencias/Ex15Parte2.png)

[Comando utilizado no Ex16.](./Evidencias/Ex16Parte2.png)

[Comando utilizado no Ex17.](./Evidencias/Ex17Parte2.png)

[Comando utilizado no Ex18.](./Evidencias/Ex18Parte2.png)

[Comando utilizado no Ex19.](./Evidencias/Ex19Parte2.png)

## 4️⃣ Exercícios Avançados II 
[Comando utilizado no Ex20.](./Evidencias/Ex20Parte3.png)

[Comando utilizado no Ex21.](./Evidencias/Ex21Parte3.png)

[Comando utilizado no Ex22.](./Evidencias/Ex22Parte3.png)

[Comando utilizado no Ex23.](./Evidencias/Ex23Parte3.png)

[Comando utilizado no Ex25.](./Evidencias/Ex25Parte3.png)

[Comando utilizado no Ex26.](./Evidencias/Ex26Parte3.png)                                                                                                                                               

# 🏆 Certificados