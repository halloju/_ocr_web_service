<script>
export default {
    name: 'UploadImage',
    created() {
        console.log('created');
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
            isOK: false
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
        },
        openfolder() {
            this.$refs.inputFile.click();
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

        <Button type="button" label="選擇圖檔" @click="openfolder" class="pi p-button-outlined" style="width: 12em; height: 4em">
            <label for="my-file">選擇圖檔</label>
        </Button>
        <input type="file" accept="image/*" @change="selectImg" class="form-control-file" id="my-file" ref="inputFile" style="display: none" />
        <div class="col-12 text-center" v-if="isOK && !wrongFile">
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
