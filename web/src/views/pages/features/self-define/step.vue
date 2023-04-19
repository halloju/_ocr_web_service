<script>
import Annotation from '@/components/Annotation.vue';
import axios from 'axios';
import { mapState } from 'vuex';
import { ElMessageBox } from 'element-plus';
import UploadImage from '@/components/UploadImage.vue';
import useAnnotator from '@/mixins/useAnnotator.js';

export default {
    components: {
        Annotation,
        UploadImage
    },
    name: 'SelfDefine',
    data() {
        return {
            nestedRouteItems: [
                {
                    label: '模板圖檔上傳',
                    to: '/features/general/self-define/step/1'
                },
                {
                    label: '文字位置標註',
                    to: '/features/general/self-define/step/2'
                },
                {
                    label: '方塊位置標註',
                    to: '/features/general/self-define/step/3'
                },
                {
                    label: '遮罩位置標註',
                    to: '/features/general/self-define/step/4'
                },
                {
                    label: '確認',
                    to: '/features/general/self-define/step/5'
                }
            ],
            isFinal: false,
            boxes: [],
            boxNames: ['text', 'box', 'mask', 'all'],
            isShapesVisible: {
                text: true,
                box: true,
                mask: true
            },
            isEditing: false,
            disableInput: false,
            templateNameEdit: false,
            input: localStorage.getItem('templateName') || '',
            imageSrc: localStorage.getItem('imageSource') || '',
            initialData: {
                text: [],
                box: [],
                mask: []
            },
            currentStep: 0,
            createNew: this.$store.state.createNew,
            template_id: localStorage.getItem('template_id') || ''
        };
    },
    created() {
        // 直接跳到非上傳頁，原本圖檔資料均需要留著
        this.$store.commit('createNewUpdate', false);
    },
    mounted() {
        this.isFinalStep();
    },
    setup() {
        const { rectangleTypes } = useAnnotator();
        return {
            rectangleTypes
        };
    },
    methods: {
        next() {
            if(this.rectangleType != 'mask'){
                this.getRecsFromLocalStorage().every((box) => {
                if(box.annotation.title == undefined || box.annotation.title == ''){
                    this.isEditing = true;
                    return false;
                }else{
                    return true;
                }
            });
                    
            }
            
            if (this.isEditing) {
                this.$message({
                    message: '請先完成編輯',
                    type: 'warning'
                });
                return;
            }
            if (this.currentStep < 5) {
                this.currentStep++;
            }
            this.isEditing = false;
        },
        previous() {
            if (this.currentStep > 0) {
                this.currentStep--;
            }
        },
        getRecsFromLocalStorage() {
            const recs = [];
            this.rectangleTypes.forEach((type) => {
                const rec = JSON.parse(localStorage.getItem(type.code) || '[]');
                if (rec) {
                    recs.push(...rec);
                }
            });
            return recs;
        },
        upload() {
            if (this.input === '') {
                this.$message({
                    message: '請輸入模板名稱',
                    type: 'warning'
                });
                return;
            }
            // clear state
            this.boxes = [];
            this.getRecsFromLocalStorage().forEach((box) => {
                this.boxes.push({
                    type: box.rectangleType,
                    tag: box.annotation.title,
                    points: [
                        [box.x, box.y],
                        [box.x + box.width * box.scaleX, box.y],
                        [box.x + box.width * box.scaleX, box.y + box.height * box.scaleY],
                        [box.x, box.y + box.height * box.scaleY]
                    ]
                });
            });

            if (this.boxes.length === 0) {
                this.$message({
                    message: '請至少標註一個方塊',
                    type: 'warning'
                });
                return;
            }

            let body;
            let action;
            if (this.createNew) {
                const image = new window.Image();
                image.src = localStorage.imageSource;
                body = {
                    user_id: 12345,
                    image: image.src.split(',').pop(),
                    is_no_ttl: false,
                    points_list: this.boxes,
                    template_name: this.input,
                    is_public: false
                };
                action = 'create_template';
            } else {
                body = {
                    user_id: 12345,
                    points_list: this.boxes,
                    template_name: this.input,
                    template_id: this.template_id
                };
                action = 'update_template';
            }
            axios
                .post(`/template_crud/${action}`, body)
                .then((res) => {
                    if (res.status === 200) {
                        ElMessageBox.confirm('', '成功', {
                            confirmButtonText: '確定',
                            type: 'success',
                            center: true,
                            showclose: false,
                            showCancelButton: false,
                            closeOnClickModal: false,
                            roundButton: true
                        });
                        this.clearState();
                        this.$router.push({ path: '/features/general/model-list' });
                    } else {
                        ElMessageBox.confirm('', '失敗', {
                            confirmButtonText: '確定',
                            type: 'error',
                            center: true,
                            showclose: false,
                            showCancelButton: false,
                            closeOnClickModal: false,
                            roundButton: true
                        });
                    }
                })
                .catch((err) => {
                    ElMessageBox.confirm(err, '失敗', {
                        confirmButtonText: '確定',
                        type: 'error',
                        center: true,
                        showclose: false,
                        showCancelButton: false,
                        closeOnClickModal: false,
                        roundButton: true
                    });
                });
        },
        isFinalStep() {
            if (this.currentStep === 4) {
                this.isFinal = true;
            } else {
                this.isFinal = false;
            }
        },
        clearState() {
            // remove all localStorage
            localStorage.clear();
        },
        onSwitchChange(name, value) {
            this.isShapesVisible[name] = value;
        },
        update(isEditing) {
            this.isEditing = isEditing;
        },
        toggleEditSave() {
            this.templateNameEdit = !this.templateNameEdit;
            this.disableInput = !this.disableInput;
            localStorage.setItem('templateName', this.input);
        },
        Upload(val) {
            this.isOK = val;
        }
    },
    computed: {
        ...mapState(['selfDefinedRecs']),
        buttonText() {
            return this.templateNameEdit ? '編輯' : '確認';
        },
        rectangleType() {
            return this.boxNames[this.currentStep - 1];
        },
        localStorageKey() {
            return this.boxNames[this.currentStep - 1];
        },
        editMode() {
            return this.currentStep < 4;
        }
    },
    watch: {
        currentStep() {
            this.isFinalStep();
            this.imageSrc = localStorage.getItem('imageSource');
        }
    },
    props: {
        step: {
            type: Number
        },
        Boxes: {
            type: Array
        },
        pageTitle: {
            type: String
        },
        pageDesc: {
            type: String
        }
    }
};
</script>
<template>
    <div class="grid p-fluid">
        <div class="col-12">
            <div class="card card-w-title">
                <!-- Breadcrumb -->
                <el-breadcrumb>
                    <el-breadcrumb-item :to="{ path: '/' }">首頁</el-breadcrumb-item>
                    <el-breadcrumb-item :to="{ name: 'Model-List' }">模板辨識</el-breadcrumb-item>
                    <el-breadcrumb-item>模板編輯</el-breadcrumb-item>
                </el-breadcrumb>
                <br />
                <!-- Step -->
                <!-- <Steps :model="nestedRouteItems" :readonly="false" /> -->
                <el-steps :active="currentStep" align-center>
                    <el-step title="模板圖檔上傳" />
                    <el-step title="文字位置標註" />
                    <el-step title="方塊位置標註" />
                    <el-step title="遮罩位置標註" />
                    <el-step title="確認" />
                </el-steps>
                <br />
                <div class="grid">
                    <div class="col-12">
                        <h5>{{ this.pageTitle }}</h5>
                        <p>{{ this.pageDesc }}</p>
                    </div>
                    <div class="col-6">
                        <el-button v-if="currentStep != 0" class="pi p-button-warning" @click="previous" v-tooltip="'返回上一步'" type="warning">上一步</el-button>
                        <el-button v-if="!this.isFinal" :class="{ 'pi p-button-success': !isEditing, 'pi p-button-fail': isEditing }" @click="next" v-tooltip="'請框好位置好點我'" type="success">下一步</el-button>
                        <el-button v-else class="pi p-button-success" @click="upload" v-bind:class="{ 'p-disabled': !templateNameEdit }" v-bind:disabled="!templateNameEdit" v-bind:title="!templateNameEdit ? '請確認模板名稱' : ''" type="success">
                            提交
                        </el-button>
                    </div>
                    <div class="col-6">
                        <div class="input-wrapper">
                            <span class="w-50">模板名稱：</span>
                            <el-input v-model="this.input" placeholder="模板名稱" :disabled="disableInput" />
                            <el-button type="primary" @click="toggleEditSave">{{ buttonText }}</el-button>
                        </div>
                    </div>
                    <div class="p-fluid" v-if="this.isFinal"></div>
                </div>
                <router-view />
            </div>
        </div>
    </div>
    <div v-if="currentStep > 0" class="grid p-fluid">
        <div class="col-12">
            <div class="card">
                <Annotation
                    :key="currentStep"
                    containerId="my-pic-annotation-output"
                    :imageSrc="imageSrc"
                    :editMode="editMode"
                    :language="en"
                    :width="width"
                    :height="height"
                    dataCallback=""
                    initialDataId=""
                    image_cv_id=""
                    :rectangleType="rectangleType"
                    :localStorageKey="localStorageKey"
                />
            </div>
        </div>
    </div>
    <div v-else class="grid p-fluid">
        <div class="col-12">
            <div class="card">
                <UploadImage :isUploaded="true" :createNew="createNew" @updateStatus="Upload" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.input-wrapper {
    display: flex;
    align-items: center;
}

.input-wrapper > * {
    margin-right: 10px;
}

.tooltip:disabled::before {
    content: 'Tooltip text';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    background-color: #000;
    color: #fff;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 14px;
    white-space: nowrap;
}

.tooltip:hover:disabled::before {
    display: block;
}

.tooltip:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.el-button[disabled]:before {
    content: attr(title);
}
</style>
