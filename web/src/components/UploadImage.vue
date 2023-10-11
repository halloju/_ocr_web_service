<script>
import { ElMessage } from 'element-plus';

export default {
    name: 'UploadImage',
    created() {
        if (!this.createNew) {
            this.isOK = true;
            this.imageSource = sessionStorage.imageSource;
            this.filename = sessionStorage.filename;
            this.filesize = sessionStorage.filesize;
        }
    },
    data() {
        return {
            isDragging: false,
            wrongFile: false,
            imageSource: null,
            filename: '',
            filesize: 0,
            isOK: false,
            isFileUploaded: false,
            showUpload: true,
            fileList: [],
            dialogImageUrl: '',
            dialogVisible: false
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
                        // this.$store.commit('recsClear');
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
            // clear local storage
            sessionStorage.clear();
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
                        // this.$store.commit('recsClear');
                    };
                    reader.readAsDataURL(file);
                } else {
                    this.wrongFile = true;
                    this.imageSource = null;
                    this.isDragging = false;
                }
            }
        },
        handlePictureCardPreview(file) {
            this.dialogImageUrl = file.url;
            this.dialogVisible = true;
        },
        reset() {
            this.filename = null;
            this.filesize = 0;
            this.preview = null;
            this.isOK = false;
            this.wrongFile = false;
            sessionStorage.clear();
            this.$refs.inputFile.value = '';
            // this.$store.commit('recsClear');
        },
        openfolder() {
            this.$refs.inputFile.click();
        },
        getFillColorByRectangleType(rectangleType) {
            switch (rectangleType) {
                case 'text':
                    return '#ff0000'; // Red color for text box
                case 'box':
                    return '#00ff00'; // Green color for box
                case 'mask':
                    return '#0000ff'; // Brown color for mask box
                default:
                    return '#b0c4de'; // Default color for other types
            }
        },
        handleFileInputChange(event) {
            sessionStorage.clear();
            let file = event.target.files[0];
            if (file && file.type === 'application/json') {
                let reader = new FileReader();
                reader.onload = () => {
                    try {
                        let data = JSON.parse(reader.result);
                        let types = ['text', 'box', 'mask'];
                        if (data.image) {
                            this.isDragging = false;
                            this.isOK = true;
                            sessionStorage.setItem('imageSource', `data:image/jpeg;base64,${data.image}`);
                            sessionStorage.setItem('filename', data.template_name);
                            sessionStorage.setItem('filesize', data.image.length / 1024);
                            for (let i = 0; i < 3; i++) {
                                let bbox = data.points_list.filter((item) => item['type'] === types[i]);
                                let myShapes = [];
                                let fill = this.getFillColorByRectangleType(types[i]);
                                if (bbox.length > 0) {
                                    bbox.forEach(function (element, index) {
                                        var myContent = element.hasOwnProperty('tag') ? element['tag'] : '';
                                        const mySelect = element.hasOwnProperty('filters') ? element['filters'] : null;
                                        var label_x = element['points'][0][0];
                                        var label_y = element['points'][0][1];
                                        var label_width = element['points'][1][0] - element['points'][0][0];
                                        var label_height = element['points'][2][1] - element['points'][1][1];
                                        myShapes.push({
                                            type: 'rect',
                                            name: 'rect' + index,
                                            fill: fill,
                                            opacity: 0.5,
                                            rectangleType: element['type'],
                                            stroke: '#0000ff',
                                            draggable: true,
                                            strokeWidth: 2,
                                            strokeScaleEnabled: false,
                                            annotation: {
                                                title: myContent,
                                                filters: mySelect
                                            },
                                            x: label_x,
                                            y: label_y,
                                            width: label_width,
                                            height: label_height,
                                            scaleX: 1,
                                            scaleY: 1,
                                            rectangleType: types[i]
                                        });
                                    });
                                    sessionStorage.setItem(types[i], JSON.stringify(myShapes));
                                }
                            }

                            // Convert base64 to file and add to fileList
                            const base64Data = `data:image/jpeg;base64,${data.image}`;
                            const blob = this.dataURItoBlob(base64Data);
                            const file = new File([blob], data.template_name, { type: 'image/jpeg' });
                            this.fileList.push({ name: data.template_name, url: base64Data, raw: file });
                        }
                        this.$store.commit('templateNameUpdate', data.template_name);
                        this.filename = data.template_name;
                        this.filesize = data.image.length / 1024;
                        this.imageSource = `data:image/jpeg;base64,${data.image}`;
                        this.isFileUploaded = !this.isFileUploaded;
                        // this.createNew = false;
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
        },
        toggleUpload() {
            // console.log('toggleUpload');
            this.showUpload = !this.showUpload;
        },
        beforeUpload(file) {
            // Check file size && file type
            const isIMAGE = file.type === 'image/jpeg' || 'image/png';
            if (!isIMAGE) {
                ElMessageBox.alert('圖片只能是 JPG/PNG 格式!', '錯誤', {
                    confirmButtonText: '確定',
                    type: 'error'
                });
            }
            // Push file to fileList
            if (isIMAGE) {
                sessionStorage.clear();
                var reader = new FileReader();
                reader.onload = (f) => {
                    this.imageSource = f.target.result;
                    sessionStorage.setItem('imageSource', f.target.result);
                    // console.log(sessionStorage.getItem('imageSource'));
                    file.reader = f.target.result;
                };
                reader.readAsDataURL(file.raw);
            }

            this.showUpload = !this.showUpload;
        },

        handleRemove() {
            this.showUpload = !this.showUpload;
            sessionStorage.clear();
        },

        dataURItoBlob(dataURI) {
            const byteString = atob(dataURI.split(',')[1]);
            const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
            const ab = new ArrayBuffer(byteString.length);
            const ia = new Uint8Array(ab);
            for (let i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            return new Blob([ab], { type: mimeString });
        }
    },
    props: {
        isUploaded: {
            type: Boolean,
            default: false
        },
        createNew: {
            type: Boolean,
            default: false
        }
    }
};
</script>
<template>
    <div class="card" style="background-color: white">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px">
            <p>請選擇模板圖片，圖片選擇完成後請點選開始進行標註。</p>
            <button class="uiStyle sizeM btnGreen minLength" style="margin-right: 20px">
                選擇設定檔
                <input type="file" ref="fileInput" accept=".json" @change="handleFileInputChange" />
            </button>
        </div>
        <el-upload :file-list="fileList" list-type="picture-card" :on-change="beforeUpload" :on-remove="handleRemove" :auto-upload="false" :limit="1" accept="image/*" :class="{ hideUpload: !showUpload }" :on-preview="handlePictureCardPreview">
            <el-icon><Plus /></el-icon>
        </el-upload>
    </div>
    <el-dialog v-model="dialogVisible">
        <img :src="dialogImageUrl" alt="Preview Image" />
    </el-dialog>
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

[class='hideUpload'] div {
    display: none !important;
}
</style>
