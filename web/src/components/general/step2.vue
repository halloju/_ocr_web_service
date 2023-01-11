<template>
    <div class="grid p-fluid">
        <div class="col-12 md:col-7" >
            <div class="card" style="overflow-x:scroll;overflow-y:scroll;">
                <h5>我們先看第一張圖片辨識的狀況</h5>
                <Image :src="preview" alt="Image" width="600" preview />
                <img ref="preview" />
                <div v-show="showKonva" class="" ref="img_block">
                    <div class="flex card-container overflow-hidden">
                        <v-stage ref="stage" :config="stageConfig">
                            <v-layer ref="layer">
                                <v-image
                                    :config="{
                                        width: this.imageConfig.width,
                                        height: this.imageConfig.height,
                                        image: this.image,
                                        opacity: this.imageConfig.opacity,
                                        x: this.imageConfig.x,
                                        y: this.imageConfig.y
                                    }"
                                    ref="image"
                                />
                                <Rect v-for="box in this.Boxes" :key="box.name" :boxName="box.name" :fillColor="box.fillColor" />
                            </v-layer>
                        </v-stage>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-12 md:col-5">
            <div class="card">
                <div class="flex justify-content-between align-items-center">
                    <h5>Response</h5>
                </div>
                <el-tabs v-model="activeTab" class="demo-tabs" @tab-click="handleClick">
                    <el-tab-pane label="文字" name="first">
                        <DataTable :value="regData" :scrollable="true" scrollHeight="400px" :loading="loading">
                            <Column field="index" header="編號" style="min-width:100px"></Column>
                            <Column field="text" header="文字" style="min-width:50px"></Column>
                        </DataTable>
                    </el-tab-pane>
                    <el-tab-pane label="詳細資訊" name="second">
                        <Button icon="pi pi-copy" class="p-button-text" @click="copyText"></Button>
                        <div ref="message">
                            {{regData}}
                        </div>
                    </el-tab-pane>
                </el-tabs>
                <h5>我已確認單張結果</h5>
                <el-switch
                    v-model="switchValue"
                    inline-prompt
                    active-text="是"
                    inactive-text="否"
                />
                <br>
                <Button label=" 開始辨識全部檔案" class="mr-2 mb-2 pi pi-images" @click="submit" :disabled="!switchValue"></Button>
                <Button label=" 重新上傳" class="mr-2 mb-2 pi pi-upload p-button-danger" @click="back"></Button>
                <!-- Progress Bar -->
                <el-progress
                :text-inside="true"
                :stroke-width="24"
                :percentage="uploadPercentage"
                status="success"
                color="#3b82f6"
                />
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios";
import { ElMessage, ElMessageBox } from 'element-plus'
import { ElLoading } from 'element-plus'
import Rect from '@/components/Rect.vue';
import Box from '@/components/Box.vue';

