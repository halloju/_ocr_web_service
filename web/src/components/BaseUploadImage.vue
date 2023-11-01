<script>
import { ref, computed, watch, onMounted } from 'vue';
import { apiClient } from '@/service/auth.js';
import { ElLoading, ElMessageBox } from 'element-plus';
import { FILE_SIZE_LIMIT, API_TIMEOUT } from '@/constants.js';
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
        imageComplexity: {
            type: String
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

        const isUploadDisabled = computed(() => {
            if (fileList.value.length === 0) {
                return true;
            } else {
                return false;
            }
        });
        async function submit() {
            const generalImageResponseList = [];
            const responseData = {};
            const base64Image = fileList.value[0].reader.split(',')[1];
            responseData['base64Image'] = base64Image;
            responseData['fileName'] = fileList.value[0].name;
            // 打 API
            const formData = new FormData();
            if (props.useLanguage) {
                formData.append('image_complexity', props.imageComplexity);
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
                    msg = 'The files you tried to upload are too large. \n (total exceed 20 MB)';
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
            const loading = ElLoading.service({
                lock: true,
                text: 'Loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });

            // 顯示結果
            setTimeout(() => {
                store.commit('generalImageResponse', generalImageResponseList);
                // emit('uploadConfig', imageComplexity, selectedLang.value.code);
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
        function beforeUpload(file) {
            // Check file size && file type
            const isIMAGE = file.type === 'image/jpeg' || 'image/png';
            const isLt2M = file.size / 1024 / 1024 < FILE_SIZE_LIMIT;
            if (!isIMAGE) {
                ElMessageBox.alert('圖片只能是 JPG/PNG 格式!', '錯誤', {
                    confirmButtonText: '確定',
                    type: 'error'
                });
            }
            if (!isLt2M) {
                ElMessageBox.alert(`圖片大小不能超過 ${FILE_SIZE_LIMIT}MB!`, '錯誤', {
                    confirmButtonText: '確定',
                    type: 'error'
                });
            }
            // Push file to fileList
            if (isIMAGE && isLt2M) {
                var reader = new FileReader();
                reader.onload = (f) => {
                    imageSource.value = f.target.result;
                    file.reader = f.target.result;
                };
                reader.readAsDataURL(file.raw);
                fileList.value.push(file);
            }
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
            isUploadDisabled,
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
            <el-upload
                :file-list="fileList"
                list-type="picture-card"
                :on-change="beforeUpload"
                :on-remove="handleRemove"
                multiple
                :limit="category.limit"
                :on-exceed="handleExceed"
                :auto-upload="false"
                :on-preview="handlePictureCardPreview"
                accept="image/*"
            >
                <el-icon><Plus /></el-icon>
            </el-upload>
            <el-dialog v-model="dialogVisible" :width="dialogWidth">
                <img :src="dialogImageUrl" alt="Uploaded Image Preview" @load="onLoadImg" :width="imgWidth" />
            </el-dialog>
        </div>

        <div style="display: grid; place-items: center">
            <div class="formBtnContainer">
                <button class="uiStyle sizeL subLength btnGreen" @click="submit" :disabled="isUploadDisabled">
                    {{ buttonText }}
                </button>
            </div>
        </div>
    </div>
</template>
