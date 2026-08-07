from collections import defaultdict
class StructureBuilder:
    def build_sections(self,elements):


        documents=defaultdict(list)



        # group by document

        for item in elements:

            documents[
                item["document"]
            ].append(item)



        all_sections=[]



        for document,items in documents.items():


            current_section=None



            for item in items:


                element_type=item.get(
                    "type",
                    ""
                )


                if element_type=="section_header":


                    if current_section:

                        all_sections.append(
                            current_section
                        )


                    current_section={

                        "document":document,

                        "title":item["text"],

                        "content":[],

                        "page_start":item["page"],

                        "page_end":item["page"]

                    }



                else:


                    if current_section is None:


                        current_section={

                            "document":document,

                            "title":"Introduction",

                            "content":[],

                            "page_start":item["page"],

                            "page_end":item["page"]

                        }



                    current_section["content"].append(
                        item["text"]
                    )


                    current_section["page_end"]=item["page"]



            if current_section:

                all_sections.append(
                    current_section
                )



        return all_sections