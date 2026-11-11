# N2 — Marcos e Yan

Trabalho da disciplina **Segurança da Informação (2026)**.

Demonstração **didática** de dois conceitos juntos:

1. **Coleta de dados** — um "Jogo da Velha" que, antes de liberar o jogo, pede
   um login (código + senha) e grava o que foi digitado num arquivo. Serve para
   mostrar como um programa aparentemente inofensivo pode registrar dados.
2. **Monitoramento de pasta ("bandeira")** — um script que vigia uma pasta em
   tempo real e, ao encontrar o sabor **"Pizza de Peperoni"** dentro de um
   arquivo, revela o **código de cor RGB** escrito ao lado dele.

---

## Estrutura das pastas

```
N2- Marcos e Yan/
├── Codigo e Scripts/     → todo o código-fonte, scripts e dependências
│   ├── tic_tac_toe_simulacao.py   (o jogo + tela de login)
│   ├── monitor_bandeira.py        (o monitor da pasta)
│   ├── requirements.txt
│   ├── jogo_da_velha.ico
│   └── README.md                  (instruções técnicas detalhadas)
│
├── Jogo da Velha/        → apenas o executável pronto
│   └── Jogo da Velha.exe
│
└── Pasta monitorada/     → a pasta vigiada pelo monitor
    └── sabores.txt        (cardápio de pizzas + código de cor de cada uma)
```

---

## Como usar

### Jogar (sem precisar de Python)
Entre na pasta **`Jogo da Velha`** e dê dois cliques em **`Jogo da Velha.exe`**.
A tela de login aparece; preencha os dois campos (agora aceita **qualquer
caractere**, inclusive símbolos) e clique em **Entrar e jogar**. O que foi
digitado é salvo num `acessos.txt` criado ao lado do executável.

### Rodar o monitor da "bandeira"
O monitor já vem apontado para a pasta **`Pasta monitorada`** (ao lado dele).
Pelo terminal, dentro de **`Codigo e Scripts`**:

```bash
pip install -r requirements.txt
python monitor_bandeira.py
```

Ele faz uma varredura inicial e fica vigiando. Ao encontrar
**"Pizza de Peperoni"** no `sabores.txt`, mostra no terminal e grava em
`resultados.txt`:

```
🎯 [BANDEIRA] 'Pizza de Peperoni' encontrado em: ...\sabores.txt | código de cor RGB: #FF6347
```

> Os detalhes técnicos (como funciona cada script, como recompilar o `.exe`,
> como mudar o sabor-alvo etc.) estão no **README dentro de `Codigo e Scripts`**.

---

## Rodar em qualquer PC / clonar o repositório

Os caminhos são **relativos à própria pasta**, então basta manter as três
subpastas juntas, do jeito que estão. Depois de clonar/copiar:

- **Só jogar (Windows, sem instalar nada):** abra `Jogo da Velha/Jogo da Velha.exe`.
  O `.exe` já traz o Python embutido. ⚠️ É um executável **Windows** — em
  Mac/Linux use o script `.py`.
- **Rodar pelo código (qualquer sistema com Python 3.8+):**
  ```bash
  cd "Codigo e Scripts"
  pip install -r requirements.txt
  python tic_tac_toe_simulacao.py   # o jogo
  python monitor_bandeira.py        # o monitor
  ```

> **Importante:** não separe as pastas. O jogo lê a cor em
> `../Pasta monitorada/sabores.txt` e o monitor vigia essa mesma pasta; se elas
> não estiverem lado a lado, o jogo grava `cor=indisponivel`.
>
> Os arquivos gerados em execução (`acessos.txt`, `resultados.txt`) e caches do
> Python estão no `.gitignore`, então não vão para o repositório.

---

## Observação ética

Projeto de **demonstração de conceito** para estudo. Coletar dados reais,
senhas ou informações de terceiros sem autorização é crime no Brasil
(Lei 12.737/2012, art. 154-A do Código Penal). A proposta aqui é o contrário:
entender o mecanismo para **reconhecer e se defender** dessas técnicas.
