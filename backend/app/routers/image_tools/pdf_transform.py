import io
import os
import tempfile
import zipfile

from app.exceptions import CustomException
from fastapi import APIRouter, File, Request, Response, UploadFile, Depends
from logger import Logger
from pdf2image import convert_from_bytes
from PIL import Image, ImageFile
from pydantic.typing import List
from route_utils import verify_token

# setting
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
router = APIRouter()
logger = Logger(__name__)

def zipfiles(filenames):
    zip_filename = "archive.zip"

    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")
    no = 0
    for fpath in filenames:
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
    path = os.path.join(folder, f'{name}.jpg')
    with open(path, 'wb') as f:
        f.write(img_byte_arr.getvalue())
    return path

@router.post("/pdf_transform", summary="pdf 轉圖片", dependencies=[Depends(verify_token)])
async def gp_ocr(request: Request, files: List[UploadFile] = File(...), timeout: int = 300):
    '''
    將 pdf 轉成圖片
    '''
    success_file_num = 0
    all_img_files = []
    zip_dir = tempfile.mkdtemp()
    logger.info({'upload_file_num': len(files)})
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
            except Exception as e:
                logger.error({'error_msg': str(e)})
                raise CustomException(status_code=400, message=f'{doc.filename} 該檔案出了一點問題，請確認此 pdf 是否有效')
            logger.info({'filename': filename, 'page_num': len(doc_results)})
            img_files = [get_bytes_value(image, zip_dir, f'{filename}_{idx}') for idx, image in enumerate(doc_results)] if doc_results else None
            all_img_files.extend(img_files)
            success_file_num += 1
    if success_file_num != 0:
        logger.info({'success_file_num': success_file_num})
        return zipfiles(all_img_files)
    else:
        logger.error({'error_msg': '未上傳有效的 pdf 檔案'})
        raise CustomException(status_code=400, message='未上傳有效的 pdf 檔案')
