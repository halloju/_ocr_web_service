<script>
import Annotation from '@/components/Annotation.vue';
import { onBeforeRouteLeave } from 'vue-router';
import { mapState } from 'vuex';
import { ElMessageBox, ElMessage, ElLoading } from 'element-plus';
import UploadImage from '@/components/UploadImage.vue';
import useAnnotator from '@/mixins/useAnnotator.js';
import { apiClient } from '@/service/auth.js';
import img2 from '@/assets/img/create_template_step2.jpg';
import img3 from '@/assets/img/create_template_step3.jpg';
import img4 from '@/assets/img/create_template_step4.jpg';
import { error_table, default_error_msg } from '@/constants.js';

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
            currentStep: this.$store.state.createNew ? 0 : 1,
            template_id: sessionStorage.getItem('template_id') || '',
            pageTitle: ['Step 2 文字位置標註', 'Step 3 方塊位置標註', 'Step 4 遮罩位置標註'],
            pageDesc: [
                '框選的區域，後續可辨識出當中的文字。請框選要項值可能書寫的區域，並排除要項標題。舉例來說，若要辨識文件序號，請框選如下圖中的藍框。',
                '框選的區域，後續可辨識是否有被勾選或填滿。舉例來說，若要辨識新申請、變更、取消是否有被勾選，請框選如下圖中的三個綠框。p.s. 若沒有要辨識的方塊，請跳過此步驟！',
                '請框選模板中會變動的區域。舉例來說，要項值的書寫區域，或是人證上的照片等，如下圖中的橘框。p.s. 此步驟可能提升模板辨識的準確率，但非必要！'
            ],
            pageImg: [img2, img3, img4],
            progressSteps: [
                {
                    title: '圖檔上傳',
                    status: this.$store.state.createNew ? 'now' : 'done'
                },
                {
                    title: '文字標註',
                    status: this.$store.state.createNew ? 'next' : 'now'
                },
                {
                    title: '方塊標註',
                    status: 'next'
                },
                {
                    title: '遮罩標註',
                    status: 'next'
                },
                {
                    title: '模板確認',
                    status: 'next'
                }
            ],
            processType: 'basic'
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
        onBeforeRouteLeave((to, from, next) => {
            if (to.path != '/features/general/model-list') {
                ElMessageBox.confirm('回到上一步會清空所有編輯紀錄，是否確定刪除?', '警告', {
                    confirmButtonText: '確定',
                    cancelButtonText: 'Cancel',
                    type: 'error',
                    center: true
                })
                    .then(() => {
                        sessionStorage.clear();
                        next();
                    })
                    .catch(() => {
                        next(false);
                    });
            } else {
                next();
            }
        });
        const { rectangleTypes } = useAnnotator();
        return {
            rectangleTypes
        };
    },
    methods: {
        next() {
            this.isEditing = false;
            var warning_message;
            if (this.currentStep != 0) {
                if (this.rectangleType != 'mask' && this.rectangleType != undefined) {
                    this.getRecsFromLocalStorage().every((box) => {
                        if (box.rectangleType != 'mask') {
                            if (box.annotation.title == undefined || box.annotation.title == '' || box.annotation.filters.length == 0) {
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

            // Set the status of the current step to 'done'
            if (this.currentStep <= this.progressSteps.length) {
                this.progressSteps[this.currentStep].status = 'done';
            }

            // Move to the next step
            if (this.currentStep < 5) {
                this.currentStep++;
            }

            // Set the status of the new current step to 'now'
            if (this.currentStep <= this.progressSteps.length) {
                this.progressSteps[this.currentStep].status = 'now';
            }

            this.isEditing = false;
        },

        previous() {
            if (this.currentStep == 1) {
                const answer = window.confirm('回到上一步會清空所有編輯紀錄，是否確定刪除?');
                if (answer) {
                    sessionStorage.clear();

                    // Set the status of the current step to 'next'
                    if (this.currentStep < this.progressSteps.length) {
                        this.progressSteps[this.currentStep].status = 'next';
                    }

                    this.currentStep--;

                    // Set the status of the new current step to 'now'
                    if (this.currentStep >= 0 && this.currentStep < this.progressSteps.length) {
                        this.progressSteps[this.currentStep].status = 'now';
                    }
                } else {
                    ElMessage.info('已取消');
                    return;
                }
            } else if (this.currentStep > 1) {
                // Set the status of the current step to 'next'
                if (this.currentStep < this.progressSteps.length) {
                    this.progressSteps[this.currentStep].status = 'next';
                }

                this.currentStep--;

                // Set the status of the new current step to 'now'
                if (this.currentStep >= 0 && this.currentStep < this.progressSteps.length) {
                    this.progressSteps[this.currentStep].status = 'now';
                }
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
                    ],
                    filters: box.annotation.filters
                    // box.rectangleType === 'text' ? ['tchinese', 'english', 'number', 'symbol'] : ( box.rectangleType === 'box' ? ['checkbox'] : null )
                });
            });

            if (this.boxes.length === 0) {
                this.$message({
                    message: '請至少標註一個方塊/文字',
                    type: 'warning'
                });
                return;
            } else {
                var num = 0;
                for (var box of this.boxes) {
                    if (box['type'] === 'mask') {
                        num++;
                    }
                }
                if (num == this.boxes.length) {
                    this.$message({
                        message: '請至少標註一個方塊/文字',
                        type: 'warning'
                    });
                    return;
                }
            }

            let body;
            let action;
            console.log(this.boxes)
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
            apiClient
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
                        this.$router.push({ name: 'ModelList' }).catch((err) => {
                            console.log(err);
                        });

                        console.log('success');
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
                    let error_msg = default_error_msg;
                    if (typeof err.response.data === 'object' && 'mlaas_code' in err.response.data) {
                        console.log(err.response.data.mlaas_code);
                        if (err.response.data.mlaas_code in error_table) error_msg = error_table[err.response.data.mlaas_code] + ' (' + err.response.data.mlaas_code + ')';
                    }
                    ElMessageBox.confirm(error_msg, '失敗', {
                        confirmButtonText: '確定',
                        type: 'error',
                        center: true,
                        showclose: false,
                        showCancelButton: false,
                        closeOnClickModal: false,
                        roundButton: true
                    });
                })
                .finally(() => {
                    loading.close();
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
            sessionStorage.clear();
            // this.$store.commit('setTemplateName', '');
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
        },
        getOcrConfig() {
            const ocrTypes = {
                general: {
                    title: '全文辨識',
                    subtitle: '全文辨識',
                    description: '請上傳一張或多張圖片，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/gp_ocr',
                    useModelComplexity: true,
                    useLanguage: true,
                    defaultImgURL: '',
                    category: {
                        name: 'general',
                        limit: 20
                    },
                    explanation: '',
                    file: null
                }
            };
            return ocrTypes['general'];
        },
        async cancel() {
            await ElMessageBox.confirm('是否確定取消新增', '提示', {
                confirmButtonText: '確定',
                cancelButtonText: '取消',
                type: 'warning'
            });
            this.clearState();
            this.$router.push({ name: 'ModelList' });
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
    <div class="layoutZoneContainer">
        <div style="display: flex; align-items: center; margin-bottom: 20px; margin-top: 20px">
            <p>新增辨識模板</p>
            <div style="flex: 1; text-align: center">
                <div class="progressbarContainer">
                    <ul>
                        <li v-for="(step, index) in progressSteps" :key="index" :class="step.status">
                            <div class="progressTitle">{{ step.title }}</div>
                            <div class="progressDot"></div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <div style="margin-bottom: 20px; margin-top: 20px">
            <div style="display: flex; align-items: center">
                <div style="display: flex; align-items: center; margin-right: 20px">
                    <p style="margin-right: 10px; margin-bottom: 0px">模板名稱：</p>
                    <input class="uiStyle" type="text" :disabled="disableInput" v-model="this.input" />
                    <div class="bx-btn-set" style="margin-left: 20px">
                        <button class="uiStyle sizeS btnGreen" @click="toggleEditSave">
                            {{ buttonText }}
                        </button>
                        <div class="p-fluid" v-if="this.isFinal"></div>
                    </div>
                    <router-view />
                </div>
                <div v-if="useModelComplexity" style="display: flex; align-items: center">
                    <p style="margin-right: 10px">使用高精準度模型：</p>
                    <div class="switchField">
                        <label class="switch">
                            <input type="checkbox" id="switch" v-model="switchValue" />
                            <span class="slider round"></span>
                        </label>
                    </div>
                </div>
                <p v-if="useModelComplexity" style="margin-left: 10px; color: red">*注意，當您使用高精準度模型時會耗時較久</p>
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
                        dataCallback=""
                        initialDataId=""
                        image_cv_id=""
                        :rectangleType="rectangleType"
                        :localStorageKey="localStorageKey"
                        :setShowText="true"
                        height="40vh"
                        :justShow="true"
                        :hasTitle="false"
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
        <div style="display: flex; justify-content: center; align-items: space-between; margin-bottom: 20px; margin-top: 0rem">
            <button v-if="currentStep !== 0" class="uiStyle sizeM btnGreen minLength" @click="previous" style="margin-right: 20px">上一步</button>
            <button v-if="currentStep !== 0" class="uiStyle sizeM btnDarkBlue minLength" @click="cancel" style="margin-right: 20px">取消新增</button>
            <button v-if="!this.isFinal" class="uiStyle sizeM btnGreen minLength" @click="next" style="margin-right: 20px">下一步</button>
            <button v-else class="uiStyle sizeM btnGreen minLength" @click="upload" v-bind:class="{ 'p-disabled': !templateNameEdit }" v-bind:disabled="!templateNameEdit" v-bind:title="!templateNameEdit ? '請確認模板名稱' : ''" type="success">
                提交
            </button>
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
