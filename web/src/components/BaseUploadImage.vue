<script>
import { ref } from 'vue';
import { apiClient } from '@/service/auth.js';
import { ElLoading, ElMessageBox, ElMessage } from 'element-plus';
import { TOTAL_FILE_SIZE_LIMIT, FILE_SIZE_LIMIT, API_TIMEOUT } from '@/constants.js';
import { useStore } from 'vuex';
import { handleErrorMsg } from '@/mixins/useCommon.js';

export default {
    name: 'BaseUploadImage',
    props: {
        apiUrl: {
            type: String,
            required: true
        },
        selectedModel: {
            type: Object
        },
        useLanguage: {
            type: Boolean,
            default: false
        },
        // The default category is 'general' with limited file number to be 20
        category: {
            type: Object
        },
        imageClass: {
            type: String
        },
        defaultImgURL: {
            type: Object
        },
        description: {
            type: String
        }
    },
    setup(props, { emit }) {
        const store = useStore();
        const breadcrumbItems = [
            { label: '主要功能', to: '#' },
            { label: '通用文件辨識', to: '#' },
            { label: '通用辨識', to: '#' },
            { label: '圖檔上傳', to: '#' }
        ];
        const buttonText = ref('開始辨識');
        const buttonType = ref('btnDarkBlue');
        const uploadButtonText = ref('帶入範例圖片');
        // upload 參數
        const fileList = ref([]);
        const dialogVisible = ref(false);
        const imgWidth = ref('');
        const dialogWidth = ref('');
        const dialogImageUrl = ref('');
        const imageSource = ref('');

        async function submit() {
            // check
            var error_str = '';
            if (fileList.value.length === 0) {
                error_str += `還未選擇檔案，請選擇後再繼續。\n`;
            }
            if (props.selectedModel.length == 0) {
                error_str += `語言與類型不可為空，請選擇後再繼續。\n`;
            }
            if (error_str != '') {
                ElMessage({
                    message: error_str,
                    type: 'warning'
                });
                return;
            }

            const loading = ElLoading.service({
                lock: true,
                text: 'Loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });

            const generalImageResponseList = [];
            const responseData = {};
            const base64Image = fileList.value[0].reader.split(',')[1];
            responseData['base64Image'] = base64Image;
            responseData['fileName'] = fileList.value[0].name;
            // 打 API
            const formData = new FormData();
            if (props.useLanguage) {
                props.selectedModel.forEach((filter) => {
                    formData.append('filters', filter);
                });
            }
            if (props.imageClass) {
                formData.append('image_class', props.imageClass);
            }
            fileList.value.forEach((file) => {
                formData.append('files', file.raw);
            });
            formData.append('template_id', store.state.template_id);
            // predict_images
            try {
                const response = await apiClient.post(props.apiUrl, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    timeout: API_TIMEOUT
                });
                generalImageResponseList.push(...response.data);
            } catch (error) {
                var msg = '';
                if (error.message && error.message.includes('413')) {
                    console.log('The file you tried to upload is too large.');
                    msg = `The files you tried to upload are too large. \n (total exceed ${TOTAL_FILE_SIZE_LIMIT} MB)`;
                } else if (error.code === 'ERR_NETWORK') {
                    this.status = 'network';
                } else {
                    msg = handleErrorMsg(error.response);
                }
                //error alert for the axios request
                ElMessageBox.confirm(msg, '失敗', {
                    confirmButtonText: '確定',
                    type: 'error',
                    center: true,
                    showclose: false,
                    showCancelButton: false,
                    closeOnClickModal: false,
                    roundButton: true
                }).then(() => {
                    return;
                });
            }

            // 顯示結果
            setTimeout(() => {
                store.commit('generalImageResponse', generalImageResponseList);
                loading.close();
                emit('nextStepEmit', 2);
            }, 1000);
        }
        async function takeDefault() {
            const imageUrl = props.defaultImgURL;

            // Fetch the image data from the URL
            const response = await fetch(imageUrl);
            const blob = await response.blob();

            // Create a File object from Blob
            const file = new File([blob], 'default.jpg', { type: 'image/jpeg' });
            const fileDict = {
                name: 'default.jpeg',
                url: imageUrl,
                raw: file,
                size: file.size,
                type: file.type
            };

            beforeUpload(fileDict);
        }

        function beforeUpload(file, uploadFiles) {
            // Check file size && file type
            const rawFile = file.raw;
            const isIMAGE = rawFile.type === 'image/jpeg' || rawFile.type === 'image/png';
            const isPDF = rawFile.type === 'application/pdf';
            const isLt2M = rawFile.size < FILE_SIZE_LIMIT;
            if (!isIMAGE && !isPDF) { // Check if file is neither an image nor a PDF
                ElMessageBox.alert('文件只能是 JPG/PNG/PDF 格式!', '錯誤', {
                    confirmButtonText: '確定',
                    type: 'error'
                });
                uploadFiles.pop();
            } else if (isLt2M) {
                processFile(file);
            } else {
                // If the file is an image but over the size limit, compress it
                if (isIMAGE) {
                    compressImageBasedOnRatio(rawFile, FILE_SIZE_LIMIT).then((compressedBlob) => {
                        // Replace the original file with the compressed one
                        const compressedFile = new File([compressedBlob], file.name, {
                            type: file.type,
                            lastModified: Date.now()
                        });
                        // Add the compressed file back to uploadFiles
                        file.raw = compressedFile; // Update the raw file to the compressed one
                        processFile(file); // Process the file after compression
                    });
                } else {
                    processFile(file);
                }
            }
        }

        function processFile(file) {
            var reader = new FileReader();
            reader.onload = (f) => {
                imageSource.value = f.target.result;
                file.reader = f.target.result;
            };
            // Use file.raw if available, otherwise fall back to file itself
            reader.readAsDataURL(file.raw || file);
            fileList.value.push(file);
        }

        function compressImageBasedOnRatio(file, targetMaxSize, attempt = 1) {
            console.log('Compressing image, attempt:', attempt);
            return new Promise((resolve, reject) => {
                const initialSize = file.size;
                const sizeRatio = initialSize / targetMaxSize;

                var img = new Image();
                img.src = URL.createObjectURL(file);
                img.onload = () => {
                    // Apply a decreasing factor to the dimensions on each attempt
                    const decreaseFactor = Math.sqrt(sizeRatio) * (1 + 0.1 * attempt);
                    var targetWidth = img.width / decreaseFactor;
                    var targetHeight = img.height / decreaseFactor;

                    var canvas = document.createElement('canvas');
                    canvas.width = targetWidth;
                    canvas.height = targetHeight;

                    var ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, targetWidth, targetHeight);

                    canvas.toBlob((blob) => {
                        if (blob.size > targetMaxSize && attempt < 10) {
                            // Limit the number of attempts to prevent infinite recursion
                            // If the size is still too big, try again with an increased attempt count
                            resolve(compressImageBasedOnRatio(blob, targetMaxSize, attempt + 1));
                        } else {
                            resolve(blob); // Resolve with the blob if under target size or max attempts reached
                        }
                    }, file.type);
                };

                img.onerror = () => reject(new Error('Image loading error'));
            });
        }

        function handleRemove(file) {
            // Remove file from fileList
            for (let i = 0; i < fileList.value.length; i++) {
                if (fileList.value[i].raw.uid === file.uid) {
                    fileList.value.splice(i, 1);
                    break;
                }
            }
        }

        function handlePictureCardPreview(file) {
            dialogImageUrl.value = file.url;
            dialogVisible.value = true;
        }

        // handle if the upload number exceed the limit
        function handleExceed(file) {
            ElMessageBox.alert(`只能上傳 ${props.category.limit} 張圖片!`, '錯誤', {
                confirmButtonText: '確定',
                type: 'error'
            });
        }

        // Image preview
        function onLoadImg(e) {
            // Get image width
            const img = e.target;
            let width = 0;

            if (img.fileSize > 0 || (img.naturalWidth > 1 && img.naturalHeight > 1)) {
                width = img.naturalWidth;
            }
            if (img.naturalWidth < 200) {
                width = 200;
            } else if (img.naturalHeight > img.naturalWidth && width > 370) {
                width = 370;
            } else {
                width = 500;
            }
            imgWidth.value = width;
            dialogWidth.value = width + 40;
        }

        return {
            description: props.description,
            breadcrumbItems,
            buttonText,
            buttonType,
            uploadButtonText,
            fileList,
            dialogVisible,
            imgWidth,
            dialogWidth,
            dialogImageUrl,
            defaultImgURL: props.defaultImgURL,
            category: props.category,
            useModelComplexity: props.useModelComplexity,
            useLanguage: props.useLanguage,
            takeDefault,
            submit,
            beforeUpload,
            handleRemove,
            handlePictureCardPreview,
            onLoadImg,
            handleExceed
        };
    }
};
</script>

