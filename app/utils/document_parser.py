import os

from docx import Document

from rapidocr_onnxruntime import RapidOCR

from utils.pdf_parser import PDFParser


class DocumentParser:

    @staticmethod
    def extract_text(
        file_path: str
    ):

        extension = (
            os.path.splitext(
                file_path
            )[1]
            .lower()
        )

        if extension == ".pdf":

            return PDFParser.extract_text(
                file_path
            )

        elif extension == ".docx":

            return (
                DocumentParser
                .extract_docx(
                    file_path
                )
            )

        elif extension in [

            ".png",

            ".jpg",

            ".jpeg"

        ]:

            return (
                DocumentParser
                .extract_image(
                    file_path
                )
            )

        elif extension == ".txt":

            with open(

                file_path,

                "r",

                encoding="utf-8"

            ) as f:

                return f.read()

        else:

            raise Exception(

                f"Unsupported file type: {extension}"
            )

    @staticmethod
    def extract_docx(
        file_path: str
    ):

        doc = Document(
            file_path
        )

        text = []

        for para in doc.paragraphs:

            text.append(
                para.text
            )

        return "\n".join(text)

    @staticmethod
    def extract_image(
        file_path: str
    ):

        engine = RapidOCR()

        result, _ = engine(
            file_path
        )

        extracted_text = []

        if result:

            for item in result:

                extracted_text.append(
                    item[1]
                )

        return "\n".join(
            extracted_text
        )