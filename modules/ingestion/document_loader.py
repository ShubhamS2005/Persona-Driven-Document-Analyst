from modules.ingestion.docling_extractor import DoclingExtractor
from modules.ingestion.pymupdf_extarctor import PyMuPDFExtractor


class DocumentLoader:

    def __init__(self):

        print("Initializing document loaders...")

        self.docling = DoclingExtractor()

        self.pymupdf = PyMuPDFExtractor()

        print("Document loaders ready")


    def load(self, pdf_path):

        print("\nUsing Docling...")


        # -----------------------------
        # Primary extractor
        # -----------------------------

        try:

            data = self.docling.extract(
                pdf_path
            )


            if data and len(data) > 5:

                print(
                    f"Docling extracted {len(data)} elements"
                )

                return data


            raise Exception(
                "Docling returned insufficient data"
            )


        except Exception as e:

            print(
                "Docling failed:",
                e
            )


        # -----------------------------
        # Fallback extractor
        # -----------------------------

        print(
            "Using PyMuPDF fallback..."
        )


        try:

            data = self.pymupdf.extract(
                pdf_path
            )


            if data and len(data) > 0:

                print(
                    f"PyMuPDF extracted {len(data)} elements"
                )

                return data


            raise Exception(
                "PyMuPDF returned no data"
            )


        except Exception as e:

            print(
                "PyMuPDF failed:",
                e
            )


            return []