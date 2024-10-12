import requests
from PyPDF2 import PdfReader
from gentopia.tools.basetool import *
import os

class PDFReaderFromURLArgs(BaseModel):
    url: str = Field(..., description="The URL of the PDF to be downloaded and read")


class PDFReader(BaseTool):
    """Tool that downloads a PDF from a given URL, reads it, and returns the content as a string."""

    name = "pdf_reader"
    description = "A tool that downloads a PDF from a URL and returns its content as a string."

    args_schema: Optional[Type[BaseModel]] = PDFReaderFromURLArgs

    def _run(self, url: str) -> str:
        
        try:
            print('I was here')
            
            response = requests.get(url)
            if response.status_code != 200:
                return f"Failed to download the PDF. Status code: {response.status_code}"

            
            temp_pdf_path = "temp_downloaded_pdf.pdf"
            
            # Save the PDF content to a file
            with open(temp_pdf_path, 'wb') as f:
                f.write(response.content)

           
            reader = PdfReader(temp_pdf_path)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            
            # Clean up the temporary file
           # os.remove(temp_pdf_path)
            
            return text

        except requests.exceptions.RequestException as e:
            return f"An error occurred while downloading the PDF: {str(e)}"
        except Exception as e:
            return f"An error occurred while reading the PDF: {str(e)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    # Example usage:
    pdf_url = "https://arxiv.org/pdf/2404.16130"  
    pdf_reader = PDFReader()
    content = pdf_reader._run(pdf_url)
    print(content)
