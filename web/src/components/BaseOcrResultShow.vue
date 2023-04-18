<script>
import { ref, computed, onMounted } from 'vue';
import Annotation from '@/components/Annotation.vue';
import { Download, Back } from '@element-plus/icons-vue';
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import * as XLSX from 'xlsx/xlsx.mjs';
import { PULL_INTERVAL, MAX_RETRIES } from '@/constants.js';
import { useStore } from 'vuex';
import useAnnotator from '@/mixins/useAnnotator.js';

export default {
    components: {
        Annotation
    },
    name: 'BaseOcrResultShow',
    setup(props, { emit }) {
        const { parseOcrDetail } = useAnnotator();
        const store = useStore();

        const containerId = ref('my-pic-annotation');
        const imageSrc = ref(null);
        const imageResult = ref('');
        const localStorageKey = ref('storage');
        const width = ref(1200);
        const height = ref(600);
        const dataCallback = ref('');
        const initialData = ref('');
        const initialDataId = ref(null);
        const file_name = ref('');
        const num = ref('');
        const isDownload = ref(false);
        const excelData = ref([]);
        const tableData = ref([]);
        const reloadAnnotator = ref(false);
        const isRunning = ref(false);
        const finishedStatus = ref(['SUCCESS', 'FAIL']);
        const general_upload_res = computed(() => store.state.general_upload_res);
        const getTaskData = computed(() => {
            excelData.value = [];
            tableData.value = [];
            general_upload_res.value.forEach((item, index) => {
                excelData.value.push({
                    filename: item.file_name,
                    image_id: item.image_id,
                    ocr_results: JSON.stringify(item.ocr_results)
                });
                tableData.value.push({
                    num: index + 1,
                    task_id: item.task_id,
                    status: item.status,
                    image_id: item.image_id,
                    file_name: item.file_name,
                    isFinished: item.status === 'SUCCESS' ? true : false
                });
            });
            return tableData.value;
        });

        function callback(data, image_cv_id) {
            for (let i = 0; i < general_upload_res.value.length; i++) {
                if (image_cv_id === general_upload_res[i].image_id) {
                    for (let j = 0; j < general_upload_res[i].ocr_results.length; j++) {
                        general_upload_res[i].ocr_results[j].text = data[j].annotation.text;
                    }
                    break;
                }
            }
        }

        function getStatusColor(status) {
            switch (status) {
                case 'SUCCESS':
                    return 'success';
                case 'PENDING':
                    return 'gray';
                default:
                    return '';
            }
        }

        async function getOcrStatus(item) {
            axios
                .get(`/task/status/${general_upload_res.value[item].task_id}`)
                .then(async (res) => {
                    console.log('getOcrStatus', res);
                    if (res.data.status === 'SUCCESS') {
                        await getOcrResults(item);
                    } else {
                        console.log('getOcrResults', res.data.status);
                        store.commit('generalImageOcrStatus', { item: item, status: res.data.status });
                    }
                })
                .catch((res) => {
                    console.log('getOcrStatus', res);
                    ElMessage({
                        message: '辨識失敗',
                        type: 'warning'
                    });
                });
        }

        async function getOcrResults(item) {
            axios
                .get(`/task/result/${general_upload_res.value[item].task_id}`)
                .then((res) => {
                    if (res.data.status === 'SUCCESS') {
                        store.commit('generalImageOcrResults', { item: item, ocr_results: res.data.result, file_name: res.data.file_name });
                    } else {
                        ElMessage({
                            message: '辨識失敗',
                            type: 'warning'
                        });
                    }
                    store.commit('generalImageOcrStatus', { item: item, status: res.data.status });
                    reloadAnnotator.value = !reloadAnnotator.value;
                })
                .catch((res) => {
                    console.log('getOcrResults', res);
                    ElMessage({
                        message: '辨識失敗',
                        type: 'warning'
                    });
                });
        }

        async function waitUntilOcrComplete() {
            isRunning.value = true;
            let count = 0;
            while (isRunning) {
                const unfinishedItems = general_upload_res.value.filter((item) => !finishedStatus.value.includes(item.status));
                for (let i = 0; i < unfinishedItems.length; i++) {
                    const item = unfinishedItems[i];
                    await getOcrStatus(general_upload_res.value.indexOf(item));
                }
                if (unfinishedItems.length === 0) {
                    isRunning.value = false;
                    break;
                }
                await new Promise((resolve) => setTimeout(resolve, PULL_INTERVAL)); // wait 2 seconds before polling again
                count++;
                // 這個數字太小可能也跑不完？感覺要衡量一下
                if (count === MAX_RETRIES) break;
            }
        }

        // ocr 結果轉成 annotation 的格式
        function handleButtonClick(row) {
            axios
                .get(`/task/get_image/${row.image_id}`)
                .then((res) => {
                    if (res !== null) {
                        imageSrc.value = 'data:image/png;base64,' + res.data;
                    } else {
                        imageSrc.value = '';
                    }
                })
                .catch((err) => {
                    console.log(err);
                    ElMessage({
                        message: 'Get Image Failed',
                        type: 'warning'
                    });
                });
            let fileInfo = tableData.value.filter((item) => item.task_id === row.task_id);
            file_name.value = fileInfo[0].file_name;
            num.value = fileInfo[0].num;
            let ocr_results = general_upload_res.value.filter((item) => item.task_id === row.task_id)[0].ocr_results;
            initialData.value = parseOcrDetail(ocr_results);
        }

        function back() {
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
                    emit('nextStepEmit', 1);
                })
                .catch(() => {
                    ElMessage({
                        type: 'info',
                        message: '操作取消'
                    });
                });
        }

        function downloadFile() {
            const jsonWorkSheet = XLSX.utils.json_to_sheet(excelData.value);
            const workBook = {
                SheetNames: ['jsonWorkSheet'],
                Sheets: {
                    jsonWorkSheet: jsonWorkSheet
                }
            };
            XLSX.writeFile(workBook, '通用辨識結果.xlsx');
        }

        // Start to pull the status
        onMounted(() => {
            waitUntilOcrComplete();
        });

        return {
            containerId,
            imageSrc,
            imageResult,
            localStorageKey,
            width,
            height,
            dataCallback,
            initialData,
            initialDataId,
            file_name,
            num,
            isDownload,
            Download,
            Back,
            excelData,
            tableData,
            reloadAnnotator,
            isRunning,
            finishedStatus,
            getTaskData,
            general_upload_res,
            callback,
            getStatusColor,
            getOcrStatus,
            getOcrResults,
            waitUntilOcrComplete,
            handleButtonClick,
            back,
            downloadFile
        };
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
                            <div class="flex-shrink-1 md:flex-shrink-0 flex align-items-center justify-content-center font-bold p-4 m-3">成功辨識：{{ general_upload_res.length }} 張</div>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="card">
                            <div class="flex align-items-center justify-content-center font-bold m-2 mb-5">
                                <el-table :data="getTaskData" style="width: 100%" :key="isRunning">
                                    <el-table-column prop="num" label="號碼" sortable width="100" />
                                    <el-table-column prop="file_name" label="檔名" sortable width="200" />
                                    <el-table-column prop="status" label="辨識狀態" width="180">
                                        <template #default="{ row }">
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
                        <div v-if="imageSrc !== null">
                            <p>號碼：{{ num }}</p>
                            <p>檔名：{{ file_name }}</p>
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
