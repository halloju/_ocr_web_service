<script>
import Annotation from '@/components/Annotation.vue';
import { Download, Back } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import * as XLSX from 'xlsx/xlsx.mjs';

export default {
    components: {
        Annotation
    },
    name: 'General3',
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
            isDownload: false,
            resData: this.$store.state.general_upload_res,
            general_execute_time: this.$store.state.general_execute_time,
            Download: Download,
            Back: Back,
            excelData: [],
            tableData: []
        };
    },
    computed: {
        getExcel() {
            this.excelData = [];
            this.tableData = [];
            for (let i = 0; i < this.resData.length; i++) {
                this.excelData.push({
                    filename: this.resData[i].fileName,
                    image_cv_id: this.resData[i].image_cv_id,
                    ocr_results: JSON.stringify(this.resData[i].ocr_results)
                });
                this.tableData.push({
                    filename: this.resData[i].fileName,
                    ocr_results: JSON.stringify(this.resData[i].ocr_results),
                    image: `data:image/png;base64, ` + this.resData[i].base64Image
                });
            }
            return this.tableData;
        }
    },
    methods: {
        callback(data, image_cv_id) {
            console.log(data);
            console.log(image_cv_id);
            console.log(this.resData);
            for (let i = 0; i < this.resData.length; i++) {
                if (image_cv_id === this.resData[i].image_cv_id) {
                    for (let j = 0; j < this.resData[i].ocr_results.length; j++) {
                        this.resData[i].ocr_results[j].text = data[j].annotation.text;
                    }
                    break;
                }
            }
            console.log(this.resData);
        },
        getImage(item) {
            let ImageSrc = this.$store.state.general_upload_image[item - 1].reader;
            return ImageSrc;
        },
        getShapeData(item) {
            console.log('item:', item);
            let myShapes = [];
            console.log(this.$store.state.general_upload_res);
            let regData = this.$store.state.general_upload_res[item - 1].ocr_results;
            let image_cv_id = JSON.stringify(this.$store.state.general_upload_res[item - 1].image_cv_id);
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
                            <div class="flex-shrink-1 md:flex-shrink-0 flex align-items-center justify-content-center font-bold p-4 m-3">成功辨識：{{ this.resData.length }} 張，共耗時 {{ general_execute_time }} 秒</div>
                        </div>
                    </div>
                    <div class="flex align-items-center justify-content-center font-bold m-2 mb-5">
                        <el-carousel trigger="click" :autoplay="false" height="650px" indicator-position="outside">
                            <el-carousel-item v-for="item in this.resData.length" :key="item" style="overflow: scroll">
                                <h3> 第 {{item}} 張</h3>
                                <Annotation
                                    containerId="my-pic-annotation-output"
                                    :editMode="false"
                                    :language="en"
                                    :imageSrc="getImage(item)"
                                    :width="width"
                                    :height="height"
                                    :dataCallback="callback"
                                    :initialData="getShapeData(item)"
                                    :initialDataId="initialDataId"
                                    :image_cv_id="this.resData[item - 1].image_cv_id"
                                ></Annotation>
                            </el-carousel-item>
                        </el-carousel>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-12">
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
        </div>
    </div>
</template>

<script>
import Annotation from '@/components/Annotation.vue';
import { Download, Back } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as XLSX from 'xlsx/xlsx.mjs'

export default {
    components: {
        Annotation
    },
    name: 'General3',
    data() {
        return {
            // 上方
            imageSrc: this.$store.state.general_upload_image[0].reader,
            localStorageKey: "storage",
            width: 1200,
            height: 600,
            dataCallback: '',
            initialData: '[{"type":"rect","name":"shape-1673851677198","fill":"#b0c4de","opacity":0.5,"stroke":"#00f","draggable":true,"strokeWidth":2,"strokeScaleEnabled":false,"annotation":{"title":"要項一","text":"","linkTitle":"","link":""},"x":121.30823537700691,"y":186.11122465281173,"width": 200,"height":215.33333333333334},{"type":"rect","name":"shape-1673851944263","fill":"#b0c4de","opacity":0.5,"stroke":"#00f","draggable":true,"strokeWidth":2,"strokeScaleEnabled":false,"annotation":{"title":"要項二","text":"","linkTitle":"","link":""},"x":219.74836905871385,"y":37.62814538676607,"width":150.5125815470643,"height":150.5125815470643}]',
            initialDataId: null,
            // 下方
            isDownload: false,
            resData: this.$store.state.general_upload_res,
            general_execute_time: this.$store.state.general_execute_time,
            Download: Download,
            Back: Back,
            excelData: [],
            tableData: []
        };
    },
    computed: {
        getExcel() {
            this.excelData = []
            this.tableData = []
            for (let i = 0; i < this.resData.length; i++) {
                this.excelData.push({
                    "filename": this.resData[i].fileName,
                    "image_cv_id": this.resData[i].image_cv_id,
                    "ocr_results": JSON.stringify(this.resData[i].ocr_results)
                })
                this.tableData.push({
                    "filename": this.resData[i].fileName,
                    "ocr_results": JSON.stringify(this.resData[i].ocr_results),
                    "image": `data:image/png;base64, ` + this.resData[i].base64Image,
                })
            }
            return this.tableData
        },
    },
    methods: {
        callback(data, image_cv_id) {
            for (let i = 0; i < this.resData.length; i++) {

                if (image_cv_id === this.resData[i].image_cv_id) {
                    for (let j = 0; j < this.resData[i].ocr_results.length; j++) {
                        this.resData[i].ocr_results[j].text = data[j].annotation.text;
                    }
                    break
                }
            }
            console.log(this.resData)
        },
        getImage(item) {
            let ImageSrc = 'data:image/png;base64,' + this.resData[item-1].base64Image;
            return ImageSrc
        },
        getShapeData(item) {
            let myShapes = []
            let regData = this.$store.state.general_upload_res[item-1].ocr_results;
            let image_cv_id = JSON.stringify(this.$store.state.general_upload_res[item-1].image_cv_id);
            regData.forEach(function(element, index) {
                var label = Object.values(element);
                var points = Object.values(label[0]);
                var myContent = label[1];
                var label_x = points[0][0];
                var label_y = points[0][1];
                var label_width = points[1][0] - label_x ;
                var label_height = points[2][1] - label_y ;
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
                        title: index+1,
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
            return JSON.stringify(myShapes)
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
        downloadFile() {
            const jsonWorkSheet = XLSX.utils.json_to_sheet(this.excelData);
            const workBook = {
                SheetNames: ['jsonWorkSheet'],
                Sheets: {
                    'jsonWorkSheet': jsonWorkSheet,
                }
            }
            XLSX.writeFile(workBook, "通用辨識結果.xlsx");
        },
    }
};
</script>
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
