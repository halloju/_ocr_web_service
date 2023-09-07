<script>
import { ref, computed, onMounted } from 'vue';
import Annotation from '@/components/Annotation.vue';
import { Download, Back } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import * as XLSX from 'xlsx/xlsx.mjs';
import { PULL_INTERVAL, MAX_RETRIES, error_table, default_error_msg } from '@/constants.js';
import { useStore } from 'vuex';
import useAnnotator from '@/mixins/useAnnotator.js';
import { apiClient } from '@/service/auth.js';

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
        const width = ref('1200');
        const height = ref(600);
        const dataCallback = ref('');
        const initialData = ref('');
        const initialDataId = ref(null);
        const file_name = ref('');
        const num = ref('');
        const reloadAnnotator = ref(false);
        const isRunning = ref(false);
        const finishedStatus = ref(['SUCCESS', 'FAIL']);
        const general_upload_res = computed(() => store.state.general_upload_res);
        const image_cv_id = ref('');

        const buttonText = ref('返回辨識');
        const buttonType = ref('btnDarkBlue');
        const downloadButtonText = ref('下載 Excel');
        const selectedRows = ref([]);

        const getExcelData = (selectedItems) => {
            let excelData = [];
            let selectedTaskIds = selectedItems.map((item) => item.task_id); // Extract task_ids from selected items

            general_upload_res.value.forEach((item) => {
                // Check if the item's task_id exists in selectedTaskIds
                if (selectedTaskIds.includes(item.task_id) && item.ocr_results) {
                    item.ocr_results.data_results.forEach((result_dic) => {
                        let cols = {
                            filename: item.file_name,
                            image_id: item.image_id
                        };
                        for (const key in result_dic) {
                            cols[key] = typeof result_dic[key] == `object` ? JSON.stringify(result_dic[key]) : result_dic[key];
                        }
                        excelData.push(cols);
                    });
                }
            });
            return excelData;
        };

        function callback(data, image_cv_id) {
            store.dispatch('updateGeneralImageOcrResults', { data, image_cv_id });
        }

        // fail to fail msg
        function getErrorMsg(row, tableData) {
            let fileInfo = tableData.filter((item) => item.task_id === row.task_id);
            if (fileInfo[0].status_msg in error_table) return error_table[fileInfo[0].status_msg] + '(' + fileInfo[0].status_msg + ')';
            else return default_error_msg + '(' + fileInfo[0].status_msg + ')';
        }

        function getStatusColor(status) {
            switch (status) {
                case 'SUCCESS':
                    return 'success';
                case 'PENDING':
                    return 'gray';
                case 'PROCESSING':
                    return 'gray';
                default:
                    return '';
            }
        }

        async function getOcrStatus(item) {
            let err_code = '';
            apiClient
                .get(`/task/status/${general_upload_res.value[item].task_id}`)
                .then(async (res) => {
                    if (res.data.status === 'SUCCESS') {
                        await getOcrResults(item);
                    } else if (res.data.status === 'FAIL') {
                        err_code = res.data.status_msg;
                        store.commit('generalImageOcrStatus', { item: item, status: res.data.status, status_msg: err_code, file_name: res.data.file_name });
                    } else {
                        store.commit('generalImageOcrStatus', { item: item, status: res.data.status, status_msg: err_code, file_name: res.data.file_name });
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
            let err_code = '';
            apiClient
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
                    if (res.data.status === 'FAIL') err_code = res.data.status_msg;
                    store.commit('generalImageOcrStatus', { item: item, status: res.data.status, status_msg: err_code, file_name: res.data.file_name });
                    reloadAnnotator.value = !reloadAnnotator.value;
                })
                .catch((res) => {
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
                if (unfinishedItems.length === 0 || !isRunning.value) {
                    isRunning.value = false;
                    break;
                }
                for (let i = 0; i < unfinishedItems.length; i++) {
                    const item = unfinishedItems[i];
                    await getOcrStatus(general_upload_res.value.indexOf(item));
                }
                if (!isRunning.value) break; // Check before the timeout
                await new Promise((resolve) => setTimeout(resolve, PULL_INTERVAL)); // wait 2 seconds before polling again
                if (!isRunning.value) break; // Check after the timeout
                count++;
                // 這個數字太小可能也跑不完？感覺要衡量一下
                if (count === MAX_RETRIES) {
                    const unfinishedItems = general_upload_res.value.filter((item) => !finishedStatus.value.includes(item.status));
                    for (let i = 0; i < unfinishedItems.length; i++) {
                        const item = unfinishedItems[i];
                        store.commit('generalImageOcrStatus', { item: general_upload_res.value.indexOf(item), status: 'FAIL', status_msg: '5004', file_name: item.file_name });
                    }
                    break;
                }
            }
        }

        // ocr 結果轉成 annotation 的格式
        function handleButtonClick(row, tableData) {
            console.log('aaa');
            apiClient
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
            let fileInfo = tableData.filter((item) => item.task_id === row.task_id);
            file_name.value = fileInfo[0].file_name;
            num.value = fileInfo[0].num;
            let ocr_results = general_upload_res.value.filter((item) => item.task_id === row.task_id)[0].ocr_results;
            initialData.value = parseOcrDetail(ocr_results);
            image_cv_id.value = row.image_id;
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
                    isRunning.value = false;
                    emit('nextStepEmit', 1);
                })
                .catch(() => {
                    ElMessage({
                        type: 'info',
                        message: '操作取消'
                    });
                });
        }

        function selectionChange(selected) {
            selectedRows.value = selected;
        }

        function downloadFile() {
            const excelData = getExcelData(selectedRows.value);
            const jsonWorkSheet = XLSX.utils.json_to_sheet(excelData);
            const workBook = {
                SheetNames: ['jsonWorkSheet'],
                Sheets: {
                    jsonWorkSheet: jsonWorkSheet
                }
            };
            XLSX.writeFile(workBook, '辨識結果.xlsx');
        }

        // Start to pull the status
        onMounted(async () => {
            waitUntilOcrComplete();
            // const col12Width = (document.querySelector('.col-12').clientWidth * 4) / 5;
            // width.value = col12Width - parseInt('4rem');
        });

        return {
            containerId,
            imageSrc,
            width,
            height,
            dataCallback,
            initialData,
            initialDataId,
            file_name,
            num,
            Download,
            Back,
            reloadAnnotator,
            isRunning,
            finishedStatus,
            buttonText,
            buttonType,
            downloadButtonText,
            getExcelData,
            general_upload_res,
            callback,
            getStatusColor,
            getOcrStatus,
            getOcrResults,
            waitUntilOcrComplete,
            handleButtonClick,
            getErrorMsg,
            back,
            downloadFile,
            image_cv_id,
            selectionChange
        };
    },
    computed: {
        tableData() {
            let tempTableData = [];
            this.general_upload_res.forEach((item, index) => {
                tempTableData.push({
                    num: index + 1,
                    task_id: item.task_id,
                    status: item.status,
                    image_id: item.image_id,
                    file_name: item.file_name,
                    isFinished: item.status === 'SUCCESS' ? true : false,
                    status_msg: item.status === 'FAIL' ? item.status_msg : ''
                });
            });
            return tempTableData;
        }
    }
};
</script>

