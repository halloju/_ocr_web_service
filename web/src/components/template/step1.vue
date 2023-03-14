<script>
import axios from 'axios';
import { ElLoading } from 'element-plus';

export default {
    name: 'GeneralUploadImage',
    props: ['nextStepEmit'],
    data() {
        return {
            breadcrumbHome: { icon: 'pi pi-home', to: '/' },
            breadcrumbItems: [
                { label: '主要功能', to: '#' },
                { label: '通用文件辨識', to: '#' },
                { label: '通用辨識', to: '#' },
                { label: '圖檔上傳', to: '#' }
            ],
            switchValue: false,
            image_complexity: 'medium',
            // upload 參數
            fileList: [],
            dialogVisible: false,
            imaWidth: '',
            dialogWidth: ''
        };
    },
    watch: {
        switchValue: function (newVal) {
            if (newVal) {
                this.image_complexity = 'high';
            } else {
                this.image_complexity = 'medium';
            }
        }
    },
    computed: {
        disableUpload() {
            if ((this.fileList.length === 0) | (this.selectedLang === null)) {
                return true;
            } else {
                return false;
            }
        }
    },
    methods: {
        submit() {
            const generalImageResponseList = [];
            const responseData = {};
            const base64Image = this.fileList[0].reader.split(',')[1];
            responseData['base64Image'] = base64Image;
            responseData['fileName'] = this.fileList[0].name;
            // 打 API
            const formData = new FormData();
            formData.append('image_complexity', this.image_complexity);
            formData.append('model_name', this.selectedLang.code);
            this.fileList.forEach((file) => {
                formData.append('files', file.raw);
            });
            axios
                .post('/gp_ocr/predict_images', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then((response) => {
                    generalImageResponseList.push(...response.data);
                })
                .catch((error) => {
                    console.log(error);
                    if (error.code === 'ERR_NETWORK') {
                        this.status = 'network';
                    }
                });
            const loading = ElLoading.service({
                lock: true,
                text: 'Loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            setTimeout(() => {
                this.$store.commit('generalImageResponse', generalImageResponseList);
                this.$emit('uploadConfig', this.image_complexity, this.selectedLang.code);
                loading.close();
                this.$emit('nextStepEmit', 2);
            }, 1000);
        },
        fileChange(file, fileList) {
            const isIMAGE = file.type === 'image/jpeg' || 'image/png';
            const isLt5M = file.size / 1024 / 1024 < 5;
            if (!isIMAGE) {
                this.$message.error('上傳文件只能是圖片格式!');
                fileList.pop();
                return false;
            }
            if (!isLt5M) {
                this.$message.error('上傳圖案大小不能超過 5 MB!');
                fileList.pop();
                return false;
            }
            if (isIMAGE && isLt5M) {
                var reader = new FileReader();
                reader.onload = (f) => {
                    this.imageSource = f.target.result;
                    file.reader = f.target.result;
                };
                reader.readAsDataURL(file.raw);
                this.fileList.push(file);
            }
        },
        handleRemove(file) {
            for (let i = 0; i < this.fileList.length; i++) {
                if (this.fileList[i]['uid'] === file.uid) {
                    this.fileList.splice(i, 1);
                    break;
                }
            }
        },
        handlePictureCardPreview(file) {
            this.dialogImageUrl = file.url;
            this.dialogVisible = true;
        },
        onLoadImg(e) {
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
            this.imgWidth = width;
            this.dialogWidth = width + 40;
        }
    }
};
</script>

<template>
    <div class="grid p-fluid">
        <div class="col-12 md:col-9">
            <div class="card">
                <el-upload :file-list="fileList" list-type="picture-card" :on-change="fileChange" :on-remove="handleRemove" multiple :auto-upload="false" :on-preview="handlePictureCardPreview" accept="image/*">
                    <el-icon><Plus /></el-icon>
                </el-upload>
                <el-dialog v-model="dialogVisible" :width="dialogWidth">
                    <img :src="dialogImageUrl" alt="Preview Image" @load="onLoadImg" :width="imgWidth" />
                </el-dialog>
            </div>
        </div>
        <div class="col-12 md:col-3">
            <div class="card">
                <div class="flex flex-column flex-wrap">
                    <div class="flex justify-content-start mb-1">
                        <h5>使用高精準度模型</h5>
                    </div>
                    <div class="flex justify-content-start mb-1">
                        <p>注意：當您使用高精準模型時耗時會較久</p>
                    </div>
                    <div class="flex justify-content-start mb-5">
                        <el-switch v-model="switchValue" inline-prompt active-text="是" inactive-text="否" />
                    </div>
                    <div class="flex justify-content-start mb-1">
                        <el-button type="primary" class="mr-2 mb-2" style="width: 100%" @click="submit" :disabled="disableUpload"> 圖檔提交 </el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