<template>
    <div>
        <div class="card" style="background-color: white">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px">
                <p>{{ description }}</p>
                <div v-if="(fileList.length == 0) & (defaultImgURL != '')" style="display: grid; place-items: center">
                    <div class="formBtnContainer">
                        <button class="uiStyle sizeS subLength btnGreen" @click="takeDefault">
                            {{ uploadButtonText }}
                        </button>
                    </div>
                </div>
            </div>
            <div v-if="fileList.length > 0" style="margin-bottom: 20px">
                <el-alert
                    :title="'已選擇 ' + fileList.length + ' 個檔案，最多可上傳 ' + category.limit + ' 個檔案。'"
                    type="success"
                    show-icon
                    center
                    :closable="false"
                ></el-alert>
            </div>
            <el-upload
                :file-list="fileList"
                list-type="text"
                :on-change="beforeUpload"
                :on-remove="handleRemove"
                multiple
                :limit="category.limit"
                :on-exceed="handleExceed"
                :auto-upload="false"
                :on-preview="handlePictureCardPreview"
                accept="image/*, .pdf"
            >
                <button class="uiStyle sizeS subLength btnBlue">Click to upload</button>
            </el-upload>
        </div>

        <div style="display: grid; place-items: center">
            <div class="formBtnContainer">
                <button class="uiStyle sizeL subLength btnGreen" @click="submit">
                    {{ buttonText }}
                </button>
            </div>
        </div>
    </div>
</template>

