<script>
import Box from '@/components/Box.vue';
import BoxCard from '@/components/BoxCard.vue';

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
            switchValue: false
        };
    },
    methods: {
        next() {
            const nextStep = this.step + 1;
            this.$router.push({ path: `/features/self-define/step/${nextStep}` });
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
                        <Button label=" 下一步" class="pi pi-arrow-right p-button-success" @click="next" v-tooltip="'請框好位置好點我'" style="width: 12em; height: 4em"></Button>
                        <!-- <Button v-else label=" 下一步" class="pi pi-arrow-right p-button-secondary" @click="next" v-tooltip="'請上傳圖片後點擊'" style="width: 12em; height: 4em;" :disabled="true"></Button> -->
                    </div>
                </div>
                <router-view />
            </div>
        </div>
    </div>
    <div class="grid p-fluid">
        <div class="col-12 md:col-8">
            <div class="card">
                <Box :Boxes="this.Boxes" />
            </div>
        </div>
        <div class="col-12 md:col-4">
            <div class="card">
                <BoxCard :Boxes="this.Boxes" />
            </div>
        </div>
    </div>
</template>
