# gen_manifest.py
import os
import sys
import json
import argparse

IGNORE_FILES_CI = {"index.html", "index.htm", "manifest.json", "manifest.py"}

def is_hidden(name: str) -> bool:
    return name.startswith(".")

def list_files_for_dir(dirpath: str, include_hidden: bool):
    """Lista somente arquivos do diretório atual, aplicando filtros."""
    items = []
    try:
        for name in os.listdir(dirpath):
            full = os.path.join(dirpath, name)
            if not os.path.isfile(full):
                continue
            if name.lower() in IGNORE_FILES_CI:
                continue
            if not include_hidden and is_hidden(name):
                continue
            items.append(name)
    except PermissionError:
        # Sem permissão para listar/ler este diretório
        return None
    items.sort(key=lambda s: s.lower())
    return items

def write_manifest(dirpath: str, files):
    """Grava manifest.json no diretório dado."""
    path = os.path.join(dirpath, "manifest.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(files, f, ensure_ascii=False, indent=2)
        f.write("\n")

def main():
    ap = argparse.ArgumentParser(
        description="Gera manifest.json em todos os diretórios a partir de uma raiz."
    )
    ap.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Diretório raiz (padrão: diretório atual).",
    )
    ap.add_argument(
        "--hidden",
        action="store_true",
        help="Inclui arquivos e diretórios ocultos (nomes iniciados por '.').",
    )
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    include_hidden = args.hidden

    if not os.path.isdir(root):
        print(f"Erro: raiz '{root}' não é um diretório.", file=sys.stderr)
        sys.exit(2)

    total_dirs = 0
    total_files_listed = 0

    # Caminhamento recursivo
    for dirpath, dirnames, _filenames in os.walk(root, topdown=True):
        # Opcionalmente filtra pastas ocultas para não descer nelas
        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not is_hidden(d)]

        files = list_files_for_dir(dirpath, include_hidden)
        if files is None:
            rel = os.path.relpath(dirpath, root)
            print(f"[{rel}] sem permissão; ignorado.")
            continue

        write_manifest(dirpath, files)

        rel = os.path.relpath(dirpath, root)
        if rel == ".":
            rel = ". (raiz)"
        print(f"[{rel}] manifest.json gerado com {len(files)} arquivo(s).")

        total_dirs += 1
        total_files_listed += len(files)

    print(
        f"\nConcluído: {total_dirs} diretório(s), {total_files_listed} arquivo(s) listados ao todo."
    )

if __name__ == "__main__":
    main()