<template>
    <div style="margin-top: 20px">
        <div>
            <div class="formBtnContainer">
                <button class="uiStyle sizeS subLength btnDarkBlue" @click="back" :disabled="isUploadDisabled">
                    {{ buttonText }}
                </button>
            </div>
        </div>
    </div>
    <div class="card">
        <div style="display: flex; align-items: center; justify-content: space-between">
            <h6 style="margin: 0; flex: 1">辨識結果</h6>
            <div style="display: grid; place-items: center">
                <div class="formBtnContainer">
                    <button class="uiStyle sizeS subLength btnGreen" @click="downloadFile" :disabled="isUploadDisabled">
                        {{ downloadButtonText }}
                    </button>
                </div>
            </div>
        </div>
        <div class="flex align-items-center justify-content-center font-bold m-2 mb-5">
            <el-table :data="tableData" style="width: 100%" :key="isRunning" @selection-change="selectionChange" border>
                <el-table-column type="selection" width="55" />
                <el-table-column prop="num" label="號碼" sortable :min-width="10" />
                <el-table-column prop="file_name" label="檔名" sortable :min-width="30" />
                <el-table-column prop="status" label="辨識狀態" :min-width="20">
                    <template v-slot="scope">
                        <el-tooltip :disabled="scope.row.status != 'FAIL'" class="error-tip" effect="dark" :content="getErrorMsg(scope.row, this.tableData)" placement="top">
                            <el-tag :type="getStatusColor(scope.row.status)">{{ scope.row.status }}</el-tag>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column label="檢視" :min-width="30">
                    <template v-slot="scope">
                        <el-button v-if="scope.row.isFinished" @click="handleButtonClick(scope.row, this.tableData)" type="primary" round>V</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div v-if="imageSrc !== null">
            <p>號碼：{{ num }}</p>
            <p>檔名：{{ file_name }}</p>
            <Annotation containerId="my-pic-annotation-output" :imageSrc="imageSrc" :editMode="false" :width="width" :height="height" :dataCallback="callback" :initialData="initialData" initialDataId="" :image_cv_id="image_cv_id"></Annotation>
        </div>
    </div>
</template>
<style scoped>
.my-button {
    margin: 10px;
}
</style>
