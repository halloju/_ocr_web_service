<script>
import { ref, computed, onMounted } from 'vue';
import Annotation from '@/components/Annotation.vue';
import axios from 'axios';
import moment from 'moment';
import { ElMessageBox, ElMessage } from 'element-plus';
import PhotoService from '@/service/PhotoService';
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
        Annotation
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

        onMounted(async () => {
            images.value = await galleriaService.getImages();
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
        const height = ref(1000);
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
                label: '名稱',
                editable: false,
                type: 'input',
                width: '150px'
            },
            // {
            //     prop: 'creation_time',
            //     label: '創建日期',
            //     editable: false,
            //     type: 'date',
            //     width: '200px'
            // },
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
        const creation_time = ref('');

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
            console.log('handleLook');
            template_id.value = templateid;
            try {
                const response = await axios.get('/template_crud/get_template_detail/' + template_id.value);
                template.value = response['data'];
                initialData.value = parseTemplateDetail(response['data'], userType);
                creation_time.value = template.value.creation_time;
                imageSrc.value = 'data:image/png;base64,' + response['data'].image;
                dialogVisible.value = true;
                dialogWidth.value = '850px';
                console.log('dialogVisible');
            } catch (error) {
                if (error.code === 'ERR_NETWORK') {
                    // status.value = 'network';
                    console.error('ERR_NETWORK');
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

                const response = await axios.delete('/template_crud/delete_template/' + template_id);
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
                console.log(error);
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
            sessionStorage.clear();
            store.commit('createNewUpdate', true);
            router.push({ name: 'SelfDefine' });
        }

        async function editTemplate() {
            // clear local storage
            sessionStorage.clear();
            // get template detail
            const response = await axios.get('/template_crud/get_template_detail/' + template_id.value);
            //template.value = response['data'];

            // set local storage
            sessionStorage.imageSource = 'data:image/png;base64,' + response['data'].image;
            for (let i = 0; i < rectangleTypes.value.length; i++) {
                let data = parseTemplateDetail(response['data'], rectangleTypes.value[i].code);
                sessionStorage.setItem(rectangleTypes.value[i].code, JSON.stringify(data));
            }
            sessionStorage.setItem('template_id', template_id.value);
            sessionStorage.setItem('templateName', response['data'].template_name);
            store.commit('createNewUpdate', false);
            router.push({ name: 'SelfDefine' });
        }

        function downloadTemplate() {
            let template_info_json = JSON.stringify(template.value);
            let blob = new Blob([template_info_json], { type: 'text/plain;charset=utf-8' });
            let url = URL.createObjectURL(blob);
            let link = document.createElement('a');
            link.href = url;
            link.download = `${template_id.value}.json`;
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
            dialogWidth,
            dialogVisible,
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
            creation_time,
            templateOCR
        };
    }
};
</script>

<template>
    <div class="grid">
        <div class="col-12">
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
                        <el-button type="primary" class="mr-2 mb-2" style="width: 100%" @click="createTemplate"> ＋新增 </el-button>
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
                    <el-table-column label="操作" width="500px">
                        <template #default="scope">
                            
                            <el-button v-show="scope.row.editable" size="" type="success" @click="handleConfirm(scope.row)">確認</el-button>
                            <el-button class="mr-1" size="" type="primary" @click="templateOCR(scope.row.template_id)">辨識</el-button>
                            <el-button size="" type="success" @click="handleLook(scope.row.template_id, rectangleTypes[0].code)">檢視</el-button>
                            <el-button size="" type="danger"  @click="handleDelete(scope.row.template_id)">刪除</el-button>
                            <el-button size="" type="warning"  plain @click="editTemplate">編輯</el-button>
                            <el-button size="" type="info" plain @click="downloadTemplate">下載</el-button>
                            

                        </template>
                    </el-table-column>
                </el-table>
                <el-dialog v-model="dialogVisible" :width="dialogWidth" >
                    <div class="card" style="height: 850px; overflow-y: scroll">
                        <h4> template id: {{ template_id }} </h4>
                        <h5> 創建日期: {{ creation_time }} </h5>
                        <div class="flex flex-column card-container">
                            <div class="flex align-items-center justify-content-center h-4rem font-bold border-round m-2">
                                <SelectButton v-model="selectedRectangleType" :options="rectangleTypes" optionLabel="name" @change="handleLook(template_id, selectedRectangleType.code)" />
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
                            <div class="flex align-items-center justify-content-center h-100rem font-bold border-round m-2">
                                <!-- <BoxCard boxName="text" :boxTitle="myModel.name" /> -->
                            </div>
                        </div>
                    </div>
                </el-dialog>
            </div>
        </div>
    </div>
</template>
