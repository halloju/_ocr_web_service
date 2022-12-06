<script>
import UploadImage from '@/components/UploadImage.vue';

export default {
    components: {
        UploadImage
    },
    name: 'SelfDefine1',
    data() {
        return {
            isOK: false,
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
            switchValue: false
        };
    },
    methods: {
        next() {
            this.$router.push({ path: '/features/self-define/step2' });
        },
        getFiles(val) {
            this.myFiles = val;
        },
        Upload(val) {
            this.isOK = val;
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
                <Steps :model="nestedRouteItems" :readonly="true" />
                <br />
                <div class="grid">
                    <div class="col-8">
                        <h5>新增自定義模板</h5>
                        <p>上傳一張清晰的圖片進行標注，並於後續步驟框選標註需辨識的區域位於哪一個區域。</p>
                    </div>
                    <div class="col-2">
                        <FileUpload mode="basic" name="demo[]" url="./upload" :auto="true" chooseLabel="匯入設定檔" style="width: 12em; height: 4em" />
                    </div>
                    <div class="col-2">
                        <Button v-if="isOK" label=" 下一步" class="pi pi-arrow-right p-button-success" @click="next" v-tooltip="'請上傳圖片後點擊'" style="width: 12em; height: 4em"></Button>
                        <Button v-else label=" 下一步" class="pi pi-arrow-right p-button-secondary" @click="next" v-tooltip="'請上傳圖片後點擊'" style="width: 12em; height: 4em" :disabled="true"></Button>
                    </div>
                </div>
                <router-view />
            </div>
        </div>
    </div>

    <div class="grid p-fluid">
        <div class="col-12">
            <div class="card">
                <UploadImage :isUploaded="true" @updateStatus="Upload" />
            </div>
        </div>
    </div>
</template>
