<script>
import Annotation from '@/components/Annotation.vue';
import { onBeforeRouteLeave } from 'vue-router';
import { mapState } from 'vuex';
import { ElMessageBox, ElMessage, ElLoading } from 'element-plus';
import UploadImage from '@/components/UploadImage.vue';
import useAnnotator from '@/mixins/useAnnotator.js';
import { initializeClient } from '@/service/auth.js';

export default {
    components: {
        Annotation,
        UploadImage
    },
    name: 'SelfDefine',
    props: {
        Boxes: {
            type: Array
        }
    },
    data() {
        return {
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
            input: this.$store.state.templateName || '',
            imageSrc: sessionStorage.getItem('imageSource') || '',
            initialData: {
                text: [],
                box: [],
                mask: []
            },
            createNew: this.$store.state.createNew,
            currentStep: this.$store.state.createNew? 0: 1,
            template_id: sessionStorage.getItem('template_id') || '',
            apiClient: null,
            pageTitle: ['Step 2 文字位置標註', 'Step 3 方塊位置標註', 'Step 4 遮罩位置標註'],
            pageDesc: ['框選的區域，後續可辨識出當中的文字。請框選要項值可能書寫的區域，並排除要項標題。舉例來說，若要辨識文件序號，請框選如下圖中的藍框。',
                '框選的區域，後續可辨識是否有被勾選或填滿。舉例來說，若要辨識新申請、變更、取消是否有被勾選，請框選如下圖中的三個綠框。p.s. 若沒有要辨識的方塊，請跳過此步驟！', '請框選模板中會變動的區域。舉例來說，要項值的書寫區域，或是人證上的照片等，如下圖中的橘框。p.s. 此步驟可能提升模板辨識的準確率，但非必要！'],
            pageImg: ['src/assets/img/create_template_step2.jpg', 'src/assets/img/create_template_step3.jpg', 'src/assets/img/create_template_step4.jpg']
        };
    },
    created() {
        // 直接跳到非上傳頁，原本圖檔資料均需要留著
        this.$store.commit('createNewUpdate', false);
    },
    mounted() {
        this.isFinalStep();
        this.initializeClient();
    },
    setup() {
        onBeforeRouteLeave((to, from) => {
            if (to.path != '/features/general/model-list') {
                const answer = window.confirm('回到上一步會清空所有編輯紀錄，是否確定刪除?');
                if (!answer) {
                    sessionStorage.clear();
                    return false;
                }
            }
        });
        const { rectangleTypes } = useAnnotator();
        return {
            rectangleTypes
        };
    },
    methods: {
        async initializeClient() {
            this.apiClient = await initializeClient();
        },
        next() {
            this.isEditing = false;
            var warning_message;
            if (this.currentStep != 0) {
                if (this.rectangleType != 'mask' && this.rectangleType != undefined) {
                    this.getRecsFromLocalStorage().every((box) => {
                        if (box.rectangleType != 'mask') {
                            if (box.annotation.title == undefined || box.annotation.title == '') {
                                this.isEditing = true;
                                return false;
                            }
                        }
                        return true;
                    });
                }
                warning_message = '請先完成編輯';
            } else {
                if (sessionStorage.getItem('imageSource')) {
                    this.imageSrc = sessionStorage.getItem('imageSource');
                } else {
                    this.isEditing = true;
                }
                warning_message = '請先上傳圖片';
            }

            if (this.isEditing) {
                this.$message({
                    message: warning_message,
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
            if (this.currentStep == 1) {
                const answer = window.confirm('回到上一步會清空所有編輯紀錄，是否確定刪除?');
                if (answer) {
                    sessionStorage.clear();
                    this.currentStep--;
                } else {
                    ElMessage.info('已取消');
                    return;
                }
            } else if (this.currentStep > 1) {
                this.currentStep--;
            }
        },
        getRecsFromLocalStorage() {
            const recs = [];
            this.rectangleTypes.forEach((type) => {
                const rec = JSON.parse(sessionStorage.getItem(type.code) || '[]');
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
            if (!this.template_id) {
                const image = new window.Image();
                image.src = sessionStorage.imageSource;
                body = {
                    image: image.src.split(',').pop(),
                    is_no_ttl: false,
                    points_list: this.boxes,
                    template_name: this.input,
                    is_public: false
                };
                action = 'create_template';
            } else {
                body = {
                    points_list: this.boxes,
                    template_name: this.input,
                    template_id: this.template_id
                };
                action = 'update_template';
            }
            const loading = ElLoading.service({
                lock: true,
                text: 'Loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            this.apiClient
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
                        console.log(res);
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
                    console.log(err);
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
                loading.close();
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
            sessionStorage.clear();
            this.$store.commit('setTemplateName', '');
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
            sessionStorage.setItem('templateName', this.input);
        },
        Upload(val) {
            this.isOK = val;
        }
    },
    computed: {
        ...mapState(['templateName']),
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
        },
        tooltip_text() {
            if (this.currentStep == 0) return '請上傳圖片後點我';
            else return '請框好位置後點我';
        }
    },
    watch: {
        currentStep() {
            this.isFinalStep();
        },
        templateName(newName) {
            this.input = newName;
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
                        <h5>{{ this.pageTitle[this.currentStep - 1]  }}</h5>
                        <p>{{ this.pageDesc[this.currentStep - 1] }}</p>
                        <img :src="this.pageImg[this.currentStep - 1]" height="200"/>
                        <img v-if="this.currentStep == 0" :src="this.imageSource" class="img-fluid" />
                    </div>
                    <div class="col-6">
                        <el-button v-if="currentStep != 0" class="pi p-button-warning" @click="previous" v-tooltip="'返回上一步'" type="warning">上一步</el-button>
                        <el-button v-if="!this.isFinal" :class="{ 'pi p-button-success': !isEditing, 'pi p-button-fail': isEditing }" @click="next" v-tooltip="this.tooltip_text" type="success">下一步</el-button>
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
                <Annotation :key="currentStep" containerId="my-pic-annotation-output" :imageSrc="imageSrc" :editMode="editMode" dataCallback="" initialDataId="" image_cv_id="" :rectangleType="rectangleType" :localStorageKey="localStorageKey" :setShowText="true" height="600" :justShow="true" />
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
