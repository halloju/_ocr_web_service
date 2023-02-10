<script>
import axios from 'axios';
import Annotation from '@/components/Annotation.vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { ElLoading } from 'element-plus';
export default {
    components: {
        Annotation
    },
    name: 'General2',
    props: {
        image_complexity: String,
        selectedLang: String
    },
    data() {
        return {
            // 上方
            imageSrc: this.$store.state.general_upload_image[0].reader,
            localStorageKey: 'storage',
            width: 1200,
            height: 600,
            dataCallback: '',
            initialData:
                '[{"type":"rect","name":"shape-1673851677198","fill":"#b0c4de","opacity":0.5,"stroke":"#00f","draggable":true,"strokeWidth":2,"strokeScaleEnabled":false,"annotation":{"title":"要項一","text":"","linkTitle":"","link":""},"x":121.30823537700691,"y":186.11122465281173,"width": 200,"height":215.33333333333334},{"type":"rect","name":"shape-1673851944263","fill":"#b0c4de","opacity":0.5,"stroke":"#00f","draggable":true,"strokeWidth":2,"strokeScaleEnabled":false,"annotation":{"title":"要項二","text":"","linkTitle":"","link":""},"x":219.74836905871385,"y":37.62814538676607,"width":150.5125815470643,"height":150.5125815470643}]',
            initialDataId: null,
            // 下方
            switchValue: false,
            submitClick: false,
            uploadPercentage: 0,
            // 資料
            shapes: [],
            allImage: this.$store.state.general_upload_image
        };
    },
    watch: {
        selectButtonValue: function (newVal) {
            if (newVal.name === '詳細資訊') {
                this.switchButton = false;
            } else {
                this.switchButton = true;
            }
        }
    },
    computed: {
        getShapeData() {
            let myShapes = [];
            let image_cv_id = JSON.stringify(this.$store.state.general_upload_res[0].image_cv_id);
            let regData = this.$store.state.general_upload_res[0].ocr_results;
            regData.forEach(function (element, index) {
                var label = Object.values(element);
                var points = Object.values(label[0]);
                var myContent = label[1];
                var label_x = points[0][0];
                var label_y = points[0][1];
                var label_width = points[1][0] - label_x;
                var label_height = points[2][1] - label_y;
                myShapes.push({
                    type: 'rect',
                    name: image_cv_id + index,
                    fill: '#b0c4de',
                    opacity: 0.5,
                    stroke: '#0ff',
                    draggable: true,
                    strokeWidth: 2,
                    strokeScaleEnabled: false,
                    annotation: {
                        title: index + 1,
                        text: myContent,
                        linkTitle: '',
                        link: ''
                    },
                    x: label_x,
                    y: label_y,
                    width: label_width,
                    height: label_height
                });
            });
            return JSON.stringify(myShapes);
        }
    },
    methods: {
        previewImage() {
            const dataURL = this.$refs.stage.getStage().toDataURL();
            this.preview = dataURL;
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
            this.submitClick = true;
            const start_time = new Date().getTime();
            const imageLen = this.allImage.length;
            const stepPercentage = 100 / imageLen;
            const generalImageResponseList = [];
            for (let i = 0; i < imageLen; i++) {
                // 準備 responseData
                const responseData = {};
                const base64Image = this.allImage[i].reader.split(',')[1];
                const fileName = this.allImage[i].name;
                responseData['base64Image'] = base64Image;
                responseData['fileName'] = fileName;
                // 一張一張打
                axios
                    .post('/ocr/gp_ocr', {
                        image: base64Image,
                        image_complexity: this.image_complexity,
                        model_name: this.selectedLang
                    })
                    .then((response) => {
                        responseData['ocr_results'] = response.data.ocr_results;
                        responseData['image_cv_id'] = response.data.image_cv_id;
                        generalImageResponseList.push(responseData);
                        this.uploadPercentage = (this.uploadPercentage + stepPercentage).toFixed(2);
                    })
                    .catch((error) => {
                        console.log(error);
                        if (error.code === 'ERR_NETWORK') {
                            this.status = 'network';
                        }
                    });
            }
            const end_time = new Date().getTime();
            const loading = ElLoading.service({
                lock: true,
                text: 'Loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            setTimeout(() => {
                console.log(generalImageResponseList);
                this.$store.commit('generalImageResponse', generalImageResponseList);
                const api_time = (end_time - start_time) / 1000;
                this.$store.commit('generalExecuteTime', api_time);
                this.$emit('nextStepEmit', 3);
                loading.close();
            }, 2000);
        },
        back() {
            ElMessageBox.confirm('本次辨識結果將不保留，請問是否要繼續？', '警告', {
                confirmButtonText: '確定',
                cancelButtonText: '取消',
                type: 'warning',
                center: true
            })
                .then(() => {
                    ElMessage({
                        type: 'success',
                        message: '回到圖檔上傳'
                    });
                    this.$emit('nextStepEmit', 1);
                })
                .catch(() => {
                    ElMessage({
                        type: 'info',
                        message: '操作取消'
                    });
                });
        }
    }
};
</script>
<template>
    <div class="grid p-fluid">
        <div class="col-12">
            <div class="card" style="overflow-x: scroll; overflow-y: scroll">
                <h5>我們先看第一張圖片辨識的狀況</h5>
                <Annotation containerId="my-pic-annotation-output" :editMode="false" :imageSrc="imageSrc" :width="width" :height="height" dataCallback="" :initialData="getShapeData" :initialDataId="initialDataId" :justShow="true"></Annotation>
                <h5>我已確認單張結果，包含以上所有要項</h5>
                <el-switch v-model="switchValue" inline-prompt active-text="是" inactive-text="否" style="width: 150px" />
                <br />
                <el-button type="primary" style="width: 150px" class="mr-2 mb-2" @click="submit" :disabled="!switchValue"> 開始辨識全部檔案 </el-button>
                <el-button type="danger" style="width: 150px" class="mr-2 mb-2 pi pi-upload" @click="back"> 重新上傳 </el-button>
                <!-- Progress Bar -->
                <el-progress v-show="submitClick" :text-inside="true" :stroke-width="24" :percentage="uploadPercentage" status="success" color="#3b82f6" />
            </div>
        </div>
    </div>
</template>
<style>
.el-button {
    margin-left: 0px !important;
}
</style>
