import re


class Cleaner:
    def clean_text(self,text):
        if not text:
            return ""
        
        # normalize spaces
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        # remove strange artifacts
        text = text.replace(
            "ﬀ",
            "ff"
        )


        text = text.strip()


        return text



    def clean_elements(self,elements):

        cleaned=[]


        for item in elements:


            text=self.clean_text(
                item.get("text","")
            )


            if not text:
                continue


            item["text"]=text


            cleaned.append(item)



        return cleaned