<template>
    <div class="grid">
        <div class="col-7">
            <div class="card" style="height: 850px; overflow-y: scroll">
                <h2>個人模板檢視</h2>
                <el-table :data="formattedTableData" style="width: 100%">
                    <el-table-column :prop="item.prop" :label="item.label" v-for="(item, index) in tableHeader" :key="item.prop" :width="item.width">
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
                    <el-table-column label="操作" width="320px">
                        <template #default="scope">
                            <el-button v-show="!scope.row.editable" size="big" @click="scope.row.editable = true">編輯</el-button>
                            <el-button v-show="scope.row.editable" size="small" type="success" @click="scope.row.editable = false">確認</el-button>
                            <el-button size="big" type="info" @click="">檢視</el-button>
                            <el-button size="big" type="danger" @click="handleDelete(scope.$index)">删除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>
        <div class="col-5">
            <div class="card" style="height: 850px; overflow-y: scroll">
                <h5>請選擇標註模式</h5>
                <div class="flex flex-column card-container">
                    <div class="flex align-items-center justify-content-center h-4rem font-bold border-round m-2">
                        <SelectButton v-model="myModel" :options="models" optionLabel="name" />
                    </div>
                    <div class="flex align-items-center justify-content-center h-4rem font-bold border-round m-4">
                        <Button icon="pi pi-download" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'下載模板設定檔'" @click="" />
                        <Button icon="pi pi-pencil" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'編輯模版'" @click="getAvailableTemplate" />
                        <Button icon="pi pi-trash" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'刪除模板'" @click="" disabled="true" />
                    </div>
                    <div class="flex align-items-center justify-content-center h-100rem font-bold border-round m-2">
                        <AnnotationVertical
                            containerId="my-pic-annotation-output"
                            :editMode="false"
                            :imageSrc="imageSrc"
                            :width="width"
                            :height="height"
                            dataCallback=""
                            :initialData="getShapeData"
                            :initialDataId="initialDataId"
                            :justShow="true"
                        ></AnnotationVertical>
                    </div>
                    <div class="flex align-items-center justify-content-center h-100rem font-bold border-round m-2">
                        <!-- <BoxCard boxName="text" :boxTitle="myModel.name" /> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import moment from 'moment'
import axios from "axios";
import PhotoService from '@/service/PhotoService';
import AnnotationVertical from '@/components/AnnotationVertical.vue';

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
        getShapeData() {
            let myShapes = []
            let image_cv_id = JSON.stringify(this.$store.state.general_upload_res[0].image_cv_id);
            let regData = this.$store.state.general_upload_res[0].ocr_results;
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
        formattedTableData() {
            return this.tableData.map(row => {
                return {
                ...row,
                updated_at: this.formatDate(row.updated_at)
                };
            });
        },
    },
    data() {
        return {
            models: [{ name: '文字' }, { name: '方塊' }, { name: '遮罩' }],
            myModel: { name: '文字' },
            width: 1000,
            height: 600,
            images: null,
            imageSrc: this.$store.state.general_upload_image[0].reader,
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
                    width: '200px'
                },
                {
                    prop: 'updated_at',
                    label: '更新日期',
                    editable: false,
                    type: 'date',
                    width: '200px'
                }
            ],
            tableData: [],
        };
    },
    methods: {
        formatDate(date) {
            return moment(date).format('YYYY-MM-DD HH:mm:ss');
        },
        async getAvailableTemplate() {
            let user_id = '13520';
            let tableData = []
            try {
                const response = await axios.get("/template_crud/get_available_templates/"+ user_id, {
                    params: {
                        is_public: false,
                    }
                })
                tableData = response["data"]["available_templates"];
                console.log(tableData)
                return tableData;
            } catch (error) {
                console.log(error)
                if (error.code === 'ERR_NETWORK') {
                    this.status = 'network'
                }
                return error
            }
        },
        handleEdit(row) {
            row.editable = true;
        },
        handleDelete(index) {
            this.tableData.splice(index, 1);
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
        }
    }
};
</script>