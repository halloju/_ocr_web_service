<script>
import { ElMessage } from 'element-plus';

export default {
    name: 'UploadImage',
    created() {
        if (sessionStorage.imageSource !== '') {
            this.isOK = true;
            this.imageSource = sessionStorage.imageSource;
            this.filename = sessionStorage.filename;
            this.filesize = sessionStorage.filesize;
        }
    },
    components: {},
    data() {
        return {
            isDragging: false,
            wrongFile: false,
            imageSource: null,
            filename: '',
            filesize: 0,
            isOK: false,
            isFileUploaded: false
        };
    },
    computed: {
        getClasses() {
            return { isDragging: this.isDragging };
        },
        showFileSize() {
            if (this.filesize === undefined) {
                return 0;
            } else {
                return Number(this.filesize).toFixed(2);
            }
        }
    },
    watch: {
        isOK: {
            handler: function () {
                this.$emit('updateStatus', this.isOK);
            }
        }
    },
    methods: {
        dragOver() {
            if (this.isUploaded) {
                this.isDragging = true;
            }
        },
        dragLeave() {
            this.isDragging = false;
        },
        drop(e) {
            if (!this.isUploaded) {
                e.preventDefault();
                return;
            }
            let files = e.dataTransfer.files;
            this.wrongFile = false;
            // allows only 1 file
            if (files.length === 1) {
                let file = files[0];
                // allows image only
                if (file.type.indexOf('image/') >= 0) {
                    var reader = new FileReader();
                    reader.onload = (f) => {
                        this.imageSource = f.target.result;
                        this.isDragging = false;
                        this.isOK = true;
                        this.filename = file.name;
                        this.filesize = file.size / 1024;
                        sessionStorage.imageSource = this.imageSource;
                        sessionStorage.filename = this.filename;
                        sessionStorage.filesize = this.filesize;
                        this.$store.commit('recsClear');
                    };
                    reader.readAsDataURL(file);
                } else {
                    this.wrongFile = true;
                    this.imageSource = null;
                    this.isDragging = false;
                }
            }
        },
        selectImg(e) {
            if (!this.isUploaded) {
                e.preventDefault();
                return;
            }
            let input = e.target;
            this.wrongFile = false;
            // allows only 1 file
            if (input.files.length === 1) {
                let file = input.files[0];
                // allows image only
                if (file.type.indexOf('image/') >= 0) {
                    var reader = new FileReader();
                    reader.onload = (f) => {
                        this.imageSource = f.target.result;
                        this.isDragging = false;
                        this.isOK = true;
                        this.filename = file.name;
                        this.filesize = file.size / 1024;
                        sessionStorage.imageSource = this.imageSource;
                        sessionStorage.filename = this.filename;
                        sessionStorage.filesize = this.filesize;
                        this.$store.commit('recsClear');
                    };
                    reader.readAsDataURL(file);
                } else {
                    this.wrongFile = true;
                    this.imageSource = null;
                    this.isDragging = false;
                }
            }
        },
        reset() {
            this.filename = null;
            this.filesize = 0;
            this.preview = null;
            this.isOK = false;
            this.wrongFile = false;
            sessionStorage.imageSource = '';
            sessionStorage.filename = null;
            sessionStorage.filesize = 0;
            sessionStorage.isUploaded = false;
            this.$refs.inputFile.value = '';
            this.$store.commit('recsClear');
        },
        openfolder() {
            this.$refs.inputFile.click();
        },
        handleFileInputChange(event) {
            this.$store.commit('recsClear');
            sessionStorage.removeItem('imageSource');
            let file = event.target.files[0];
            if (file && file.type === 'application/json') {
                let reader = new FileReader();
                reader.onload = () => {
                    try {
                        let data = JSON.parse(reader.result);
                        if (data.image) {
                            this.isDragging = false;
                            this.isOK = true;
                            sessionStorage.setItem('imageSource', `data:image/jpeg;base64,${data.image}`);
                            sessionStorage.setItem('filename', data.template_name);
                            sessionStorage.setItem('filesize', data.image.length / 1024);
                            data.points_list.forEach((item) => {
                                this.$store.commit('recsUpdate', {
                                    type: item.type,
                                    data: {
                                        startPointX: item.points[0][0],
                                        startPointY: item.points[0][1],
                                        endPointX: item.points[2][0],
                                        endPointY: item.points[2][1],
                                        name: item.tag,
                                        scaleX: 1,
                                        scaleY: 1,
                                        width: item.points[2][0] - item.points[0][0],
                                        height: item.points[2][1] - item.points[0][1],
                                        canDelete: true,
                                        canEdit: true,
                                        canSave: false
                                    }
                                });
                            });
                            this.$store.commit('templateNameUpdate', data.template_name);
                            this.filename = data.template_name;
                            this.filesize = data.image.length / 1024;
                            this.imageSource = `data:image/jpeg;base64,${data.image}`;
                            this.isFileUploaded = !this.isFileUploaded;
                        }
                    } catch (error) {
                        console.error('Error parsing JSON data:', error);
                    }
                };
                reader.readAsText(file);
            } else {
                ElMessage({
                    type: 'error',
                    message: '請上傳正確的設定檔'
                });
            }
            this.$refs.fileInput.value = '';
        }
    },
    props: {
        isUploaded: {
            type: Boolean,
            default: false
        }
    }
};
</script>
<template>
    <div class="container col-12" :class="getClasses" @dragover.prevent="dragOver" @dragleave.prevent="dragLeave" @drop.prevent="drop($event)">
        <div class="col-12 text-center">
            <h1 class="mb-3">上傳圖檔</h1>
        </div>

        <div class="file-input-container">
            <label class="file-input-label">
                選擇設定檔
                <input type="file" ref="fileInput" accept=".json" @change="handleFileInputChange" />
            </label>
        </div>

        <Button type="button" label="選擇圖檔" @click="openfolder" class="pi p-button-outlined" style="width: 12em; height: 4em">
            <label for="my-file">選擇圖檔</label>
        </Button>
        <input type="file" accept="image/*" @change="selectImg" class="form-control-file" id="my-file" ref="inputFile" style="display: none" />
        <div class="col-12 text-center" v-if="isOK && !wrongFile" :key="this.isFileUploaded">
            <Image v-if="this.imageSource" :src="this.imageSource" alt="Image" width="500" preview />
            <p class="mb-0 text-left">檔案名稱： {{ this.filename }}</p>
            <p class="mb-0 text-left">檔案大小： {{ this.showFileSize }} KB</p>
        </div>
        <div class="my-content flex justify-content-center align-items-center" v-if="wrongFile" style="color: black; height: 500px; font-size: 25px">請上傳正確檔案格式</div>
        <div class="my-content flex justify-content-center align-items-center" v-if="!isOK && !wrongFile" style="color: black; height: 500px; font-size: 25px">請拖曳圖片</div>
    </div>
    <div class="col-12 mt-3 text-center">
        <Button label="清除圖檔" class="pi p-button-info" @click="reset" style="width: 12em; height: 4em"></Button>
    </div>
</template>
<style scoped>
.file-input-container {
    display: inline-block;
    position: relative;
    width: 12em;
    height: 4em;
}

.file-input-label {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #409eff;
    color: #fff;
    font-size: 16px;
    padding: 12px 24px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    width: 100%;
    height: 100%;
}

.file-input-label:hover {
    background-color: #66b1ff;
}

.el-icon-upload {
    font-size: 24px;
    margin-right: 8px;
    background-color: #fff;
    padding: 4px;
    border-radius: 50%;
    color: #409eff;
}
/* Hide the default file input */
input[type='file'] {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}
</style>
