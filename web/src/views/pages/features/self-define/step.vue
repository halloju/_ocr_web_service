<script>
import Box from '@/components/Box.vue';
import BoxCard from '@/components/BoxCard.vue';
import axios from 'axios';
import { mapState } from 'vuex';
import { ElMessageBox } from 'element-plus';

export default {
    components: {
        BoxCard,
        Box
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
            boxNames: ['text', 'box', 'mask'],
            isShapesVisible: {
                text: true,
                box: true,
                mask: true
            },
            isEditing: false,
            disableInput: false,
            templateNameEdit: false,
            input: this.$store.state.selfDefinedRecs.name
        };
    },
    created() {
        // 直接跳到非上傳頁，原本圖檔資料均需要留著
        this.$store.commit('createNewUpdate', false);
    },
    mounted() {
        this.isFinalStep();
    },
    methods: {
        next() {
            if (this.isEditing) {
                this.$message({
                    message: '請先完成編輯',
                    type: 'warning'
                });
                return;
            }
            const nextStep = this.step + 1;
            this.$router.push({ path: `/features/general/self-define/step/${nextStep}` });
        },
        upload() {
            if (this.input === '') {
                this.$message({
                    message: '請輸入模板名稱',
                    type: 'warning'
                });
                return;
            }

            for (let i = 0; i < this.boxNames.length; i++) {
                this.selfDefinedRecs[this.boxNames[i]].forEach((box) => {
                    this.boxes.push({
                        type: this.boxNames[i],
                        tag: box.name,
                        points: [
                            [box.startPointX, box.startPointY],
                            [box.endPointX, box.startPointY],
                            [box.endPointX, box.endPointY],
                            [box.startPointX, box.endPointY]
                        ]
                    });
                });
            }

            if (this.boxes.length === 0) {
                this.$message({
                    message: '請至少標註一個方塊',
                    type: 'warning'
                });
                return;
            }

            let body;
            let action;
            if (this.selfDefinedRecs.id.length === 0) {
                console.log('create');
                const image = new window.Image();
                image.src = sessionStorage.imageSource;
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
                    template_id: this.selfDefinedRecs.id
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
            if (this.step === 5) {
                this.isFinal = true;
            } else {
                this.isFinal = false;
            }
        },
        clearState() {
            this.$store.commit('recsClear');
            sessionStorage.removeItem('imageSource');
            sessionStorage.filename = '';
            sessionStorage.filesize = 0;
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
            this.$store.commit('templateNameUpdate', this.input);
        }
    },
    computed: {
        ...mapState(['selfDefinedRecs']),
        buttonText() {
            return this.templateNameEdit ? '編輯' : '確認';
        }
    },
    watch: {
        step() {
            this.isFinalStep();
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
                <Steps :model="nestedRouteItems" :readonly="false" />
                <br />
                <div class="grid">
                    <div class="col-12">
                        <h5>{{ this.pageTitle }}</h5>
                        <p>{{ this.pageDesc }}</p>
                    </div>
                    <div class="col-6">
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
    <div class="grid p-fluid">
        <div class="col-12 md:col-8">
            <Box :Boxes="this.Boxes" :isShapesVisible="this.isShapesVisible" @update:isEditing="update" />
        </div>
        <div class="col-12 md:col-4">
            <div class="card" style="overflow-x: scroll">
                <BoxCard :Boxes="this.Boxes" @toggleShowShapes="onSwitchChange" />
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
