import os
import re
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Garante que emojis/acentos apareçam no terminal do Windows (evita UnicodeError)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ==========================================
# CONFIGURAÇÕES (PERSONALIZE AQUI)
# ==========================================
# Por padrão vigia a pasta "Pasta monitorada" que fica ao lado desta,
# dentro de "N2- Marcos e Yan". Pode trocar por um caminho fixo se quiser.
BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_PARA_MONITORAR = os.path.abspath(os.path.join(BASE, "..", "Pasta monitorada"))

# A "bandeira": o sabor que o monitor procura. Ao encontrar, ele revela o
# código de cor RGB (hexadecimal) que estiver escrito na mesma linha.
SABOR_ALVO = "Pizza de Peperoni"

ARQUIVO_LOG = "resultados.txt"
EXTENSOES_SUPORTADAS = (".txt", ".log", ".csv", ".md", ".json", ".pdf", ".docx")

# Qualquer código hex de cor no formato #RRGGBB (ou #RGB)
HEX_RE = re.compile(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b")

# ==========================================
# LOGGING
# ==========================================
logging.basicConfig(
    filename=ARQUIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8",
)


def ler_texto(caminho):
    """Extrai texto de .txt/.pdf/.docx e similares. Retorna '' se não conseguir."""
    ext = os.path.splitext(caminho)[1].lower()

    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(caminho)
            return "\n".join((p.extract_text() or "") for p in reader.pages)
        except Exception as e:
            logging.error(f"Falha ao ler PDF {caminho}: {e}")
            return ""

    if ext == ".docx":
        try:
            import docx
            doc = docx.Document(caminho)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            logging.error(f"Falha ao ler DOCX {caminho}: {e}")
            return ""

    # texto puro
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        logging.error(f"Falha ao ler {caminho}: {e}")
        return ""


def procurar_termos(caminho):
    """Procura o SABOR_ALVO e, na mesma linha, extrai o código de cor RGB."""
    conteudo = ler_texto(caminho)
    if not conteudo:
        return

    for linha in conteudo.splitlines():
        if SABOR_ALVO.lower() in linha.lower():
            cor = HEX_RE.search(linha)
            codigo = cor.group(0) if cor else "(nenhum código de cor na linha)"
            msg = (f"[BANDEIRA] '{SABOR_ALVO}' encontrado em: {caminho} "
                   f"| código de cor RGB: {codigo}")
            print("🎯 " + msg)
            logging.info(msg)


class MonitorHandler(FileSystemEventHandler):
    def _tratar(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(EXTENSOES_SUPORTADAS):
            # pequena espera: o arquivo pode ainda estar sendo gravado
            time.sleep(0.5)
            procurar_termos(event.src_path)

    def on_created(self, event):
        self._tratar(event)

    def on_modified(self, event):
        self._tratar(event)


def varredura_inicial(pasta):
    """Procura nos arquivos que JÁ existem na pasta ao iniciar."""
    for raiz, _, arquivos in os.walk(pasta):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            if caminho.lower().endswith(EXTENSOES_SUPORTADAS):
                procurar_termos(caminho)


def iniciar(pasta):
    varredura_inicial(pasta)

    handler = MonitorHandler()
    observer = Observer()
    observer.schedule(handler, pasta, recursive=True)
    observer.start()
    print(f"✅ Monitorando: {pasta}")
    print(f"🔎 Procurando pela bandeira: {SABOR_ALVO}")
    print("🛑 Ctrl+C para parar.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n⏹️ Encerrado.")
    observer.join()


if __name__ == "__main__":
    if not os.path.exists(PASTA_PARA_MONITORAR):
        print(f"❌ Pasta não encontrada: {PASTA_PARA_MONITORAR}")
        raise SystemExit(1)
    iniciar(PASTA_PARA_MONITORAR)
