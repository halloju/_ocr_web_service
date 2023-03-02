from pdf2image import convert_from_path
import glob
import os
from tqdm import tqdm
pdf_files = [i for i in filepaths if i.split('.')[-1] in ['pdf', 'PDF']]
img_folder = os.path.join(save_path, 'img')
output_folder = os.path.join(save_path, 'output')
if not os.path.exists(img_folder):
    os.makedirs(img_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
for filepath in pdf_files:
    # pdf to image
    img_list = []
    try:
        pages = convert_from_path(filepath, 300)
        filename = filepath.split('/')[-1].replace('.pdf', '').replace('.PDF', '.jpg')
        for page_no, page in tqdm(enumerate(pages)):
            img_file = os.path.join(img_folder, f'{filename}_{page_no}.jpg')
            page.save(img_file, 'JPEG')
            img_list += [img_file]
    except Exception as error:
        print(filepath)
        print(error)
    if len(img_list) > 0:
        print(f'{filepath} 轉換的頁數: {len(img_list)}')
    else:
        break
