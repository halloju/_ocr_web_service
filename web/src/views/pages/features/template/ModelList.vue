<script>
import { ref, computed, onMounted } from 'vue';
import Annotation from '@/components/Annotation.vue';
import moment from 'moment';
import { ElMessageBox, ElMessage } from 'element-plus';
import PhotoService from '@/service/PhotoService';
import useAnnotator from '@/mixins/useAnnotator.js';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { apiClient } from '@/service/auth.js';
import { handleErrorMsg } from '@/mixins/useCommon.js';
import { Delete, Edit, Download, Pointer, View } from '@element-plus/icons-vue';
import EditableRow from '@/components/EditableRow.vue';
import ActionColumn from '@/components/ActionColumn.vue';
import BreadCrumb from '@/components/BreadCrumb.vue';
import SelectButton from 'primevue/selectbutton';

const item = {
    name: '',
    birth: '',
    province: '',
    city: '',
    address: '',
    phone: ''
};

const header = {
    prop: 'key',
    label: '自定義',
    editable: false,
    type: 'input'
};

export default {
    name: 'ModelList',
    components: {
        Annotation,
        EditableRow,
        ActionColumn,
        BreadCrumb,
        SelectButton
    },
    setup() {
        const store = useStore();
        const router = useRouter();
        const { rectangleTypes, parseTemplateDetail } = useAnnotator();
        const galleriaService = new PhotoService();

        const images = ref(null);
        const tableData = ref([]);
        const dialogVisible = ref(false);
        const dialogWidth = ref('');

        const breadcrumbItems = ref([{ path: '/', label: '首頁' }, { label: '通用辨識' }, { label: '模板辨識', isCurrent: true }]);
        const actions = ref([
            { label: '辨識', icon: 'Pointer', type: 'primary', handler: 'templateOCR' },
            { label: '檢視', icon: 'View', type: 'info', handler: 'handleLook' },
            { label: '編輯', icon: 'Edit', type: 'info', handler: 'editTemplate' },
            { label: '刪除', icon: 'Delete', type: 'danger', handler: 'handleDelete' },
            { label: '下載', icon: 'Download', type: 'info', handler: 'downloadTemplate' }
        ]);

        onMounted(async () => {
            images.value = await galleriaService.getImages();
            tableData.value = await getAvailableTemplate();
        });

        const formattedTableData = computed(() => {
            if (tableData.value.length === 0) {
                return [];
            }
            return tableData.value.map((row, idx) => {
                return {
                    idx: idx + 1,
                    ...row,
                    created_at: formatDate(row.creation_time),
                    expired_at: formatDate(row.expiration_time)
                };
            });
        });

        const selectedRectangleType = ref({
            name: '文字',
            code: 'text'
        });
        const width = ref(1000);
        const height = ref('600');
        const imageSrc = ref('');

        const tableHeader = ref([
            {
                prop: 'idx',
                label: 'NO',
                editable: false,
                type: 'number',
                width: '5'
            },
            {
                prop: 'template_name',
                label: '模板名稱',
                editable: false,
                type: 'input',
                width: '20'
            },
            {
                prop: 'template_id',
                label: '模板編號',
                editable: false,
                type: 'number',
                width: '25'
            }
        ]);

        const template_id = ref('');
        const template = ref('');
        const initialData = ref('');
        const creation_time = ref('');
        const buttonText = ref('新增模板');

        // Methods
        function formatDate(date) {
            return moment(date).format('YYYY-MM-DD HH:mm:ss');
        }

        async function getAvailableTemplate() {
            let tableData = [];
            try {
                const response = await apiClient.get('/template_crud/get_available_templates');
                tableData = response['data']['template_infos'];
                return tableData;
            } catch (error) {
                if (error.response.data.msg === 'available_templates are not found') {
                    return [];
                } else {
                    const error_msg = handleErrorMsg(error.response);
                    ElMessage({
                        type: 'error',
                        message: error_msg
                    });
                }
                return error;
            }
        }

        function handleConfirm(row) {
            row.editable = false;
        }

        async function handleLook(id, userType = 'text') {
            template_id.value = id;
            const response = await getTemplateDetail(template_id.value);
            if (response) {
                template.value = response['data'];
                initialData.value = parseTemplateDetail(response['data'], userType);
                creation_time.value = template.value.creation_time;
                imageSrc.value = 'data:image/png;base64,' + response['data'].image;
                dialogVisible.value = true;
                dialogWidth.value = '950px';
            }
        }

        async function handleDelete(template_id) {
            try {
                const confirmResult = await ElMessageBox.confirm('此操作將永久刪除該模板, 是否繼續?', '提示', {
                    confirmButtonText: '確定',
                    cancelButtonText: '取消',
                    type: 'warning'
                });

                if (confirmResult) {
                    const response = await apiClient.delete('/template_crud/delete_template/' + template_id);
                    if (!response.error) {
                        ElMessage({
                            type: 'success',
                            message: '刪除成功!'
                        });
                        tableData.value = await getAvailableTemplate();
                    } else {
                        ElMessage({
                            type: 'error',
                            message: '刪除失敗!'
                        });
                    }
                } else {
                    ElMessage({
                        type: 'info',
                        message: '已取消刪除'
                    });
                }
            } catch (error) {
                if (error != 'cancel') {
                    const error_msg = handleErrorMsg(error.response);
                    // console.log(error_msg);
                    ElMessage({
                        type: 'error',
                        message: '刪除失敗! ' + error_msg
                    });
                    return error;
                }
            }
        }

        function prepend(index) {
            item.editable = true;
            tableData.value.splice(index, 0, item);
        }

        function append(index) {
            item.editable = true;
            tableData.value.splice(index + 1, 0, item);
        }

        function deleteCurrentColumn(index) {
            tableHeader.value.splice(index, 1);
        }

        function insertBefore(index) {
            header.editable = true;
            tableHeader.value.splice(index, 0, header);
        }

        function createTemplate() {
            sessionStorage.clear();
            store.commit('createNewUpdate', true);
            store.commit('templateNameUpdate', '');
            router.push({ name: 'SelfDefine' });
        }

        async function getTemplateDetail(template_id) {
            try {
                const response = await apiClient.get('/template_crud/get_template_detail/' + template_id);
                if (response.status == 200) return response;
            } catch (error) {
                if (error.code === 'ERR_NETWORK') {
                    console.error('ERR_NETWORK');
                } else {
                    const error_msg = handleErrorMsg(error.response);
                    ElMessage({
                        type: 'error',
                        message: error_msg
                    });
                }
            }
        }

        async function editTemplate(template_id) {
            // clear local storage
            sessionStorage.clear();
            // get template detail
            const response = await apiClient.get('/template_crud/get_template_detail/' + template_id);
            //template.value = response['data'];

            // set local storage
            sessionStorage.imageSource = 'data:image/png;base64,' + response['data'].image;
            for (let i = 0; i < rectangleTypes.value.length; i++) {
                let data = parseTemplateDetail(response['data'], rectangleTypes.value[i].code);
                sessionStorage.setItem(rectangleTypes.value[i].code, JSON.stringify(data));
            }
            sessionStorage.setItem('template_id', template_id);
            // sessionStorage.setItem('templateName', response['data'].template_name);
            store.commit('templateNameUpdate', response['data'].template_name);
            store.commit('createNewUpdate', false);
            router.push({ name: 'SelfDefine' });
        }

        async function downloadTemplate(template_id) {
            const response = await getTemplateDetail(template_id);
            if (response) {
                template.value = response['data'];
                let template_info_json = JSON.stringify(template.value);
                let blob = new Blob([template_info_json], { type: 'text/plain;charset=utf-8' });
                let url = URL.createObjectURL(blob);
                let link = document.createElement('a');
                link.href = url;
                link.download = `${template_id}.json`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
            }
        }

        async function deleteTemplate() {
            try {
                await ElMessageBox.confirm('此操作將永久刪除該模板, 是否繼續?', '提示', {
                    confirmButtonText: '確定',
                    cancelButtonText: '取消',
                    type: 'warning'
                });

                const response = await apiClient.delete('/template_crud/delete_template/' + template_id.value);
                if (!response.error) {
                    ElMessage({
                        type: 'success',
                        message: '刪除成功!'
                    });
                    tableData.value = await getAvailableTemplate();
                } else {
                    ElMessage({
                        type: 'error',
                        message: '刪除失敗!'
                    });
                }
            } catch (error) {
                if (error instanceof ElMessageBox.MessageBoxClosedError) {
                    ElMessage({
                        type: 'info',
                        message: '已取消刪除'
                    });
                } else {
                    const error_msg = handleErrorMsg(error.response);
                    ElMessage({
                        type: 'error',
                        message: '刪除失敗!' + error_msg
                    });
                    return error;
                }
            }
        }

        function templateOCR(template_id) {
            store.commit('TemplateIdUpdate', template_id);
            router.push({ path: '/features/ocr/template' });
        }

        return {
            // Data
            rectangleTypes,
            selectedRectangleType,
            width,
            height,
            imageSrc,
            tableData,
            tableHeader,
            formattedTableData,
            dialogWidth,
            dialogVisible,
            buttonText,
            breadcrumbItems,
            actions,
            template,
            template_id,
            initialData,
            creation_time,
            formatDate,
            getAvailableTemplate,
            handleConfirm,
            handleDelete,
            prepend,
            append,
            deleteCurrentColumn,
            insertBefore,
            createTemplate,
            editTemplate,
            downloadTemplate,
            deleteTemplate,
            templateOCR,
            handleLook,
            Delete,
            Edit,
            Download,
            View,
            Pointer
        };
    }
};
</script>
<template>
    <div class="layoutZoneContainer">
        <BreadCrumb :items="breadcrumbItems" />

        <div class="action-header">
            <h4 style="margin-bottom: 0px">模板列表</h4>
            <button class="uiStyle sizeS subLength btnGreen" @click="createTemplate">
                {{ buttonText }}
            </button>
        </div>

        <el-table :data="formattedTableData" style="width: 100%" border>
            <el-table-column v-for="item in tableHeader" :key="item.prop" :prop="item.prop" :label="item.label" :min-width="item.width">
                <template #default="scope">
                    <EditableRow :item="item" :row="scope.row" @edit="handleEdit(scope.$index, scope.row)" />
                </template>
            </el-table-column>

            <ActionColumn
                v-for="action in actions"
                :key="action.label"
                :label="action.label"
                :icon="action.icon"
                :type="action.type"
                :handler="action.handler"
                @templateOCR="templateOCR"
                @handleLook="handleLook"
                @editTemplate="editTemplate"
                @handleDelete="handleDelete"
                @downloadTemplate="downloadTemplate"
            />
        </el-table>

        <el-dialog v-model="dialogVisible" :width="dialogWidth">
            <div class="card" style="height: 80vh; overflow-y: scroll">
                <h4>template id: {{ template_id }}</h4>
                <h5>創建日期: {{ creation_time }}</h5>
                <div class="flex flex-column card-container">
                    <div class="flex align-items-center justify-content-center h-4rem font-bold border-round m-2">
                        <!-- Wrap the SelectButton in a container -->
                        <SelectButton v-model="selectedRectangleType" :options="rectangleTypes" optionLabel="name" @change="handleLook(template_id, selectedRectangleType?.code)" />
                    </div>
                    <div class="flex align-items-center justify-content-center h-100rem font-bold border-round m-2">
                        <Annotation
                            ref="child"
                            containerId="my-pic-annotation-output"
                            :editMode="false"
                            :imageSrc="imageSrc"
                            :width="dialogWidth"
                            :height="height"
                            dataCallback=""
                            :initialData="initialData"
                            :justShow="true"
                            :isVertical="true"
                        ></Annotation>
                    </div>
                    <div class="flex align-items-center justify-content-center h-100rem font-bold border-round m-2"></div>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<style scoped>
.select-button-container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center; /* This will center-align the buttons horizontally */
    height: 100%; /* Adjust this if you want a specific height */
}
.action-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    margin-top: 20px;
}

.p-buttonset {
    display: flex;
    justify-content: space-between;
    width: 60%; /* adjust this if needed */
    margin: 0 auto; /* makes the button group center-aligned */
}

.p-highlight {
    background-color: rgb(13, 13, 202);
    border: 1px solid #ccc;
    border-radius: 3px;
}
</style>
