<script>
import { ref, computed, onMounted } from 'vue';
import AnnotationVertical from '@/components/AnnotationVertical.vue';
import axios from 'axios';
import moment from 'moment';
import { ElMessageBox, ElMessage } from 'element-plus';
import { usePhotoService } from '@/service/PhotoService.js';
import useAnnotator from '@/mixins/useAnnotator.js';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

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
        AnnotationVertical
    },

    setup() {
        const store = useStore();
        const router = useRouter();
        const { rectangleTypes, parseTemplateDetail } = useAnnotator();
        const { getImages } = usePhotoService();

        const images = ref(null);
        const tableData = ref([]);

        onMounted(async () => {
            images.value = await getImages();
            tableData.value = await getAvailableTemplate();
        });

        const formattedTableData = computed(() => {
            if (tableData.value.length === 0) {
                return [];
            }
            return tableData.value.map((row) => {
                return {
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
        const height = ref(600);
        const imageSrc = ref('');

        const tableHeader = ref([
            {
                prop: 'template_id',
                label: '編號',
                editable: false,
                type: 'number',
                width: '200px'
            },
            {
                prop: 'template_name',
                label: '姓名',
                editable: false,
                type: 'input',
                width: '150px'
            },
            {
                prop: 'creation_time',
                label: '創建日期',
                editable: false,
                type: 'date',
                width: '200px'
            },
            {
                prop: 'expiration_time',
                label: '到期日期',
                editable: false,
                type: 'date',
                width: '200px'
            }
        ]);

        const template_id = ref('');
        const template = ref('');
        const initialData = ref('');

        // Methods
        function formatDate(date) {
            return moment(date).format('YYYY-MM-DD HH:mm:ss');
        }

        async function getAvailableTemplate() {
            let user_id = '13520';
            let tableData = [];
            try {
                const response = await axios.get('/template_crud/get_available_templates/' + user_id);
                tableData = response['data']['template_infos'];
                return tableData;
            } catch (error) {
                if (error.response.data.msg === 'available_templates are not found') {
                    return [];
                }
                return error;
            }
        }

        function handleConfirm(row) {
            row.editable = false;
        }

        async function handleLook(templateid, userType) {
            template_id.value = templateid;
            try {
                const response = await axios.get('/template_crud/get_template_detail/' + template_id.value);
                initialData.value = parseTemplateDetail(response['data'], userType);
                imageSrc.value = 'data:image/png;base64,' + response['data'].image;
            } catch (error) {
                if (error.code === 'ERR_NETWORK') {
                    status.value = 'network';
                }
                return error;
            }
        }

        async function handleDelete(template_id) {
            try {
                await ElMessageBox.confirm('此操作將永久刪除該模板, 是否繼續?', '提示', {
                    confirmButtonText: '確定',
                    cancelButtonText: '取消',
                    type: 'warning'
                });

                const response = await axios.delete('/template_crud/delete_template/' + template_id.value);
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
                    ElMessage({
                        type: 'error',
                        message: '刪除失敗!'
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
            store.commit('createNewUpdate', true);
            router.push({ name: 'SelfDefine' });
        }

        async function editTemplate() {
            // clear local storage
            localStorage.clear();
            // get template detail
            const response = await axios.get('/template_crud/get_template_detail/' + template_id.value);
            //template.value = response['data'];

            // set local storage
            localStorage.imageSource = 'data:image/png;base64,' + response['data'].image;
            for (let i = 0; i < rectangleTypes.value.length; i++) {
                let data = parseTemplateDetail(response['data'], rectangleTypes.value[i].code);
                localStorage.setItem(rectangleTypes.value[i].code, JSON.stringify(data));
            }
            localStorage.setItem('template_id', template_id.value);
            store.commit('templateNameUpdate', response['data'].template_name);
            store.commit('createNewUpdate', false);
            router.push({ path: '/features/general/self-define/step' });
        }

        function downloadTemplate() {
            let template_info_json = JSON.stringify(template.value);
            let blob = new Blob([template_info_json], { type: 'text/plain;charset=utf-8' });
            let url = URL.createObjectURL(blob);
            let link = document.createElement('a');
            link.href = url;
            link.download = `${template.value.template_name}.json`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        }

        async function deleteTemplate() {
            try {
                await ElMessageBox.confirm('此操作將永久刪除該模板, 是否繼續?', '提示', {
                    confirmButtonText: '確定',
                    cancelButtonText: '取消',
                    type: 'warning'
                });

                const response = await axios.delete('/template_crud/delete_template/' + template_id.value);
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
                    ElMessage({
                        type: 'error',
                        message: '刪除失敗!'
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
            formatDate,
            getAvailableTemplate,
            handleConfirm,
            handleLook,
            handleDelete,
            prepend,
            append,
            deleteCurrentColumn,
            insertBefore,
            createTemplate,
            editTemplate,
            downloadTemplate,
            deleteTemplate,
            template,
            template_id,
            initialData,
            templateOCR
        };
    }
};
</script>

<template>
    <div class="grid">
        <div class="col-7">
            <div class="card" style="height: 850px; overflow-y: scroll">
                <!-- Breadcrumb -->
                <el-breadcrumb>
                    <el-breadcrumb-item :to="{ path: '/' }">首頁</el-breadcrumb-item>
                    <el-breadcrumb-item>模板辨識</el-breadcrumb-item>
                </el-breadcrumb>
                <br />
                <div class="flex justify-content-start flex-wrap card-container">
                    <div class="flex align-items-center justify-content-center mt-1 mb-0 mr-2">
                        <h2>模板檢視</h2>
                    </div>
                    <div class="flex align-items-center justify-content-center mt-1 mb-1">
                        <el-button type="primary" class="mr-2 mb-2" style="width: 100%" @click="createTemplate" :disabled="isUploadDisabled"> ＋新增 </el-button>
                    </div>
                </div>
                <el-table :data="formattedTableData" style="width: 100%">
                    <el-table-column :prop="item.prop" :label="item.label" v-for="item in tableHeader" :key="item.prop" :width="item.width">
                        <template #default="scope">
                            <div v-show="item.editable || scope.row.editable" class="editable-row">
                                <template v-if="item.type === 'input'">
                                    <el-input size="small" v-model="scope.row[item.prop]" :placeholder="`請輸入 ${item.label}`" @change="handleEdit(scope.$index, scope.row)" />
                                </template>
                            </div>
                            <div v-show="!item.editable && !scope.row.editable" class="editable-row">
                                <span class="editable-row-span">{{ scope.row[item.prop] }}</span>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="350px">
                        <template #default="scope">
                            <el-button v-show="!scope.row.editable" size="big" @click="scope.row.editable = true">編輯</el-button>
                            <el-button v-show="scope.row.editable" size="small" type="success" @click="handleConfirm(scope.row)">確認</el-button>
                            <el-button class="mr-1" size="big" type="success" @click="templateOCR(scope.row.template_id)">辨識</el-button>
                            <el-button size="big" type="info" @click="handleLook(scope.row.template_id, rectangleTypes[0].code)">檢視</el-button>
                            <el-button size="big" type="danger" @click="handleDelete(scope.row.template_id)">刪除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <div class="col-5">
            <div v-if="(formattedTableData.length >= 1) & !template_id" class="card flex justify-content-center align-items-center" style="height: 850px">請點選檢視</div>
            <div v-else-if="template_id" class="card" style="height: 850px; overflow-y: scroll">
                <h5>請選擇標註模式</h5>
                <div class="flex flex-column card-container">
                    <div class="flex align-items-center justify-content-center h-4rem font-bold border-round m-2">
                        <SelectButton v-model="selectedRectangleType" :options="rectangleTypes" optionLabel="name" @change="handleLook(template_id, selectedRectangleType.code)" />
                    </div>
                    <div class="flex align-items-center justify-content-center h-4rem font-bold border-round m-4">
                        <Button icon="pi pi-download" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'下載模板設定檔'" @click="downloadTemplate" />
                        <Button icon="pi pi-pencil" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'編輯模版'" @click="editTemplate" />
                        <Button icon="pi pi-trash" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'刪除模板'" @click="deleteTemplate" />
                    </div>
                    <div class="flex align-items-center justify-content-center h-100rem font-bold border-round m-2">
                        <AnnotationVertical
                            ref="child"
                            containerId="my-pic-annotation-output"
                            :editMode="false"
                            :imageSrc="imageSrc"
                            :width="width"
                            :height="height"
                            dataCallback=""
                            :initialData="initialData"
                            :initialDataId="initialDataId"
                            :justShow="true"
                        ></AnnotationVertical>
                    </div>
                    <div class="flex align-items-center justify-content-center h-100rem font-bold border-round m-2">
                        <!-- <BoxCard boxName="text" :boxTitle="myModel.name" /> -->
                    </div>
                </div>
            </div>
            <div v-else class="card flex justify-content-center align-items-center" style="height: 850px">沒有模板可以檢視</div>
        </div>
    </div>
</template>
