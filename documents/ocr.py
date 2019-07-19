import pdf2image
import os
import subprocess
from sys import argv

cmd = ["C:/Users/Sifat/AppData/Local/Tesseract-OCR/tesseract.exe",
       "--tessdata-dir", "C:/Users/Sifat/AppData/Local/Tesseract-OCR/tessdata",
       "image_path", "stdout"]


def get_image_list_from_pdf(file_path: str):
    """
    Creates one image for each page of the pdf and returns the path of the images sorted by page number in a list
    :param file_path: path of the pdf file
    :return: a list of path of the image files (one for each page, sorted by page number)
    """

    images_list = []
    pages = pdf2image.convert_from_path(file_path)

    for page_no, page in enumerate(pages):
        images_list.append('temp/{}.jpg'.format(str(page_no).rjust(3, '0')))
        page.save(images_list[-1], 'JPEG')

    print("pdf to image conversion completed..")

    return images_list


def extract_text_from_image_list(images_list: list, delete_flies: bool = True):
    """
    Extracts text from a list of image paths
    :param images_list: a list containing the paths of the image files
    :param delete_flies: boolean value, deletes the image files if found true (default behaviour)
    :return: a string containing all the text extracted from the images
    """

    text = ""
    for image in images_list:
        if os.path.exists(image):
            cmd[-2] = image
            text += str(subprocess.check_output(cmd))
            if delete_flies:
                os.remove(image)
        else:
            print('Error: No file found in the specified path {}.'.format(image))

    return text


def extract_text(file_path: str, is_pdf: bool = True):
    """
    extracts text from a given file
    :param file_path: path to file to extract text from
    :param is_pdf: True if the given file is pdf, False otherwise
    :return: extracted text from the file
    """
    print('file', file_path)

    image_list = get_image_list_from_pdf(file_path) if is_pdf else [file_path]
    text = extract_text_from_image_list(image_list, is_pdf)

    return text


def main():
    if len(argv) == 2:
        file_path = argv[1]
        is_pdf = True if str(file_path).split('.')[-1].lower() == 'pdf' else False
        print(extract_text(file_path=file_path, is_pdf=is_pdf))
    else:
        print("Usage: ./ocr.py path_to_the_file_with_proper_extension")


if __name__ == "__main__":
    main()
