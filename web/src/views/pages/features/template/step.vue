<script>
import Annotation from '@/components/Annotation.vue';
import { onBeforeRouteLeave } from 'vue-router';
import { mapState, mapMutations } from 'vuex';
import { ElMessageBox, ElMessage, ElLoading } from 'element-plus';
import UploadImage from '@/components/UploadImage.vue';
import TemplateCarousel from '@/views/pages/features/template/TemplateCarousel.vue';
import useAnnotator from '@/mixins/useAnnotator.js';
import { apiClient } from '@/service/auth.js';

import Icon from '@/components/Icon.vue';
import { error_table, default_error_msg } from '@/constants.js';
import img1 from '@/assets/img/template_step/step1.png';
import img2 from '@/assets/img/template_step/step2.png';
import img3_1 from '@/assets/img/template_step/step3-1.png';
import img3_2 from '@/assets/img/template_step/step3-2.png';
import img4 from '@/assets/img/template_step/step4.png';
import img5 from '@/assets/img/template_step/step5.png';

export default {
    components: {
        Icon,
        Annotation,
        UploadImage,
        TemplateCarousel
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
            input: this.$store.state.templateName || '',
            imageSrc: sessionStorage.getItem('imageSource') || '',
            initialData: {
                text: [],
                box: [],
                mask: []
            },
            createNew: this.$store.state.createNew,
            currentStep: this.$store.state.createNew ? 0 : 1,
            showCarousel: true,
            template_id: sessionStorage.getItem('template_id') || '',
            pageTitle: ['Step 2 文字位置標註', 'Step 3 方塊位置標註', 'Step 4 遮罩位置標註'],
            pageInfo: [
                {
                    pageDesc: `<ul class="instructions">
                        <li>請上傳<span class="red-text">空白的</span>表格或申請書圖檔 (例:未填寫的電子函證授權書、未填寫的XXX)</li>
                        <li>若<span class="red-text">無空白的</span>表格或申請書圖檔善用<strong class="bold-text">Step4.遮罩標註</strong></li>
                        <li>用來建立模板的圖片請勿包含個人機敏資訊及本行營業秘密，請參閱「IC-030_玉山銀行員工資訊安全作業要點」第六條（十）之即時通訊軟體使用規範</li>
                    </ul>`,
                    image: img1
                },
                {
                    pageDesc: `<ul class="instructions">
                        <li>框選文字填寫範圍<span class="red-text">不含欄位名稱、表格框線或底線</span></li>
                        <li>框選<span class="red-text">純文字</span>辨識範圍<span class="red-text">不含勾選框、原留印鑑框</span></li>
                    </ul>`,
                    image: img2
                },
                {
                    pageDesc: `<ul class="instructions">
                        <li>只框選方框處，<span class="red-text">不含欄位名稱、選項文字</span>\n例：確認顧客勾選項目為何，只需框選方框處，<span class="red-text">不含</span>選項文字「新申請」、「變更」、「取消」。</li>
                    </ul>
                    <img src="${img3_2}" height="30" margin="10px 0px 0px 20px" />`,
                    image: img3_1
                },
                {
                    pageDesc:`<ul class="instructions">
                        <li>例1: 以玉山名片為例, 遮罩標註會變動的內容與區域(部處、職稱、姓名等資訊)，僅留上半部進行模版比對。</li>
                        <li>例2: 以香港傳真交易申請書為例，若缺乏空白模板，須將表單欄位的填寫內容遮罩，使表單像未填寫過的空白表單 (類似立可帶的功用！)</li>
                    </ul>`,
                    image: img4
                },
                {
                    pageDesc: ``,
                    image: img5
                }
            ],
            stepsInfo: [
                {
                    first: '① 命名「模板名稱」',
                    second: '② 點選「+」按鈕，選取您欲建立的模版圖片。'
                },
                {
                    first: '① 點選「新增標註」',
                    second: '② 框選欲辨識的文字填寫範圍->輸入「欄位名稱」->選擇「區塊包含的字符」。(若有勾選框或簽名/印鑑欄位，請於下一步方塊標註時新增)'
                },
                {
                    first: '① 點選「新增標註」',
                    second: '② 框選欲辨識的勾選框、原留印鑑(簽名) -> 輸入「欄位名稱」-> 選擇「區塊包含的項目」。',
                    details: ['※勾選框：辨識勾選、塗黑等方塊', '※原留印鑑框：辨識顧客是否有簽名或留存印鑑']
                },
                {
                    first: '① 點選「新增標註」',
                    second: '② 框選表格、申請書或文件圖檔上的填寫區域與所有會變動的內容/你希望變成空白的內容。'
                },
                {
                    first: '確認文字標註、方塊標註、遮罩標註皆無誤即可送出新增模板',
                    second: ' '
                }
                // ... add the other 3 info pairs here
            ],
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
        toggleCarousel() {
            console.log(this.showCarousel)
            this.showCarousel = !this.showCarousel; // 改变 Carousel 显示状态的方法
        },
        next() {
            this.isEditing = false;
            var warning_message;
            if (this.currentStep != 0) {
                let issueDescriptions = [];
                if (this.rectangleType != 'mask' && this.rectangleType != undefined) {
                    this.getRecsFromLocalStorage().every((box, index) => {
                        if (box.rectangleType != 'mask') {
                            let issue = { index: index, box: box, problems: [] };
                            console.log(box.annotation.title)
                            if (box.annotation.title === undefined || box.annotation.title === '' || box.annotation.title === null) {
                                this.isEditing = true;
                                issue.problems.push("名稱為空");
                            }
                            if (box.annotation.filters === null || box.annotation.filters.length === 0) {
                                this.isEditing = true;
                                issue.problems.push("區域字符未選擇");
                            }

                            // If there are problems, push the issue object to the issues array
                            if (issue.problems.length > 0) {
                                const problemsString = issue.problems.join(', ');
                                console.log(issue.problems)
                                issueDescriptions.push(`${this.rectangleType}.${issue.index+1}: ${problemsString}。`);
                                return false; // Stop the every loop because there is an issue
                            }
                        }
                        return true; // Continue the every loop if no issues
                    });
                }

                // Join all issue descriptions into one string, separated by semicolons
                let allIssuesString = issueDescriptions.join('; ');
                console.log(allIssuesString);
                warning_message = '請先完成編輯:'+allIssuesString;
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
            if (this.currentStep == 0) {
                this.$store.commit('createNewUpdate', false);
                this.showCarousel = false;
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
                ElMessageBox.confirm('回到上一步會清空所有編輯紀錄，是否確定刪除?', '警告', {
                    confirmButtonText: '確定',
                    cancelButtonText: 'Cancel',
                    type: 'error',
                    center: true
                })
                    .then(() => {
                        sessionStorage.clear();
                        // Set the status of the current step to 'next'
                        if (this.currentStep < this.progressSteps.length) {
                            this.progressSteps[this.currentStep].status = 'next';
                        }
                        this.showCarousel = false;
                        this.$store.commit('createNewUpdate', true);
                        this.currentStep--;

                        // Set the status of the new current step to 'now'
                        if (this.currentStep >= 0 && this.currentStep < this.progressSteps.length) {
                            this.progressSteps[this.currentStep].status = 'now';
                        }
                    })
                    .catch(() => {
                        return;
                    });
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
        saveInput() {
            sessionStorage.setItem('templateName', this.input);
        },
        Upload(val) {
            this.isOK = val;
        },
        getOcrConfig() {
            const ocrTypes = {
                general: {
                    title: '全文辨識',
                    subName: '全文辨識',
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
        },
        pageHeadInfo() {
            if (this.currentStep >= 0 && this.currentStep <= this.stepsInfo.length) {
                const info = this.stepsInfo[this.currentStep];
                let result = '';
                if (info.details) {
                    result = `${info.first}`;
                    result += '<br>&nbsp&nbsp&nbsp&nbsp' + info.details.join('<br>&nbsp&nbsp&nbsp&nbsp');
                    result += '<br>' + `${info.second}`;
                } else {
                    result = `${info.first}<br>${info.second}`;
                }
                return result;
            }
            return ''; // default value
        },
        popInfo() {
            if (this.currentStep >= 0 && this.currentStep <= this.stepsInfo.length) {
                const info = this.pageInfo[this.currentStep];
                return info;
            }
            return null; // default value
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
        <div style="display: flex; align-items: center; margin-bottom: 10px; margin-top: 0px">
            <div style="margin-bottom: 20px; margin-top: 0px">
                <div style="display: flex; align-items: center;">
                    <p class="title">新增辨識模板</p>
                    <TemplateCarousel :show="showCarousel"/>
                    <div class="align-items-center" style="display: inline-flex; padding-left: 3px; margin-bottom: 1rem" @click="toggleCarousel">
                        <icon type="info" fill="#3c4c5e" title="完整操作說明" width="20px" height="20px" />
                    </div>
                </div>
                <div style="display: flex; align-items: center">
                    <div style="display: flex; align-items: center; margin-right: 10px">
                        <p style="margin-right: 2px; color: red">*</p>
                        <p style="margin-right: 10px; margin-bottom: 0px">模板名稱：</p>
                        <input class="uiStyle" type="text" v-model="input" @input="saveInput" @keyup.enter="saveInput" />
                        <div class="p-fluid" v-if="this.isFinal"></div>
                        <router-view />
                    </div>
                </div>
            </div>
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
        <div>
            <p v-html="pageHeadInfo" class="m-0"></p>
            <el-popover v-if="popInfo" placement="right" :width="1000"
                popper-style="box-shadow: rgb(14 18 22 / 35%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px;">
                <template #reference>
                    <div class="m-2 align-items-center" style="display: inline-flex;">
                        <icon type="info" fill="#45b29d" title="操作說明" width="28px" height="28px" />
                        <span style="display: inline-block; color: #45b29d; font-weight: 900">操作說明</span>
                    </div>
                </template>
                <template #default>
                    <img :src="popInfo.image" height="200" />
                    <p v-html="popInfo.pageDesc"></p>
                </template>
            </el-popover>
        </div>
        <div v-if="currentStep > 0" class="grid p-fluid">
            <div class="col-12">
                <Annotation :key="currentStep" containerId="my-pic-annotation-output" :imageSrc="imageSrc"
                    :editMode="editMode" initialDataId="" image_cv_id="" :rectangleType="rectangleType"
                    :localStorageKey="localStorageKey" :setShowText="true" height="45vh" :justShow="true"
                    :hasTitle="false" />
            </div>
        </div>
        <div v-else class="grid p-fluid">
            <div class="col-12">
                <UploadImage :isUploaded="true" :createNew="createNew" @updateStatus="Upload" />
            </div>
        </div>
        <div style="display: flex; justify-content: center; align-items: space-between; margin-bottom: 20px; margin-top: 0rem">
            <button v-if="currentStep !== 0" class="uiStyle sizeM btnGreen minLength" @click="previous" style="margin-right: 20px">上一步</button>
            <button v-if="currentStep !== 0" class="uiStyle sizeM btnDarkBlue minLength" @click="cancel" style="margin-right: 20px">取消新增</button>
            <button v-if="!this.isFinal" class="uiStyle sizeM btnGreen minLength" @click="next" style="margin-right: 20px">下一步</button>
            <button v-else class="uiStyle sizeM btnGreen minLength" @click="upload" type="success">提交</button>
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

.instructions > li {
    margin-left: 20px;
    display:list-item;
    list-style-type: disc;
}
.red-text {
  color: red; /* This will make the text red */
}
</style>
