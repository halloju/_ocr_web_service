<script>
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
            // 下方
            containerId: 'my-pic-annotation',
            imageSrc: null,
            imageResult: '',
            localStorageKey: 'storage',
            width: 1200,
            height: 600,
            dataCallback: '',
            initialData: '',
            initialDataId: null,
            // 上方
            isDownload: false,
            // general_upload_res: this.$store.state.general_upload_res,
            general_execute_time: this.$store.state.general_execute_time,
            Download: Download,
            Back: Back,
            excelData: [],
            tableData: [],
            reloadAnnotator: false,
            isRunning: false,
            finishedStatus: ['SUCCESS', 'FAIL']
        };
    },
    watch: {
        tableData(newTableData, oldTableData) {
            console.debug(newTableData);
        }
    },
    computed: {
        getTaskData() {
            this.excelData = [];
            this.tableData = [];
            this.general_upload_res.forEach((item, index) => {
                this.excelData.push({
                    filename: item.file_name,
                    image_id: item.image_id,
                    ocr_results: item.ocr_results
                });
                this.tableData.push({
                    num: index + 1 ,
                    task_id: item.task_id,
                    status: item.status,
                    image_id: item.image_id,
                    file_name: item.file_name,
                    isFinished: item.status === 'SUCCESS' ? true : false
                });
            });
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
        getStatusColor(status) {
            switch (status) {
                case 'SUCCESS':
                    return 'success';
                case 'PENDING':
                    return 'gray';
                default:
                    return '';
            }
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
            axios.get(`/ocr/status/${this.general_upload_res[item].task_id}`).then(async (res) => {
                if (res.data.status === 'SUCCESS') {
                    await this.getOcrResults(item);
                } else {
                    this.$store.commit('generalImageOcrStatus', { item: item, status: res.data.status });
                }
            });
        },
        async getOcrResults(item) {
            axios.get(`/ocr/result/${this.general_upload_res[item].task_id}`).then((res) => {
                if (res.data.status === 'SUCCESS') {
                    this.$store.commit('generalImageOcrResults', { item: item, ocr_results: res.data.result, file_name: res.data.file_name});
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
            axios.get(`/ocr/get_image/${row.image_id}`).then((res) => {
                if (res !== null) {
                    this.imageSrc = 'data:image/png;base64,' + res.data;
                } else {
                    this.imageSrc = '';
                }
            });
            axios.get(`/ocr/result/${row.task_id}`).then((res) => {
                if (res !== null) {
                    this.initialData = this.getShapeData(res.data.result);
                }
            });
        },
        async waitUntilOcrComplete() {
            this.isRunning = true;
            let count = 0;
            while (this.isRunning) {
                const unfinishedItems = this.general_upload_res.filter(item => !this.finishedStatus.includes(item.status));
                for (let i = 0; i < unfinishedItems.length; i++) {
                    const item = unfinishedItems[i];
                    await this.getOcrStatus(this.general_upload_res.indexOf(item));
                }
                if (unfinishedItems.length === 0) {
                    this.isRunning = false;
                    break;
                }
                await new Promise(resolve => setTimeout(resolve, 3000)); // wait 2 seconds before polling again
                count++;
                // 這個數字太小可能也跑不完？感覺要衡量一下
                if (count === 30) break;
            }
        },
        getShapeData(regData) {
            let myShapes = [];
            // 使用正規表達式將 regData 中的所有 ' 符號替換為 " 符號
            regData = JSON.parse(regData.replace(/'/g, '"'));
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
            return JSON.stringify(myShapes);
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
                                <el-table :data="getTaskData" style="width: 100%" :key="isRunning">
                                    <el-table-column prop="num" label="號碼" sortable width="100" />
                                    <el-table-column prop="file_name" label="檔名" sortable width="200" />
                                    <el-table-column prop="status" label="辨識狀態" width="180">
                                        <template #default="{row}">
                                            <el-tag :type="getStatusColor(row.status)">{{ row.status }}</el-tag>
                                        </template>
                                    </el-table-column>
                                    <el-table-column label="動作">
                                        <template v-slot="scope">
                                            <el-button type="primary" v-if="scope.row.isFinished" @click="handleButtonClick(scope.row)" round>檢視</el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>
                        </div>
                        <div v-if="imageSrc!==null">
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
