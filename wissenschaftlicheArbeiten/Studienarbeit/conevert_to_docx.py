import os
from pdf2docx import Converter
from docx import Document

LOCAL_FILE_PATH = "./wissenschaftlicheArbeiten/Studienarbeit/main.docx"
def count_words_in_word_file():
    """
    Count the words in a Microsoft Word (.docx) document.

    Args:
        file_path (str): Path to the .docx file.

    Returns:
        int: Total word count.
    """
    try:
        # Load the Word document
        doc = Document(LOCAL_FILE_PATH)

        # Initialize word count
        word_count = 0

        # Iterate through all paragraphs and count words
        for paragraph in doc.paragraphs:
            word_count += len(paragraph.text.split())
        print(f"The file has {word_count} words")
        return word_count
    except Exception as e:
        print(f"Error: {e}")
        return None

def convert_pdf_to_docx(pdf_path):
    """
    Converts a PDF file to a DOCX file.

    Args:
        pdf_path (str): Path to the PDF file to be converted.
        output_dir (str): Directory where the output DOCX will be saved. Defaults to the same directory as the input file.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' does not exist.")
        return

    if not pdf_path.lower().endswith(".pdf"):
        print("Error: The input file must be a PDF.")
        return

    
    os.makedirs(LOCAL_FILE_PATH, exist_ok=True)

    # Generate output DOCX path
    docx_path = os.path.join(LOCAL_FILE_PATH, os.path.splitext(os.path.basename(pdf_path))[0] + ".docx")

    try:
        print(f"Converting '{pdf_path}' to '{docx_path}'...")
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)  # Convert all pages
        cv.close()
        print(f"Conversion complete! DOCX saved at: {docx_path}")
        count_words_in_word_file()
    except Exception as e:
        print(f"Error during conversion: {e}")


if os.path.exists(LOCAL_FILE_PATH):
    count_words_in_word_file()
else:
    convert_pdf_to_docx("./wissenschaftlicheArbeiten/Studienarbeit/Main_files/main.pdf")
