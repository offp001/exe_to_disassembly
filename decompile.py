import os
import urllib.request
import subprocess
import marshal
import dis
import io
from contextlib import redirect_stdout

def main():
    name = input("enter exe name (without extension): ").strip().lower()
    
    exe_file = None
    for f in os.listdir('.'):
        if f.lower() == name + ".exe":
            exe_file = f
            break
    
    if not exe_file:
        print("file not found")
        return

    extractor_script = "pyinstxtractor.py"
    if not os.path.exists(extractor_script):
        url = "https://raw.githubusercontent.com/extremecoders-re/pyinstxtractor/master/pyinstxtractor.py"
        try:
            urllib.request.urlretrieve(url, extractor_script)
        except Exception:
            pass

    if os.path.exists(extractor_script):
        subprocess.run(["python3", extractor_script, exe_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    out_dir = exe_file + "_extracted"
    success = 0
    fail = 0
    total_code_blocks = 0

    if os.path.exists(out_dir):
        master_file = os.path.join(out_dir, "all_functions_disasm.txt")
        with open(master_file, "w", encoding="utf-8") as master_out:
            for root, dirs, files in os.walk(out_dir):
                for file in files:
                    if file.endswith(".pyc") and not file.endswith("_fixed.pyc"):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, "rb") as f:
                                data = f.read()

                            code_obj = None
                            for offset in [16, 0, 8, 12, 24, 32] + list(range(4, 128, 4)):
                                try:
                                    if len(data) > offset:
                                        code_obj = marshal.loads(data[offset:])
                                        break
                                except Exception:
                                    continue

                            if code_obj:
                                py_path = filepath[:-4] + ".pyasm"
                                f_buf = io.StringIO()
                                with redirect_stdout(f_buf):
                                    dis.dis(code_obj)
                                with open(py_path, "w", encoding="utf-8") as out:
                                    out.write(f"# source: {file}\n\n")
                                    for line in f_buf.getvalue().splitlines():
                                        out.write(f"{line}\n")

                                code_objects = []
                                seen_ids = set()

                                def collect_codes(co):
                                    if id(co) in seen_ids:
                                        return
                                    seen_ids.add(id(co))
                                    code_objects.append(co)
                                    if hasattr(co, "co_consts"):
                                        for const in co.co_consts:
                                            if hasattr(const, "co_code"):
                                                collect_codes(const)

                                collect_codes(code_obj)

                                for co in code_objects:
                                    total_code_blocks += 1
                                    master_out.write("=" * 70 + "\n")
                                    master_out.write(f"file: {file} | function: {getattr(co, 'co_name', 'unknown')} | line: {getattr(co, 'co_firstlineno', 0)}\n")
                                    master_out.write("=" * 70 + "\n")

                                    f_buf = io.StringIO()
                                    with redirect_stdout(f_buf):
                                        try:
                                            dis.dis(co)
                                        except Exception:
                                            pass
                                    master_out.write(f_buf.getvalue())
                                    master_out.write("\n\n")

                                success += 1
                                try:
                                    os.remove(filepath)
                                except Exception:
                                    pass
                            else:
                                fail += 1
                        except Exception:
                            fail += 1

    print(f"done ({success} converted {fail} errors, {total_code_blocks} total blocks)")

if __name__ == '__main__':
    main()