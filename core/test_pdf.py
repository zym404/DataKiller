from core.pdf_splitter import PdfEngine

if __name__ == "__main__":
    pdf = PdfEngine("./docs/农业政策文件.pdf")
    text = pdf.get_pdf_text()
    print(text)