import fitz


class PyMuPDFExtractor:


    def extract(self, pdf_path):

        doc = fitz.open(pdf_path)

        elements = []


        for page_no,page in enumerate(doc):

            blocks = page.get_text("blocks")


            for block in blocks:

                text = block[4].strip()


                if text:

                    elements.append(
                        {
                            "text":text,
                            "type":"unknown",
                            "page":page_no+1,
                            "source":pdf_path
                        }
                    )


        return elements