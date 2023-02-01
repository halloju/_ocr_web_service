<script>
import Box from '@/components/Box.vue';
import BoxCard from '@/components/BoxCard.vue';
import axios from 'axios';
import { mapState } from 'vuex';

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
                    to: '/features/self-define/step/1'
                },
                {
                    label: '文字位置標註',
                    to: '/features/self-define/step/2'
                },
                {
                    label: '方塊位置標註',
                    to: '/features/self-define/step/3'
                },
                {
                    label: '遮罩位置標註',
                    to: '/features/self-define/step/4'
                },
                {
                    label: '確認',
                    to: '/features/self-define/step/5'
                }
            ],
            breadcrumbHome: { icon: 'pi pi-home', to: '/' },
            breadcrumbItems: [
                { label: '主要功能', to: '#' },
                { label: '自定義模板', to: '#' },
                { label: '新增自定義模板', to: '#' },
                { label: '模板圖檔上傳', to: '#' }
            ],
            isFinal: false,
            boxes: [],
            boxNames: ['text', 'box', 'mask'],
            isShapesVisible: {
                text: true,
                box: true,
                mask: true
            }
        };
    },
    mounted() {
        this.isFinalStep();
    },
    methods: {
        next() {
            const nextStep = this.step + 1;
            this.$router.push({ path: `/features/self-define/step/${nextStep}` });
        },
        upload() {
            const image = new window.Image();
            image.src = sessionStorage.imageSource;

            for (let i = 0; i < this.boxNames.length; i++) {
                this.selfDefinedRecs[this.boxNames[i]].forEach((box) => {
                    this.boxes.push({
                        type: this.boxNames[i],
                        tag: box.name,
                        x_min: box.startPointX,
                        y_min: box.startPointY,
                        x_max: box.endPointX,
                        y_max: box.endPointY
                    });
                });
            }

            axios
                .post('/template/create', {
                    user_id: 12345,
                    image: image.src.split(',').pop(),
                    is_no_ttl: false,
                    bbox: this.boxes,
                    template_name: '身分證',
                    is_public: false
                })
                .then((res) => {
                    if (res.status === 200) {
                        this.$toast.add({
                            severity: 'success',
                            summary: '成功',
                            detail: '新增成功',
                            life: 3000
                        });
                        this.clearState();
                        this.$router.push({ path: '/features/self-define/step/1' });
                    } else {
                        this.$toast.add({
                            severity: 'error',
                            summary: '失敗',
                            detail: '新增失敗',
                            life: 3000
                        });
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        },
        isFinalStep() {
            if (this.step === 5) {
                this.isFinal = true;
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
        }
    },
    computed: {
        ...mapState(['selfDefinedRecs'])
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
                <Breadcrumb :home="breadcrumbHome" :model="breadcrumbItems" style="border-width: 0px" />
                <br />
                <!-- Step -->
                <Steps :model="nestedRouteItems" :readonly="false" />
                <br />
                <div class="grid">
                    <div class="col-10">
                        <h5>{{ this.pageTitle }}</h5>
                        <p>{{ this.pageDesc }}</p>
                    </div>
                    <div class="col-2">
                        <Button v-if="!this.isFinal" label=" 下一步" class="pi pi-arrow-right p-button-success" @click="next" v-tooltip="'請框好位置好點我'" style="width: 12em; height: 4em"></Button>
                        <Button v-else label=" 提交" class="pi pi-arrow-right p-button-secondary" @click="upload" v-tooltip="'請上確認後點擊'" style="width: 12em; height: 4em"></Button>
                    </div>
                </div>
                <router-view />
            </div>
        </div>
    </div>
    <div class="grid p-fluid">
        <div class="col-12 md:col-8">
            <Box :Boxes="this.Boxes" :isShapesVisible="this.isShapesVisible" />
        </div>
        <div class="col-12 md:col-4">
            <div class="card" style="overflow-x: scroll">
                <BoxCard :Boxes="this.Boxes" @toggleShowShapes="onSwitchChange" />
            </div>
        </div>
    </div>
</template>
