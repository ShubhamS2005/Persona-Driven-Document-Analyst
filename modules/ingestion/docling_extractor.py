import os

# MUST be before importing docling
os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"


from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat


class DoclingExtractor:

    def __init__(self):

        print("Initializing Docling...")


        # -----------------------------
        # Low memory PDF configuration
        # -----------------------------

        pipeline_options = PdfPipelineOptions()


        # Reduce page rendering memory
        pipeline_options.images_scale = 1.0


        # We only need text for RAG
        # avoid storing images
        pipeline_options.generate_picture_images = False


        # Enable only if PDFs are scanned
        pipeline_options.do_ocr = False


        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF:
                PdfFormatOption(
                    pipeline_options=pipeline_options
                )
            }
        )


        print("Docling ready")


    def extract(self, pdf_path):

        print(
            "Extracting:",
            pdf_path
        )


        result = self.converter.convert(
            pdf_path
        )


        document = result.document


        elements = []


        for item in document.texts:

            page = None


            if item.prov:
                page = item.prov[0].page_no


            text = item.text.strip()


            # Ignore empty elements
            if not text:
                continue


            elements.append(
                {
                    "text": text,

                    "type": str(item.label),

                    "page": page,

                    "source": pdf_path
                }
            )


        print(
            f"Extracted {len(elements)} text elements"
        )


        return elements