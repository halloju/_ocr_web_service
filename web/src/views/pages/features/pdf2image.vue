<script>
import { apiClient } from '@/service/auth.js';
import { ElLoading, ElMessageBox } from 'element-plus';
import { API_TIMEOUT } from '@/constants.js';

export default {
    name: 'pdf2image',
    data() {
        return {
            fileList: [],
            dialogVisible: false,
            dialogWidth: '50%',
            dialogFileUrl: '',
            embedWidth: '100%',
            embedHeight: '600px',
        };
    },
    mounted() {
        this.initializeClient();
    },
    computed: {
        isUploadDisabled() {
            if (this.fileList.length === 0) {
                return true;
            } else {
                return false;
            }
        }
    },
    methods: {
        fileChange(file) {
            const isLt5M = file.size / 1024 / 1024 < 5;
            if (isLt5M) {
                var reader = new FileReader();
                reader.onload = (f) => {
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
        async submit() {
            const formData = new FormData();
            this.fileList.forEach((file) => {
                formData.append('files', file.raw);
            });
            const loading = ElLoading.service({
                lock: true,
                text: 'Loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            await apiClient
                .post('/image_tools/pdf_transform', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    responseType: 'blob', // Set the response type to 'blob'
                    timeout: API_TIMEOUT // Set the timeout to 10 seconds
                })
                .then((response) => {
                    // Create anchor element
                    const downloadLink = document.createElement('a');
                    downloadLink.href = window.URL.createObjectURL(new Blob([response.data]));
                    downloadLink.setAttribute('download', 'pdf2image.zip');

                    // Simulate click on the anchor element to trigger download
                    downloadLink.click();
                })
                .catch((error) => {
                    var msg = '';
                    if (error.message && error.message.includes('413')) {
                        console.log('The file you tried to upload is too large.');
                        msg = 'The files you tried to upload are too large. \n (total exceed 8 MB)';
                    } else if (error.code === 'ERR_NETWORK') {
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
                    });
                });
            loading.close();
            //remove all file in fileList
            this.fileList = [];
        }
    }
};
</script>

<template>
    <div class="grid p-fluid">
        <div class="col-12">
            <div class="card card-w-title">
                <!-- Breadcrumb -->
                <el-breadcrumb>
                    <el-breadcrumb-item :to="{ path: '/' }">首頁</el-breadcrumb-item>
                    <el-breadcrumb-item>檔案轉換</el-breadcrumb-item>
                </el-breadcrumb>
                <br />
                <h5>pdf 轉換</h5>
                <p>請上傳一份或多份 pdf 檔，下一步會轉成圖檔並打包下載。</p>
            </div>
        </div>
    </div>
    <div class="grid p-fluid">
        <div class="col-12 md:col-9">
            <div class="card">
                <div class="card">
                    <el-upload :file-list="fileList" list-type="text" :on-change="fileChange" :on-remove="handleRemove" multiple :auto-upload="false" accept="application/pdf">
                        <template v-slot="{ file }">
                            <div class="el-upload__text">
                                <template v-if="file">
                                    {{ file.name }}
                                </template>
                                <template v-else>
                                    <el-button type="primary"> Upload PDF File </el-button>
                                </template>
                            </div>
                        </template>
                    </el-upload>
                    <el-dialog v-model="dialogVisible" :width="dialogWidth">
                        <embed :src="dialogFileUrl" type="application/pdf" :width="embedWidth" :height="embedHeight" />
                    </el-dialog>
                </div>
            </div>
        </div>
        <div class="col-12 md:col-3">
            <div class="card">
                <div class="flex flex-column flex-wrap">
                    <div class="flex justify-content-start mb-1">
                        <el-button type="primary" class="mr-2 mb-2" style="width: 100%" @click="submit" :disabled="isUploadDisabled"> 檔案提交 </el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
