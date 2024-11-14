import argparse
import os
import subprocess

try:
    from PyPDF2 import PdfMerger
    MERGE = True
except ImportError:
    print("Could not find PyPDF2. Leaving pdf files unmerged.")
    MERGE = False

def main(files, pdf_name):
    os_args = [
        "jupyter",
        "nbconvert",
        "--log-level",
        "CRITICAL",
        "--to",
        "pdf",
    ]
    generated_pdfs = []  # 存储生成的PDF文件名
    for f in files:
        os_args.append(f)
        subprocess.run(os_args)
        # 正确生成PDF文件名，确保从.ipynb转换为.pdf
        pdf_file = f.replace(".ipynb", ".pdf")
        if not os.path.exists(pdf_file):
            print(f"PDF file {pdf_file} not created. Please check the nbconvert command.")
            return
        print("Created PDF {}.".format(pdf_file))
        generated_pdfs.append(pdf_file)  # 添加到列表中

    if MERGE:
        merger = PdfMerger()
        for pdf in generated_pdfs:
            if os.path.exists(pdf):  # 检查文件是否存在
                merger.append(pdf)
            else:
                print(f"File {pdf} not found. Skipping.")
        merger.write(pdf_name)
        merger.close()
        for pdf in generated_pdfs:  # 使用正确的文件名进行删除
            if os.path.exists(pdf):  # 再次检查文件是否存在
                os.remove(pdf)
            else:
                print(f"File {pdf} not found. Skipping deletion.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--notebooks", type=str, nargs="+", required=True)
    parser.add_argument("--pdf_filename", type=str, required=True)
    args = parser.parse_args()
    main(args.notebooks, args.pdf_filename)