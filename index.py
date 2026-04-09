import os
import sys
import html
import re

def create_json_index(root_directory, output_file):
    # Verifica validità percorso
    if not os.path.isdir(root_directory):
        print(f"Errore: {root_directory} non è una directory valida.")
        return

    root_abs = os.path.abspath(root_directory)
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            # Header HTML e CSS migliorato
            f.write("<!DOCTYPE html>\n<html lang='it'>\n<head>\n")
            f.write("    <meta charset='UTF-8'>\n")
            f.write("    <style>\n")
            f.write("        body { font-family: 'Monaco', 'Consolas', monospace; margin: 40px; background-color: #1e1e1e; color: #d4d4d4; }\n")
            f.write("        .container { max-width: 1100px; margin: auto; background: #252526; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }\n")
            f.write("        h1 { color: #4ec9b0; border-bottom: 1px solid #3e3e42; padding-bottom: 10px; font-size: 1.4em; }\n")
            f.write("        .folder-section { margin-top: 25px; }\n")
            f.write("        .folder-path { background: #37373d; padding: 6px 12px; font-weight: bold; color: #9cdcfe; font-size: 0.85em; border-left: 4px solid #4ec9b0; margin-bottom: 10px; }\n")
            f.write("        ul { list-style: none; padding-left: 15px; }\n")
            f.write("        li { margin: 4px 0; }\n")
            f.write("        a { text-decoration: none; color: #ce9178; }\n")
            f.write("        a:hover { color: #d7ba7d; text-decoration: underline; }\n")
            f.write("        .count { color: #6a9955; font-size: 0.8em; margin-left: 10px; }\n")
            f.write("    </style>\n</head>\n<body>\n")
            f.write("    <div class='container'>\n")

            total_files = 0

            # Scansione ricorsiva
            for root, dirs, files in os.walk(root_abs):
                # Filtriamo i file con estensione .json
                json_files = sorted([f for f in files if f.lower().endswith('.json')])
                
                # Se non ci sono file JSON in questa cartella specifica, saltiamo la sezione
                if not json_files:
                    continue

                total_files += len(json_files)
                relative_path = os.path.relpath(root, root_abs)
                display_path = "./" if relative_path == "." else relative_path
                
                f.write(f"        <div class='folder-section'>\n")
                f.write(f"            <div class='folder-path'>📂 {html.escape(display_path)} <span class='count'>({len(json_files)} file)</span></div>\n")
                f.write("            <ul>\n")

                for filename in json_files:
                    full_path = os.path.join(root, filename)
                    file_url = f"https://maxpsq.github.io/price-tracker/{re.sub('^.*?/www/', '', full_path)}"
                    f.write(f"                <li>{html.escape('📄 ')}<a href='{file_url}'>{html.escape(filename)}</a></li>\n")
                
                f.write("            </ul>\n")
                f.write("        </div>\n")

            if total_files == 0:
                f.write("<p>Nessun file .json trovato nel percorso specificato.</p>")
            
            f.write(f"        <p style='margin-top:40px; border-top: 1px solid #3e3e42; padding-top: 10px; color: #6a9955;'>Totale file JSON indicizzati: {total_files}</p>\n")
            f.write("    </div>\n</body>\n</html>")
        
        print(f"Completato! Trovati {total_files} file .json.")
        print(f"Indice creato in: {os.path.abspath(output_file)}")

    except Exception as e:
        print(f"Errore critico: {e}")


if __name__ == "__main__":
    # Controllo degli argomenti da riga di comando
    if len(sys.argv) < 2:
        print("Utilizzo: python3 script.py /path/to/directory")
    else:
        target_dir = sys.argv[1]
        create_json_index(target_dir, './www/index.html')