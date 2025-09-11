from __future__ import annotations

import io
import pdfplumber
import docx


class CVExtractor:
    def __init__(self, file_bytes: bytes, filename: str):
        """
        :param file_bytes: raw bytes dari UploadFile.read()
        :param filename: file name (for extension detection)
        """
        self.file_bytes = file_bytes
        self.filename = filename
        self.text = self._extract_text()

    def _extract_text(self) -> str:
        """for extension detection and extract text"""
        ext = self.filename.split(".")[-1].lower()

        if ext == "pdf":
            return self._extract_pdf()
        elif ext == "docx":
            return self._extract_docx()
        elif ext == "txt":
            return self._extract_txt()
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _extract_pdf(self) -> str:
        text = ""
        with pdfplumber.open(io.BytesIO(self.file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()

    def _extract_docx(self) -> str:
        doc = docx.Document(io.BytesIO(self.file_bytes))
        return "\n".join([para.text for para in doc.paragraphs]).strip()

    def _extract_txt(self) -> str:
        return self.file_bytes.decode("utf-8", errors="ignore").strip()
