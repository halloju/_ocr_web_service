import io
import os
import shutil
import tempfile
import zipfile

from app.exceptions import CustomException
from fastapi import APIRouter, File, Response, UploadFile
from logger import Logger
from pdf2image import convert_from_path, pdfinfo_from_path
from pdf2image.generators import counter_generator
from PIL import Image, ImageFile
from pydantic.typing import List
from starlette.requests import Request

# setting
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None  # 89478485  # 0.25GB
router = APIRouter()


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


@router.post("/pdf_transform", summary="pdf 轉圖片")
async def gp_ocr(request: Request, files: List[UploadFile] = File(...), timeout: int = 300):
    '''
    將 pdf 轉成圖片
    '''
    success_file_num = 0
    all_img_files = []
    zip_dir = tempfile.mkdtemp()
    logger = request.state.logger
    logger.info({'upload_file_num': len(files)})
    for doc in files:
        # Read and encode the file data as base64
        if doc.content_type == 'application/pdf':
            filename = doc.filename.split(
                '/')[-1].replace('.pdf', '').replace('.PDF', '')
            fh, temp_filename = tempfile.mkstemp()
            with open(temp_filename, "wb") as f:
                f.write(doc.file.read())
                f.flush()
            logger.info({'filename': filename})
            # pdf_file = await file.read()  # byte
            try:
                with tempfile.TemporaryDirectory() as path:
                    info = pdfinfo_from_path(temp_filename)
                    maxPages = info["Pages"]
                    jump = 4
                    for page in range(1, maxPages + 1, jump):
                        convert_from_path(
                            temp_filename,
                            output_folder=zip_dir,
                            dpi=300,
                            thread_count=1,
                            fmt="jpg",
                            output_file=counter_generator(prefix=filename),
                            first_page=page,
                            last_page=min(page + jump - 1, maxPages)
                        )
                    logger.info({'convert_from_bytes': {'filename': filename, 'pageNum': maxPages}})
            except Exception as e:
                logger.error({'convert_from_bytes': {'error_msg': str(e)}})
                # Deletes the temporary directory and all its content
                shutil.rmtree(zip_dir)
                raise CustomException(
                    status_code=400, message=f'{doc.filename} 該檔案出了一點問題，請確認此 pdf 是否有效')
            success_file_num += 1
    if success_file_num != 0:
        logger.info({'success_file_num': success_file_num})
        resp = zipfiles([os.path.join(zip_dir, x)
                        for x in os.listdir(zip_dir)])
        # Deletes the temporary directory and all its content
        shutil.rmtree(zip_dir)
        return resp
    else:
        logger.error({'error_msg': '未上傳有效的 pdf 檔案'})
        # Deletes the temporary directory and all its content
        shutil.rmtree(zip_dir)
        raise CustomException(status_code=400, message='未上傳有效的 pdf 檔案')
