<script>
import Box from '@/components/Box.vue';
import BoxCard from '@/components/BoxCard.vue';

export default {
    components: {
        BoxCard,
        Box
    },
    name: 'SelfDefine2',
    data() {
        return {
            nestedRouteItems: [
                {
                    label: '模板圖檔上傳',
                    to: '/features/self-define/step1'
                },
                {
                    label: '文字位置標註',
                    to: '/features/self-define/step2'
                },
                {
                    label: '方塊位置標註',
                    to: '/features/self-define/step3'
                },
                {
                    label: '遮罩位置標註',
                    to: '/features/self-define/step4'
                },
                {
                    label: '確認',
                    to: '/features/self-define/step5'
                }
            ],
            breadcrumbHome: { icon: 'pi pi-home', to: '/' },
            breadcrumbItems: [
                { label: '主要功能', to: '#' },
                { label: '自定義模板', to: '#' },
                { label: '新增自定義模板', to: '#' },
                { label: '模板圖檔上傳', to: '#' }
            ],
            switchValue: false,
            boxName: 'recs_text',
            boxTitle: '文字辨識位置',
            fillColor: {
                r: 0,
                g: 255,
                b: 0,
                a: 0.5
            }
        };
    },
    methods: {
        next() {
            this.$router.push({ path: '/features/self-define/step3' });
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
                        <h5>文字位置標註</h5>
                        <p>框選文字辨識位置，並編輯區域要項名稱，按下確認後即會出現在右邊欄位中。</p>
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
                <Box :boxName="boxName" :fillColor="fillColor" />
            </div>
        </div>
        <div class="col-12 md:col-4">
            <div class="card">
                <BoxCard :boxName="boxName" :boxTitle="boxTitle" />
            </div>
        </div>
    </div>
</template>
