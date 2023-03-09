<script>
import Image from '@/assets/img/hero-img.png';
import Annotation from '@/components/Annotation.vue';
import { Download, Back } from '@element-plus/icons-vue';
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import * as XLSX from 'xlsx/xlsx.mjs';
import { mapState } from 'vuex';
export default {
    components: {
        Annotation
    },
    name: 'General3',
    data() {
        return {
            // 上方
            containerId: 'my-pic-annotation',
            imageSrc: Image,
            imageResult: "",
            localStorageKey: 'storage',
            width: 1200,
            height: 600,
            dataCallback: '',
            initialData:
                '[{"type":"rect","name":"shape-1673851677198","fill":"#b0c4de","opacity":0.5,"stroke":"#00f","draggable":true,"strokeWidth":2,"strokeScaleEnabled":false,"annotation":{"title":"要項一","text":"","linkTitle":"","link":""},"x":121.30823537700691,"y":186.11122465281173,"width": 200,"height":215.33333333333334},{"type":"rect","name":"shape-1673851944263","fill":"#b0c4de","opacity":0.5,"stroke":"#00f","draggable":true,"strokeWidth":2,"strokeScaleEnabled":false,"annotation":{"title":"要項二","text":"","linkTitle":"","link":""},"x":219.74836905871385,"y":37.62814538676607,"width":150.5125815470643,"height":150.5125815470643}]',
            initialDataId: null,
            // 下方
            isDownload: false,
            // general_upload_res: this.$store.state.general_upload_res,
            general_execute_time: this.$store.state.general_execute_time,
            Download: Download,
            Back: Back,
            excelData: [],
            tableData: [],
            reloadAnnotator: false,
            isRunning: false
        };
    },
    computed: {
        getExcel() {
            // this.excelData = [];
            this.tableData.length = 0;
            this.general_upload_res.forEach((item, index) => {
                this.tableData.push({
                    task_id: item.task_id,
                    status: item.status,
                    image_id: item.image_id,
                    isFinished: item.status === 'SUCCESS' ? true : false
                });
            });
            console.log(this.general_upload_res);
            return this.tableData;
        },
        ...mapState(['general_upload_res'])
    },
    methods: {
        callback(data, image_cv_id) {
            for (let i = 0; i < this.general_upload_res.length; i++) {
                if (image_cv_id === this.general_upload_res[i].image_id) {
                    for (let j = 0; j < this.general_upload_res[i].ocr_results.length; j++) {
                        this.general_upload_res[i].ocr_results[j].text = data[j].annotation.text;
                    }
                    break;
                }
            }
            console.log(this.general_upload_res);
        },
        getImage(item) {
            axios.get(`http://localhost:5000/ocr/get_image/${this.general_upload_res[item - 1].image_id}`).then((res) => {
                console.log('getImage', res);
                if (res.status === 200) {
                    let ImageSrc = 'data:image/png;base64,' + res.data.image_string;
                    return ImageSrc;
                } else {
                    ElMessage({
                        message: '辨識中，請稍後',
                        type: 'warning'
                    });
                }
            });
        },
        async getOcrStatus(item) {
            axios.get(`http://localhost:5000/ocr/status/${this.general_upload_res[item].task_id}`).then(async (res) => {
                if (res.data.status === 'SUCCESS') {
                    await this.getOcrResults(item);
                } else {
                    this.$store.commit('generalImageOcrStatus', { item: item, status: res.data.status });
                }
            });
        },
        async getOcrResults(item) {
            axios.get(`http://localhost:5000/ocr/result/${this.general_upload_res[item].task_id}`).then((res) => {
                if (res.data.status === 'SUCCESS') {
                    this.$store.commit('generalImageOcrResults', { item: item, ocr_results: res.data.result });
                } else {
                    ElMessage({
                        message: '辨識失敗',
                        type: 'warning'
                    });
                }
                this.$store.commit('generalImageOcrStatus', { item: item, status: res.data.status });
                this.reloadAnnotator = !this.reloadAnnotator;
            });
        },
        handleButtonClick(row) {
            console.log(row);
            axios.get(`/ocr/get_image/${row.image_id}`).then((res) => {
                if (res !== null) {
                    this.imageSrc = 'data:image/png;base64,' + res.data;
                } else {
                    this.imageSrc = "";
                }
                console.log("Success")
            });
            axios.get(`/ocr/result/${row.task_id}`).then((res) => {
                if (res !== null) {
                    console.log(res.data.result)
                    let test = this.getShapeData(res.data.result);
                    console.log(test);
                }
                console.log("Success2")
            });
        },
        async pollForResult() {
            this.isRunning = true;
            while (this.isRunning) {
                const response = await this.getOcrStatus();
                const data = await response.json();
                if (data.isDone) {
                    this.result = data.result;
                    this.isRunning = false;
                    break;
                }
                await new Promise((resolve) => setTimeout(resolve, 1000)); // wait 1 second before polling again
            }
        },
        async waitUntilOcrComplete() {
            this.isRunning = true;
            while (this.isRunning) {
                this.general_upload_res
                    .filter((item) => item.status === 'PROCESSING')
                    .forEach(async (item, index) => {
                        await this.getOcrStatus(index);
                    });
                if (this.general_upload_res.filter((item) => item.status === 'PROCESSING').length === 0) {
                    this.isRunning = false;
                    break;
                }
                await new Promise((resolve) => setTimeout(resolve, 1000)); // wait 1 second before polling again
            }
        },
        getShapeData(regData) {
            let myShapes = [];
            regData = JSON.parse(regData);
            console.log(typeof(regData))
            let image_cv_id = JSON.stringify(this.$store.state.general_upload_res[item - 1].image_id);
            regData.forEach(function (element, index) {
                var label = Object.values(element);
                var points = Object.values(label[0]);
                var myContent = label[1];
                var label_x = points[0][0];
                var label_y = points[0][1];
                var label_width = points[1][0] - label_x;
                var label_height = points[2][1] - label_y;
                var image_cv_id = label[2];
                myShapes.push({
                    type: 'rect',
                    name: image_cv_id,
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
            this.reloadAnnotator[item] = true;
            return myShapes;
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
        },
        downloadFile() {
            const jsonWorkSheet = XLSX.utils.json_to_sheet(this.excelData);
            const workBook = {
                SheetNames: ['jsonWorkSheet'],
                Sheets: {
                    jsonWorkSheet: jsonWorkSheet
                }
            };
            XLSX.writeFile(workBook, '通用辨識結果.xlsx');
        }
    },
    created() {
        this.waitUntilOcrComplete();
    }
};
</script>

<template>
    <div class="grid p-fluid">
        <div class="col-12">
            <div class="card" style="overflow-x: scroll; overflow-y: scroll; height: 860px">
                <div class="flex flex-column card-container">
                    <div class="flex align-items-center justify-content-start font-bold m-2 mb-3">
                        <div class="flex">
                            <div class="flex-grow-1 flex align-items-center justify-content-center font-bold p-4 m-3">
                                <el-tooltip content="回到圖檔上傳">
                                    <el-button class="my-button" type="success" :icon="Back" circle @click="back"></el-button>
                                </el-tooltip>
                                <el-tooltip content="下載 excel">
                                    <el-button class="my-button" type="primary" :icon="Download" circle @click="downloadFile"></el-button>
                                </el-tooltip>
                            </div>
                            <div class="flex-shrink-1 md:flex-shrink-0 flex align-items-center justify-content-center font-bold p-4 m-3">成功辨識：{{ this.general_upload_res.length }} 張，共耗時 {{ general_execute_time }} 秒</div>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="card">
                            <div class="flex align-items-center justify-content-center font-bold m-2 mb-5">
                                <el-table :data="getExcel" style="width: 100%" :key="isRunning">
                                    <el-table-column prop="task_id" label="任務" sortable width="180" />
                                    <el-table-column prop="status" label="辨識結果" width="180" />
                                    <el-table-column label="Action">
                                        <template v-slot="scope">
                                            <el-button v-if="scope.row.isFinished" @click="handleButtonClick(scope.row)">View</el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>
                        </div>
                        <Annotation
                            containerId="my-pic-annotation-output"
                            :imageSrc="imageSrc"
                            :editMode="false"
                            :language="en"
                            :width="width"
                            :height="height"
                            dataCallback=""
                            :initialData="initialData"
                            initialDataId=""
                            image_cv_id=""
                        ></Annotation>
                    </div>
                </div>
            </div>
        </div>
        <!-- <div class="col-12">
            <div class="card">
                <div class="flex align-items-center justify-content-center font-bold m-2 mb-5">
                    <el-table :data="getExcel" style="width: 100%">
                        <el-table-column label="圖片預覽" width="180">
                            <template #default="scope">
                                <el-image style="width: 120px; height: 120px" :src="scope.row.image" :preview-src-list="[scope.row.image]" hide-on-click-modal="true" preview-teleported="true"> </el-image>
                            </template>
                        </el-table-column>
                        <el-table-column prop="filename" label="檔案名稱" sortable width="180" />
                        <el-table-column prop="ocr_results" label="辨識結果" width="700" />
                    </el-table>
                </div>
            </div>
        </div> -->
    </div>
</template>
<style scoped>
.my-button {
    margin: 10px;
}
.el-carousel {
    width: 1200px;
}
.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}
.el-carousel__item:nth-child(2n + 1) {
    background-color: #d3dce6;
}
</style>
