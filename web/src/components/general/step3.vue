<template>
    <div class="grid p-fluid">
        <div class="col-12" >
            <div class="card" style="overflow-x:scroll;overflow-y:scroll; height: 600px;">
                <div class="flex flex-column card-container">
                    <div class="flex align-items-center justify-content-start font-bold m-2 mb-3">
                        <div class="flex">
                            <div class="flex-grow-1 flex align-items-center justify-content-center font-bold p-4 m-3">
                                <el-tooltip content="回到圖檔上傳">
                                    <el-button type="success" :icon="Back" circle @click="back"></el-button>
                                </el-tooltip>
                                <el-tooltip content="下載 excel">
                                    <el-button type="primary" :icon="Download" circle @click="downloadFile"></el-button>
                                </el-tooltip>
                            </div>
                            <div class="flex-shrink-1 md:flex-shrink-0 flex align-items-center justify-content-center font-bold p-4 m-3">
                                成功辨識：{{ this.resData.length }} 張，共耗時 {{ general_execute_time }} 秒
                            </div>
                        </div>
                    </div>
                    <div class="flex align-items-center justify-content-center font-bold m-2 mb-5">
                        <el-table
                            :data="getExcel"
                            style="width: 100%"
                        >
                            <el-table-column label="圖片預覽" width="180">
                                <template #default="scope">
                                    <el-image
                                        style="width: 120px; height: 120px;"
                                        :src="scope.row.image"
                                        :preview-src-list="[scope.row.image]"
                                        hide-on-click-modal="true"
                                        preview-teleported="true"
                                        >
                                    </el-image>
                                </template>
                            </el-table-column>
                            <el-table-column prop="filename" label="檔案名稱" sortable width="180" />
                            <el-table-column prop="ocr_results" label="辨識結果" width="700" />
                        </el-table>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
import { Download, Back } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as XLSX from 'xlsx/xlsx.mjs'

export default {
    components: {},
    name: 'General3',
    data() {
        return {
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
            console.log(this.resData)
            for (let i = 0; i < this.resData.length; i++) {
                this.excelData.push({
                    "filename": this.resData[i].fileName,
                    "image_cv_id": this.resData[i].image_cv_id,
                    "ocr_results": JSON.stringify(this.resData[i].ocr_results)
                })
                this.tableData.push({
                    "filename": this.resData[i].fileName,
                    "ocr_results": JSON.stringify(this.resData[i].ocr_results),
                    "image": `data:image/png;base64, ` + this.resData[i].base64Image
                })
            }
            return this.tableData
        },
    },
    methods: {
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