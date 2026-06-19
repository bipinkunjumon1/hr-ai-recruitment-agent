import fitz


class PDFParser:

    @staticmethod
    def extract_text(pdf_path: str):

        text = ""

        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

        return text