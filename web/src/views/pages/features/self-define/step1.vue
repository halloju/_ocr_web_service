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
            switchValue: false
        };
    },
    methods: {
        next() {
            this.$router.push({ path: '/features/general/self-define/step/2' });
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
                <el-breadcrumb>
                    <el-breadcrumb-item :to="{ path: '/' }">首頁</el-breadcrumb-item>
                    <el-breadcrumb-item :to="{ name: 'Model-List' }">模板辨識</el-breadcrumb-item>
                    <el-breadcrumb-item>新增模板</el-breadcrumb-item>
                </el-breadcrumb>
                <br />
                <!-- Step -->
                <Steps :model="nestedRouteItems" :readonly="true" />
                <br />
                <div class="grid">
                    <div class="col-12">
                        <h5>新增自定義模板</h5>
                        <p>上傳一張清晰的圖片進行標注，並於後續步驟框選標註需辨識的區域位於哪一個區域。</p>
                    </div>
                    <div class="col-12">
                        <el-button v-if="isOK" type="success" @click="next" v-tooltip="'請上傳好圖片後點我'">下一步</el-button>
                        <el-button v-else type="success" disabled>下一步</el-button>
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
