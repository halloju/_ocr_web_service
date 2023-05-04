<script>
import { ref, computed, watch, onMounted } from 'vue';
import axios from 'axios';
import { ElLoading, ElMessageBox } from 'element-plus';
import { FILE_SIZE_LIMIT, API_TIMEOUT } from '@/constants.js';
import { useStore } from 'vuex';

export default {
    name: 'BaseUploadImage',
    props: {
        apiUrl: {
            type: String,
            required: true
        },
        useModelComplexity: {
            type: Boolean,
            default: false
        },
        useLanguage: {
            type: Boolean,
            default: false
        },
        // The default category is 'general' with limited file number to be 20
        category: {
            type: Object
        }
    },
    setup(props, { emit }) {
        const store = useStore();

        
        const languages = [
            { name: '繁體中文 + 英數字', code: 'dbnet_v0+cht_ppocr_v1' },
            { name: '英數字', code: 'dbnet_v0+en_ppocr_v0' }
        ];
        const selectedLang = ref(languages[0]);
        const breadcrumbItems = [
            { label: '主要功能', to: '#' },
            { label: '通用文件辨識', to: '#' },
            { label: '通用辨識', to: '#' },
            { label: '圖檔上傳', to: '#' }
        ];
        const image_complexity = ref('medium');
        const switchValue = ref(false);
        // upload 參數
        const fileList = ref([]);
        const dialogVisible = ref(false);
        const imgWidth = ref('');
        const dialogWidth = ref('');
        const dialogImageUrl = ref('');
        const imageSource = ref('');

        const isUploadDisabled = computed(() => {
            if ((fileList.value.length === 0)) {
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
            formData.append('image_complexity', image_complexity.value);
            formData.append('model_name', selectedLang.value.code);
            formData.append('template_id', store.state.template_id);
            fileList.value.forEach((file) => {
                formData.append('files', file.raw);
            });

            // predict_images
            try {
                const response = await axios.post(props.apiUrl, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    timeout: API_TIMEOUT
                });
                generalImageResponseList.push(...response.data);
            } catch (error) {
                var msg = ''
                if (error.message && error.message.includes('413')) {
                    console.log('The file you tried to upload is too large.')
                    msg = 'The files you tried to upload are too large. \n (total exceed 8 MB)'
                }
                else if (error.code === 'ERR_NETWORK') {
                    this.status = 'network';
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
                emit('uploadConfig', image_complexity, selectedLang.value.code);
                loading.close();
                emit('nextStepEmit', 2);
            }, 1000);
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
        // watch
        watch(switchValue, (newVal) => {
            if (newVal) {
                image_complexity.value = 'high';
            } else {
                image_complexity.value = 'medium';
            }
        });

        return {
            breadcrumbItems,
            image_complexity,
            selectedLang,
            languages,
            fileList,
            dialogVisible,
            imgWidth,
            dialogWidth,
            dialogImageUrl,
            isUploadDisabled,
            category: props.category,
            useModelComplexity: props.useModelComplexity,
            useLanguage: props.useLanguage,
            switchValue,
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
    <div class="grid p-fluid">
        <div class="col-12 md:col-9">
            <div class="card">
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
        </div>
        <div class="col-12 md:col-3">
            <div class="card">
                <div class="flex flex-column flex-wrap">
                    <div class="flex justify-content-start mb-1" v-if="useLanguage">
                        <h5>選擇語言</h5>
                    </div>
                    <div class="flex justify-content-start mb-5" v-if="useLanguage">
                        <Dropdown v-model="selectedLang" style="width: 100%" :options="languages" optionLabel="name" placeholder="請選擇" />
                    </div>
                    <div v-if="useModelComplexity" class="flex justify-content-start mb-1">
                        <h5>使用高精準度模型</h5>
                    </div>
                    <div v-if="useModelComplexity" class="flex justify-content-start mb-1">
                        <p>注意：當您使用高精準模型時耗時會較久</p>
                    </div>
                    <div v-if="useModelComplexity" class="flex justify-content-start mb-5">
                        <el-switch v-model="switchValue" inline-prompt active-text="是" inactive-text="否" />
                    </div>
                    <div class="flex justify-content-start mb-1">
                        <el-button type="primary" class="mr-2 mb-2" style="width: 100%" @click="submit" :disabled="isUploadDisabled"> 圖檔提交 </el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
