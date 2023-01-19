<script>
import { Download, Back } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import * as XLSX from 'xlsx/xlsx.mjs';

export default {
    components: {},
    name: 'General3',
    data() {
        return {
            isDownload: false,
            regData: this.$store.state.general_upload_res,
            general_execute_time: this.$store.state.general_execute_time,
            Download: Download,
            Back: Back,
            excelData: []
        };
    },
    computed: {
        getExcel() {
            for (let i = 0; i < this.regData.length; i++) {
                this.excelData.push({
                    image_cv_id: this.regData[i].image_cv_id,
                    ocr_results: JSON.stringify(this.regData[i].ocr_results)
                });
            }
            return this.excelData;
        }
    },
    methods: {
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
            <div class="card" style="overflow-x: scroll; overflow-y: scroll; height: 600px">
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
                            <div class="flex-shrink-1 md:flex-shrink-0 flex align-items-center justify-content-center font-bold p-4 m-3">成功辨識：{{ this.regData.length }} 張，共耗時 {{ general_execute_time }} 秒</div>
                        </div>
                    </div>
                    <div class="flex align-items-center justify-content-center font-bold m-2 mb-5">
                        <el-table :data="getExcel" style="width: 100%">
                            <el-table-column prop="image_cv_id" label="image_cv_id" sortable width="180" />
                            <el-table-column prop="ocr_results" label="ocr_results" width="700" />
                        </el-table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
