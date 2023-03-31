<script>
import moment from 'moment';
import axios from 'axios';
import PhotoService from '@/service/PhotoService';
import AnnotationVertical from '@/components/AnnotationVertical.vue';
import { ElMessageBox } from 'element-plus';

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
    name: 'public',
    components: {
        AnnotationVertical
    },
    created() {
        this.galleriaService = new PhotoService();
        this.getAvailableTemplate().then((tableData) => {
            this.tableData = tableData;
        });
    },
    mounted() {
        this.galleriaService.getImages().then((data) => (this.images = data));
    },
    computed: {
        formattedTableData() {
            if (this.tableData.length === 0) {
                return [];
            }
            return this.tableData.map((row) => {
                return {
                    ...row,
                    created_at: this.formatDate(row.updated_at),
                    expired_at: this.formatDate(row.expired_at)
                };
            });
        }
    },
    data() {
        return {
            models: [
                { name: '文字', code: 'text' },
                { name: '方塊', code: 'box' },
                { name: '遮罩', code: 'mask' }
            ],
            myModel: { name: '文字', code: 'text' },
            width: 1000,
            height: 600,
            images: null,
            imageSrc: '',
            tableHeader: [
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
            ],
            tableData: [],
            template_id: '',
            template: '',
            initialData: ''
        };
    },
    methods: {
        formatDate(date) {
            return moment(date).format('YYYY-MM-DD HH:mm:ss');
        },
        async getAvailableTemplate() {
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
        },
        handleEdit(row) {
            row.editable = true;
        },
        generateTemplate(template_id, bbox) {
            let myShapes = [];
            bbox.forEach(function (element, index) {
                var myContent = element.hasOwnProperty('tag') ? element['tag'] : '';
                var label_x = element['points'][0][0];
                var label_y = element['points'][0][1];
                var label_width = element['points'][1][0] - element['points'][0][0];
                var label_height = element['points'][2][1] - element['points'][1][1];
                myShapes.push({
                    type: 'rect',
                    name: template_id,
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
        templateOCR(template_id) {
            this.$store.commit('TemplateIdUpdate', template_id);
            this.$router.push({ name: 'TemplateOCR' });
        },
        async handleLook(template_id, userType) {
            this.template_id = template_id;
            try {
                const response = await axios.get('/template_crud/get_template_detail/' + this.template_id);
                this.template = response['data'];
                let bbox = this.template.points_list.filter((item) => item.type === userType);
                this.initialData = this.generateTemplate(template_id, bbox);
                this.imageSrc = 'data:image/png;base64,' + this.template.image;
            } catch (error) {
                if (error.code === 'ERR_NETWORK') {
                    this.status = 'network';
                }
                return error;
            }
        },
        handleConfirm(row) {
            row.editable = false;
        },
        handleDelete(template_id) {
            ElMessageBox.confirm('此操作將永久刪除該模板, 是否繼續?', '提示', {
                confirmButtonText: '確定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(async () => {
                    try {
                        const response = await axios.delete('/template_crud/delete_template/' + template_id);
                        if (!response.error) {
                            this.$message({
                                type: 'success',
                                message: '刪除成功!'
                            });
                            this.tableData = await this.getAvailableTemplate();
                        } else {
                            this.$message({
                                type: 'error',
                                message: '刪除失敗!'
                            });
                        }
                    } catch (error) {
                        this.$message({
                            type: 'error',
                            message: '刪除失敗!'
                        });
                        return error;
                    }
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消刪除'
                    });
                });
        },
        prepend(index) {
            item.editable = true;
            this.tableData.splice(index, 0, item);
        },
        append(index) {
            item.editable = true;
            this.tableData.splice(index + 1, 0, item);
        },
        deleteCurrentColumn(index) {
            this.tableHeader.splice(index, 1);
        },
        insertBefore(index) {
            header.editable = true;
            this.tableHeader.splice(index, 0, header);
        },
        createTemplate() {
            this.$store.commit('createNewUpdate', true);
            this.$router.push({ name: 'SelfDefine1' });
        },
        editTemplate() {
            this.$store.commit('recsClear');
            this.template.points_list.forEach((box) => {
                this.$store.commit('recsUpdate', {
                    type: box.type,
                    data: {
                        startPointX: box.points[0][0],
                        startPointY: box.points[0][1],
                        endPointX: box.points[2][0],
                        endPointY: box.points[2][1],
                        scaleX: 1,
                        scaleY: 1,
                        width: box.points[2][0] - box.points[0][0],
                        height: box.points[2][1] - box.points[0][1],
                        canDelete: true,
                        canEdit: true,
                        canSave: false,
                        name: box.tag
                    }
                });
            });
            sessionStorage.imageSource = 'data:image/png;base64,' + this.template.image;
            this.$store.commit('templateNameUpdate', this.template.template_name);
            this.$store.commit('templateIdUpdate', this.template_id);
            this.$router.push({ path: '/features/general/self-define/step/2' });
        },
        downloadTemplate() {
            let template_info_json = JSON.stringify(this.template);
            let blob = new Blob([template_info_json], { type: 'text/plain;charset=utf-8' });
            let url = URL.createObjectURL(blob);
            let link = document.createElement('a');
            link.href = url;
            link.download = `${this.template.template_name}.json`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        },
        deleteTemplate() {
            ElMessageBox.confirm('此操作將永久刪除該模板, 是否繼續?', '提示', {
                confirmButtonText: '確定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(async () => {
                    try {
                        const response = await axios.delete('/template_crud/delete_template/' + this.template_id);
                        if (!response.error) {
                            this.$message({
                                type: 'success',
                                message: '刪除成功!'
                            });
                            this.tableData = await this.getAvailableTemplate();
                        } else {
                            this.$message({
                                type: 'error',
                                message: '刪除失敗!'
                            });
                        }
                    } catch (error) {
                        this.$message({
                            type: 'error',
                            message: '刪除失敗!'
                        });
                        return error;
                    }
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消刪除'
                    });
                });
        }
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
                            <el-button size="big" type="info" @click="handleLook(scope.row.template_id, this.myModel.code)">檢視</el-button>
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
                        <SelectButton v-model="myModel" :options="models" optionLabel="name" @click="handleLook(this.template_id, this.myModel.code)" />
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
