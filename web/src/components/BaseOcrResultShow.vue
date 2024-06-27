<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import Annotation from '@/components/Annotation.vue';
import { Download, Back } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import * as XLSX from 'xlsx/xlsx.mjs';
import { PULL_INTERVAL, MAX_RETRIES, error_table, default_error_msg } from '@/constants.js';
import { useStore } from 'vuex';
import useAnnotator from '@/mixins/useAnnotator.js';
import { apiClient } from '@/service/auth.js';
import Icon from '@/components/Icon.vue';
import { GET_TASK_RESULT_URL, GET_TASK_STATUS_URL, GET_TASK_IMAGE_URL, FEEDBACK_URL } from '@/url.js';

export default {
    props: {
        hasTitle: Boolean
    },
    components: {
        Annotation,
        Icon
    },
    name: 'BaseOcrResultShow',
    setup(props, { emit }) {
        const hasTitle = ref(props.hasTitle);
        const { parseOcrDetail } = useAnnotator();
        const store = useStore();

        const containerId = ref('my-pic-annotation');
        const imageSrc = ref(null);
        const width = ref('1200');
        const height = ref('400px');
        const dataCallback = ref('');
        const initialData = ref('');
        const initialDataId = ref(null);
        const file_name = ref('');
        const num = ref('');
        const isSelectionLight = ref(false)
        const reloadAnnotator = ref(false);
        const isRunning = ref(false);
        const finishedStatus = ref(['SUCCESS', 'FAIL']);
        const general_upload_res = computed(() => store.state.general_upload_res);
        const image_cv_id = ref('');

        const buttonText = ref('返回辨識');
        const buttonType = ref('btnDarkBlue');
        const downloadButtonText = ref('下載 Excel');
        const selectedRows = ref([]);
        const abortController = new AbortController();
        const warningStyle = {
            'background-color': 'rgb(252, 230, 190)'
        };


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

        async function getOcrResults(item) {
            try {
                let response = await apiClient.get(`${GET_TASK_RESULT_URL}/${general_upload_res.value[item].task_id}`, { signal: abortController.signal });
                let err_code = '';
                if (response.data.status === 'SUCCESS') {
                    store.commit('generalImageOcrResults', { item: item, ocr_results: response.data.result, file_name: response.data.file_name });
                } else {
                    err_code = response.data.status_msg || '';
                }
                store.commit('generalImageOcrStatus', { item: item, status: response.data.status, status_msg: err_code, file_name: response.data.file_name });
                reloadAnnotator.value = !reloadAnnotator.value;
            } catch (error) {
                if (error instanceof TypeError) {
                   console.log('cancel')
                } else {
                    ElMessage({
                        message: '辨識失敗',
                        type: 'warning'
                    });
                }
            }
        }


        async function getOcrStatus(item) {
            try {
                let response = await apiClient.get(`${GET_TASK_STATUS_URL}/${general_upload_res.value[item].task_id}`, { signal: abortController.signal });
                if (response.data.status === 'SUCCESS') {
                    await getOcrResults(item);
                } else {
                    let err_code = response.data.status_msg || '';
                    store.commit('generalImageOcrStatus', { item: item, status: response.data.status, status_msg: err_code, file_name: response.data.file_name });
                }
            } catch (error) {
                // Check specifically for TypeError and handle it
                if (error instanceof TypeError) {
                    console.log('cancel');
                } else {
                    ElMessage({
                        message: '辨識失敗',
                        type: 'warning'
                    });
                }
            }
        }

        async function waitUntilOcrComplete() {
            isRunning.value = true;
            let count = 0;
            const BATCH_SIZE = 5; // Define your batch size

            while (isRunning.value) {
                const unfinishedItems = general_upload_res.value.filter((item) => !finishedStatus.value.includes(item.status));
                if (unfinishedItems.length === 0) {
                    isRunning.value = false;
                    break;
                }

                for (let i = 0; i < unfinishedItems.length; i += BATCH_SIZE) {
                    // Create a batch
                    const batch = unfinishedItems.slice(i, i + BATCH_SIZE);

                    // Process all items in the batch concurrently
                    await Promise.all(batch.map(item => getOcrStatus(general_upload_res.value.indexOf(item))));

                    // Optional: check if the process should still continue after each batch
                    if (!isRunning.value) break;
                }

                if (!isRunning.value) break;

                // Wait for a while before processing the next batch
                await new Promise((resolve) => setTimeout(resolve, PULL_INTERVAL));
                count++;

                // Check for retry limit
                if (count === MAX_RETRIES) {
                    // Process any remaining items as failed
                    unfinishedItems.forEach(item => {
                        store.commit('generalImageOcrStatus', { item: general_upload_res.value.indexOf(item), status: 'FAIL', status_msg: '5004', file_name: item.file_name });
                    });
                    break;
                }
            }
            isRunning.value = false;
        }


        // ocr 結果轉成 annotation 的格式
        function handleButtonClick(row, tableData) {
            apiClient
                .get(`${GET_TASK_IMAGE_URL}/${row.image_id}`)
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
                    abortController.abort(); // Cancel all ongoing requests
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
            isSelectionLight.value = false;
        }

        async function sendFeedback(filteredUploads) {
            try {
                const res = await apiClient.post(FEEDBACK_URL, filteredUploads, {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    timeout: 5000  // Adjusted timeout to 5 seconds
                });
            } catch (error) {
                console.error(error);
                ElMessage({
                    message: 'API 請求失敗：' + error.message,
                    type: 'error'
                });
            }
        }

        async function downloadFile() {
            if (selectedRows.value.length <= 0) {
                ElMessage({
                    message: '請先選擇要下載的檔案',
                    type: 'warning'
                });
                isSelectionLight.value = true;
                return
            }
            const successRows = selectedRows.value.filter(row => row.status === 'SUCCESS');
            if(successRows.length == 0) {
                ElMessage({
                    message: '請選擇成功辨識的檔案',
                    type: 'warning'
                });
                return
            }
        
            const filteredUploads = general_upload_res.value.filter(upload => 
                successRows.some(row => row.task_id === upload.task_id));
            if (filteredUploads.length > 0) {
                const feedbacks = filteredUploads.map(upload => ({
                    image_cv_id: upload.image_cv_id,
                    points_list: upload.ocr_results.data_results.map(data_result => ({
                        type: 'text',
                        tag: data_result.tag, 
                        text: data_result.text,
                        points: data_result.points 
                    }))
                }));

                // Filter out feedbacks with empty points_list
                const nonEmptyFeedbacks = feedbacks.filter(feedback => feedback.points_list.length > 0);

                if (nonEmptyFeedbacks.length > 0) {
                    // Send feedback if there are non-empty points_list
                    sendFeedback(nonEmptyFeedbacks);
                }
            }
            // Proceed to file download
            const excelData = getExcelData(successRows);
            const jsonWorkSheet = XLSX.utils.json_to_sheet(excelData);
            const workBook = {
                SheetNames: ['jsonWorkSheet'],
                Sheets: {
                    jsonWorkSheet: jsonWorkSheet
                }
            };
            XLSX.writeFile(workBook, '辨識結果.xlsx');
        }
        function tableHeaderCellStyle({ row, column, rowIndex, columnIndex }) {
            if(columnIndex === 0 && isSelectionLight.value){
                return warningStyle
            }
        }
        function cellStyle({ row, column, rowIndex, columnIndex }) {
            if(columnIndex === 0 && isSelectionLight.value){
                return warningStyle
            }
        }


        // Start to pull the status
        onMounted(async () => {
            waitUntilOcrComplete();
        });
        onBeforeUnmount(() => {
            isRunning.value = false;
            abortController.abort();
        });

        return {
            selectedRows,
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
            selectionChange,
            hasTitle,
            cellStyle,
            tableHeaderCellStyle,
            isSelectionLight
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
    <button class="uiStyle sizeS minLength btnDarkBlue" @click="back" :disabled="isUploadDisabled">
        {{ buttonText }}
    </button>
    <div class="card">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px;">
            <p style="margin: 0; flex: 1;" class="subtitle">辨識結果</p>
            <div style="display: grid; place-items: center">
                <button class="uiStyle sizeS subLength btnGreen" @click="downloadFile" :disabled="isRunning">
                    {{ downloadButtonText }}
                </button>
            </div>
        </div>
        <span style="margin-right: 2px; color: red; font-size: 10px" v-if="isSelectionLight">勾選下載檔案</span>
        <div class="flex align-items-center justify-content-center font-bold m-2 mb-5">
            
            <el-table :data="tableData" style="width: 100%" :key="isRunning" @selection-change="selectionChange" :cell-style="cellStyle" :header-cell-style="tableHeaderCellStyle"
                height="250" border>
                <el-table-column type="selection" width="55" color="red"/>
                <el-table-column prop="num" label="號碼" sortable :min-width="10" /> 
                <el-table-column prop="file_name" label="檔名" sortable :min-width="30">
                    <template v-slot="scope">
                        {{ scope.row.file_name }} - {{ scope.row.num }}
                    </template>
                </el-table-column>
                <el-table-column prop="status" label="辨識狀態" :min-width="20">
                    <template v-slot="scope">
                        <el-tooltip :disabled="scope.row.status != 'FAIL'" class="error-tip" effect="dark"
                            :content="getErrorMsg(scope.row, this.tableData)" placement="top">
                            <el-tag :type="getStatusColor(scope.row.status)">{{ scope.row.status }}</el-tag>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column label="檢視" :min-width="30">
                    <template v-slot="scope">
                        <button v-if="scope.row.isFinished" @click="handleButtonClick(scope.row, this.tableData)"
                            class="preview">
                            <Icon type="eye" />
                        </button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div v-if="imageSrc !== null">
            <p class="subtitle">號碼：{{ num }}</p>
            <p>{{ file_name }}</p>
            <Annotation containerId="my-pic-annotation-output" :imageSrc="imageSrc" :editMode="false" :width="width"
                :height="height" :dataCallback="callback" :initialData="initialData" initialDataId=""
                :image_cv_id="image_cv_id" :hasTitle="hasTitle"></Annotation>
        </div>
    </div>
</template>
<style scoped>
.my-button {
    margin: 10px;
}

.preview {
    padding: 0px 0px 0px 2px;
    border: 0px;
    background: none;
}
</style>