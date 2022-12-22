<template>
    <div class="grid p-fluid">
        <div class="col-12 md:col-9">
            <div class="card">
                <el-upload :file-list="fileList" 
                           list-type="picture-card" 
                           :on-change="fileChange" 
                           :on-remove="handleRemove" 
                           :auto-upload="false" 
                           :on-preview="handlePictureCardPreview"
                           accept="image/*">
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
                        <h5>選擇語言</h5>
                    </div>
                    <div class="flex justify-content-start mb-5">
                        <Dropdown v-model="selectedLang" :options="languages" optionLabel="name" placeholder="請選擇" />
                    </div>
                    <div class="flex justify-content-start mb-1">
                        <h5>使用高精準度模型</h5>
                    </div>
                    <div class="flex justify-content-start mb-1">
                        <p>注意：當您使用高精準模型時耗時會較久</p>
                    </div>
                    <div class="flex justify-content-start mb-5">
                        <el-switch
                            v-model="switchValue"
                            inline-prompt
                            active-text="是"
                            inactive-text="否"
                        />
                    </div>
                    <div class="flex justify-content-start mb-1">
                        <el-button type="primary" class="mr-2 mb-2" @click="submit" :disabled="disableUpload"> 圖檔提交 </el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios"
import { ElLoading } from 'element-plus'
    
export default {
    name: 'GeneralUploadImage',
    props: ['nextStepEmit'],
    data() {
        return {
            selectedLang: null,
            languages: [
                { name: '繁體中文', code: 'Chinese' },
            ],
            nestedRouteItems: [
                {
                    label: '圖檔上傳',
                    to: '/features/general'
                },
                {
                    label: '單張結果確認',
                    to: '/features/general/step2'
                }
            ],
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
            dialogWidth: '',
        };
    },
    watch: {
        switchValue: function(newVal){
            if (newVal){
                this.image_complexity = 'high';
            } else {
                this.image_complexity = 'medium';
            }
        }
    },
    computed: {
        disableUpload() {
            if (this.fileList.length === 0 | this.selectedLang===null) {
                return true;
            } else {
                return false;
            }
        },
    },
    methods: {
        async submit() {
            const loading = ElLoading.service({
                            lock: true,
                            text: 'Loading',
                            background: 'rgba(0, 0, 0, 0.7)',
                        })
            this.$store.commit('generalImageUpdate', this.fileList);
            // 前綴拿掉
            const base64Image = this.fileList[0].reader.split(',')[1]
            // 打 API
            axios.post("/ocr/gpocr", {
                                "image": base64Image,
                                "image_complexity": this.image_complexity,
                                "language": this.selectedLang.code,
                            })
                            .then( (response) =>
                               {this.status = response.status;
                                this.response = response;
                                console.log(response)
                                this.$store.commit('generalImageResponse', response);
                                })
                            .catch( (error) => {
                                console.log(error)
                                if(error.code === 'ERR_NETWORK'){
                                    this.status = 'network';
                                }
                })
            setTimeout(()=>{
                // 下一步
                this.$emit('nextStepEmit', 2)
                this.$emit('uploadConfig', this.image_complexity, this.selectedLang.code)
                loading.close()
            }, 2000)
        },
        fileChange(file, resfileList) {
            // allows image only
            if (file.raw.type.indexOf('image/') >= 0) {
                    var reader = new FileReader();
                    reader.onload = (f) => {
                        this.imageSource = f.target.result;
                        file.reader = f.target.result;
                    };
                    reader.readAsDataURL(file.raw);
                    this.fileList.push(file)
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
