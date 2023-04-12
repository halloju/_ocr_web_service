from app.exceptions import CustomException
from fastapi import APIRouter, UploadFile, Request, Response, File
from pydantic.typing import List
from fastapi import Depends
from fastapi.responses import StreamingResponse
from pdf2image import convert_from_bytes
import zipfile
import io
import os
import tempfile
from PIL import ImageFile, Image
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
router = APIRouter()

def zipfiles(filenames):
    zip_filename = "archive.zip"

    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")
    no = 0
    for fpath in filenames:
        # print(fpath)
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)

        # Add file, at correct path
        zf.write(fpath, fname)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename}'
    })

    return resp

def get_bytes_value(image, folder, name):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    path = os.path.join(folder, name+'.jpg')
    with open(path, 'wb') as f:
        f.write(img_byte_arr.getvalue())
    return path

@router.post("/pdf_transform")  # responses={},
async def gp_ocr(request: Request, files: List[UploadFile] = File(...), timeout: int = 300):
    '''
    將 pdf 轉成圖片
    '''
    success_file_num = 0
    all_img_files = []
    zip_dir = tempfile.mkdtemp()
    for doc in files:
        # Read and encode the file data as base64
        if doc.content_type == 'application/pdf':
            filename = doc.filename.split('/')[-1].replace('.pdf', '').replace('.PDF', '')
            # pdf_file = await file.read()  # byte
            try:
                with tempfile.TemporaryDirectory() as path:
                    doc_results = convert_from_bytes(
                        doc.file.read(), output_folder=path, dpi=300, thread_count=4
                    )
            except:
                raise CustomException(status_code=400, message=f'{doc.filename} 該檔案出了一點問題，請確認此 pdf 是否有效')
            img_files = [get_bytes_value(image, zip_dir, f'{filename}_{idx}') for idx, image in enumerate(doc_results)] if doc_results else None
            all_img_files.extend(img_files)
            success_file_num += 1
    if success_file_num != 0:
        return zipfiles(all_img_files)
    else:
        raise CustomException(status_code=400, message='未上傳有效的 pdf 檔案')