export default {
    components: {
        Box,
        Rect
    },
    name: 'General2',
    mounted() {
        this.image = new window.Image();
        this.image.src = this.$store.state.general_upload_image[0].reader;
        this.$nextTick(() => {
            this.resize = Math.min(this.$refs.img_block.clientWidth / this.image.width, this.$refs.img_block.clientHeight / this.image.height);
            })
        this.image.onload = () => {
            this.imageConfig = {
                width: this.image.width * this.resize * this.ratio,
                height: this.image.height * this.resize * this.ratio,
                x: (this.$refs.img_block.clientWidth - this.image.width * this.resize * this.ratio) / 2,
                y: (this.$refs.img_block.clientHeight - this.image.height * this.resize * this.ratio) / 2
            };
            const dataURL = this.$refs.stage.getStage().toDataURL()
            this.preview = dataURL
        };
        const fake = [ { "startPointX": 100, "startPointY": 200, "endPointX": 500, "endPointY": 250, "scaleX": 1, "scaleY": 1, "width": 100, "height": 100, "name": "example_0" }, 
                       { "startPointX": 200, "startPointY": 347, "endPointX": 376, "endPointY": 493, "scaleX": 1, "scaleY": 1, "width": 100, "height": 100, "name": "example_1" },
                       { "startPointX": 250, "startPointY": 160, "endPointX": 376, "endPointY": 493, "scaleX": 1, "scaleY": 1, "width": 100, "height": 100, "name": "example_2" } ]
        this.$store.commit('generalBoxesUpdate', fake);
        this.getRegData();
    },
    data() {
        return {
            // 前一步驟上傳的圖檔
            firstImage: this.$store.state.general_upload_image[0],
            allImage:  this.$store.state.general_upload_image,
            regData: null,
            uploadPercentage: 0,
            isDownload: false,
            switchValue: false,
            switchButton: false,
            selectButtonValue: { name: '詳細資訊' },
            selectButtonValues: [{ name: '詳細資訊' }, { name: '文字' }],
            activeTab: "first",
            Boxes: [ { "name": "general_boxes", "title": "文字辨識位置", "step": 2, "fillColor": { "r": 0, "g": 255, "b": 0, "a": 0.5 } }, ],
            preview: null,
            image: null,
            resize: null,
            showKonva: false,
            ratio: 1,
            stageConfig: {
                x: 0,
                y: 0,
                width: 800,
                height: 600
            },
            imageConfig: {
                width: 800,
                height: 600,
                x: 10,
                y: 20
            },

        };
    },
    watch: {
        selectButtonValue: function(newVal){
            if (newVal.name === '詳細資訊' ){
                this.switchButton = false;
            } else {
                this.switchButton = true;
            }
        }
    },
    computed: {
        getFile() {
            this.firstImage = this.$store.state.general_upload_image[0];
            return this.firstImage;
        },
    },
    methods: {
        previewImage() {
            const dataURL = this.$refs.stage.getStage().toDataURL()
            this.preview = dataURL
        },
        getRegData() {
            this.regData = this.$store.state.general_upload_res.data.ocr_results;
            this.regData.forEach(function(element, index) {
                element.index = index + 1;
            });
            return this.regData
        },
        copyText() {
            const range = document.createRange();
            range.selectNode(this.$refs.message);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
            document.execCommand('copy');
        },
        submit() {
            const start_time = new Date().getTime();
            console.log(this.allImage)
            const imageLen = this.allImage.length
            const stepPercentage = 100 / imageLen
            const generalImageResponseList = []

            for (let i = 0; i < imageLen; i++) {
                // 準備 responseData
                const responseData = {}
                const base64Image = this.allImage[i].reader.split(',')[1];
                const fileName =  this.allImage[i].name;
                responseData['base64Image'] = base64Image
                responseData['fileName'] = fileName
                // 一張一張打
                axios.post("/ocr/gpocr", {
                                "image": base64Image,
                                "image_complexity": 'medium',
                                "language": 'Chinese',
                            })
                            .then( (response) =>
                               {
                                responseData['ocr_results'] = response.data.ocr_results;
                                responseData['image_cv_id'] = response.data.image_cv_id;
                                generalImageResponseList.push(responseData)
                                this.uploadPercentage = (this.uploadPercentage + stepPercentage)
                                })
                            .catch( (error) => {
                                console.log(error)
                                if(error.code === 'ERR_NETWORK'){
                                    this.status = 'network';
                                }
                })
            }
            const end_time = new Date().getTime();
            const loading = ElLoading.service({
                            lock: true,
                            text: 'Loading',
                            background: 'rgba(0, 0, 0, 0.7)',
                        })
            setTimeout(()=>{
                console.log(generalImageResponseList)
                this.$store.commit('generalImageResponse', generalImageResponseList);
                const api_time = (end_time - start_time) / 1000 ;
                this.$store.commit('generalExecuteTime', api_time);
                this.$emit('nextStepEmit', 3)
                loading.close()
            }, 2000)
        },
        back(){
            ElMessageBox.confirm(
                '本次辨識結果將不保留，請問是否要繼續？',
                '警告',
                {
                confirmButtonText: '確定',
                cancelButtonText: '取消',
                type: 'warning',
                center: true,
                }
            )
                .then(() => {
                    ElMessage({
                        type: 'success',
                        message: '回到圖檔上傳',
                    })
                    this.$emit('nextStepEmit', 1)
                })
                .catch(() => {
                ElMessage({
                    type: 'info',
                    message: '操作取消',
                })
                })
        },
    }
};
</script>