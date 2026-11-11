# Código e Scripts — N2 Marcos e Yan

Documentação técnica dos dois programas do projeto.
Requer **Python 3.8+**.

---

## Instalar dependências

```bash
pip install -r requirements.txt
```

(`watchdog` para o monitor; `pypdf` e `python-docx` para o monitor ler PDF/DOCX.)

---

## 1. `tic_tac_toe_simulacao.py` — jogo + tela de login

Janela em **Tkinter** com o título *"Jogo da Velha — Segurança da Informação 2026"*.

- Mostra aviso de **simulação / dados fictícios**.
- Pede dois campos:
  - **Código (Campo 1)** — texto normal.
  - **Senha (Campo 2)** — digitação mascarada com asteriscos (`show="*"`).
- **Aceita qualquer caractere** nos dois campos (símbolos inclusive); a única
  regra é não deixar nenhum campo vazio.
- Grava o registro em **`acessos.txt`** com data/hora, código, senha **e o
  código de cor da "bandeira"** (lido do `sabores.txt`), no formato:
  ```
  2026-11-10 23:02:28 | codigo=w3$ | senha=abc | cor=#FF6347
  ```
  A cor é a do **Pizza de Peperoni** — ou seja, o jogo captura o dado digitado
  **e** a bandeira ao mesmo tempo, mostrando os dois juntos no arquivo.
- Em seguida libera um **jogo da velha** jogável contra o computador.

Rodar pelo código:
```bash
python tic_tac_toe_simulacao.py
```

> **Onde o `acessos.txt` é salvo?** Ao lado do próprio programa (o script
> descobre a própria pasta, funcionando igual como `.py` ou como `.exe`). A cor
> é buscada em `../Pasta monitorada/sabores.txt`; se a pasta não estiver ao
> lado, grava `cor=indisponivel` e o jogo continua normalmente.

### Recompilar o executável
O `.exe` entregue está em `../Jogo da Velha/`. Para gerar de novo após editar o código:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon jogo_da_velha.ico --name "Jogo da Velha" tic_tac_toe_simulacao.py
```

O executável sai em `dist/Jogo da Velha.exe` — depois é só movê-lo para a
pasta `Jogo da Velha`.

> ⚠️ **Importante:** editar o `.py` **não** muda o `.exe` nem uma janela já
> aberta. O `.exe` é uma "foto congelada" do código no momento da compilação;
> e o Python só lê o `.py` quando o programa inicia. Para ver qualquer
> mudança: feche a janela, (recompile se usar o `.exe`) e rode de novo.

---

## 2. `monitor_bandeira.py` — monitor da pasta ("bandeira")

Vigia uma pasta em tempo real e procura a **bandeira** dentro dos arquivos.
Ao encontrar o sabor-alvo, extrai o **código de cor RGB (hexadecimal)** que
estiver na mesma linha.

Configurações no topo do arquivo:

| Variável | O que é | Valor padrão |
|---|---|---|
| `PASTA_PARA_MONITORAR` | pasta vigiada | `../Pasta monitorada` (ao lado, automático) |
| `SABOR_ALVO` | a bandeira procurada | `"Pizza de Peperoni"` |
| `ARQUIVO_LOG` | onde registra os achados | `resultados.txt` |

- Faz uma **varredura inicial** nos arquivos que já existem ao iniciar.
- Depois continua vigiando novos arquivos e alterações, em tempo real.
- Lê **.txt, .csv, .md, .json, .log, .pdf e .docx**.
- Ao achar o sabor-alvo, imprime no terminal e grava em `resultados.txt`:
  ```
  🎯 [BANDEIRA] 'Pizza de Peperoni' encontrado em: ...\sabores.txt | código de cor RGB: #FF6347
  ```

Rodar:
```bash
python monitor_bandeira.py
```

### O arquivo da pasta monitorada
Em `../Pasta monitorada/sabores.txt` há ~10 sabores, cada um com um código
de cor hexadecimal ao lado. O que o monitor revela é a cor do
**Pizza de Peperoni** (`#FF6347`). Para trocar a bandeira, mude `SABOR_ALVO`.

---

## Demonstração completa (sugestão de roteiro)

1. Abra um terminal e rode `python monitor_bandeira.py` — ele já mostra a cor
   do Pizza de Peperoni na varredura inicial.
2. Com o monitor rodando, edite/adicione uma linha com outro sabor no
   `sabores.txt` (ou troque o `SABOR_ALVO`) e salve — o monitor detecta a
   mudança na hora.
3. Para a parte de coleta, rode o jogo (`.exe` ou `.py`), faça o "login" e
   mostre o `acessos.txt` sendo preenchido.

---

## Observação ética

Demonstração de conceito para estudo. Coletar dados reais ou de terceiros sem
autorização é crime (Lei 12.737/2012, art. 154-A do Código Penal). O objetivo
é entender para **se defender**.
