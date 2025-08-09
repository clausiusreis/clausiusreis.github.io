# gen_index.py
import os
import sys
import argparse
import html
import urllib.parse
from datetime import datetime

IGNORE_FILES_CI = {"index.html", "index.htm"}  # não listar o próprio índice

def is_hidden(name: str) -> bool:
    return name.startswith(".")

def list_files_for_dir(dirpath: str, include_hidden: bool):
    """Retorna somente arquivos deste diretório (nomes base), filtrados e ordenados."""
    try:
        entries = os.listdir(dirpath)
    except PermissionError:
        return None

    files = []
    for name in entries:
        full = os.path.join(dirpath, name)
        if not os.path.isfile(full):
            continue
        if name.lower() in IGNORE_FILES_CI:
            continue
        if not include_hidden and is_hidden(name):
            continue
        files.append(name)

    files.sort(key=lambda s: s.lower())
    return files

def esc(s: str) -> str:
    return html.escape(s, quote=True)

def url_for_filename(name: str) -> str:
    # Link relativo ao index da própria pasta
    return urllib.parse.quote(name)

def build_html(dirpath: str, root: str, files: list):
    rel = os.path.relpath(dirpath, root)
    rel_display = "." if rel == "." else rel.replace(os.sep, "/")
    title = f"Arquivos — {rel_display}"

    if files:
        lis = "\n".join(
            f'      <li><a href="{url_for_filename(name)}" download>{esc(name)}</a></li>'
            for name in files
        )
    else:
        lis = '      <li><em>Nenhum arquivo nesta pasta.</em></li>'

    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <style>
    :root {{ --fg:#111; --muted:#666; --bg:#fff; --card:#f6f7f9; }}
    html,body{{margin:0;padding:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,"Helvetica Neue",Arial}}
    .wrap{{max-width:900px;margin:40px auto;padding:0 20px}}
    h1{{font-size:1.25rem;margin:0 0 10px}}
    .status{{color:var(--muted);margin:0 0 16px}}
    ul{{margin:0;padding-left:20px}}
    li{{margin:6px 0}}
    a{{color:#0366d6;text-decoration:none;word-break:break-all}}
    a:hover{{text-decoration:underline}}
    .crumbs{{font-size:.9rem;color:var(--muted);margin-bottom:8px}}
    .footer{{margin-top:24px;font-size:.85rem;color:var(--muted)}}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="crumbs">{esc(rel_display)}</div>
    <h1>Arquivos nesta pasta</h1>
    <p class="status">Clique para baixar.</p>
    <ul>
{lis}
    </ul>
    <div class="footer">Gerado em {esc(generated)}.</div>
  </div>
</body>
</html>
"""

def write_index(dirpath: str, html_str: str):
    out = os.path.join(dirpath, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html_str)

def main():
    ap = argparse.ArgumentParser(
        description="Gera index.html em TODAS as subpastas (mas não na raiz), com links para download dos arquivos."
    )
    ap.add_argument("root", nargs="?", default=".", help="Diretório raiz (padrão: diretório atual).")
    ap.add_argument("--hidden", action="store_true", help="Inclui arquivos e pastas ocultas (nomes iniciados por '.').")
    ap.add_argument("--exclude-dir", action="append", default=[], help="Exclui diretórios pelo nome (pode repetir).")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    include_hidden = args.hidden
    exclude_dirs = set(args.exclude_dir or [])

    if not os.path.isdir(root):
        print(f"Erro: raiz '{root}' não é um diretório.", file=sys.stderr)
        sys.exit(2)

    total_dirs = 0
    total_files = 0

    for dirpath, dirnames, _ in os.walk(root, topdown=True):
        # filtra dirs ocultos e excluídos antes de descer
        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not is_hidden(d)]
        if exclude_dirs:
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        # pula a RAIZ (não gera index.html nela)
        if os.path.abspath(dirpath) == root:
            continue

        files = list_files_for_dir(dirpath, include_hidden)
        if files is None:
            rel = os.path.relpath(dirpath, root)
            print(f"[{rel}] sem permissão; ignorado.")
            continue

        html_str = build_html(dirpath, root, files)
        write_index(dirpath, html_str)

        rel = os.path.relpath(dirpath, root)
        print(f"[{rel}] index.html gerado com {len(files)} arquivo(s).")

        total_dirs += 1
        total_files += len(files)

    print(f"\nConcluído: {total_dirs} subdiretório(s) processados; {total_files} arquivo(s) listados no total.\n(Conforme solicitado, nenhum index.html foi criado na raiz.)")

if __name__ == "__main__":
    main()
