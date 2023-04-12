<script>
import BaseUploadImage from '@/components/BaseUploadImage.vue';
import BaseOcrResultShow from '@/components/BaseOcrResultShow.vue';

export default {
    components: {
        BaseUploadImage,
        BaseOcrResultShow
    },
    name: 'RemittanceOCR',
    data() {
        return {
            step: 1,
            image_complexity: '',
            selectedLang: '',
            category: {
                name: 'limited',
                limit: 1
            }
        };
    },
    watch: {},
    computed: {},
    methods: {
        nextStep(step) {
            this.step = step;
        },
        getUploadConfig(image_complexity, selectedLang) {
            this.image_complexity = image_complexity;
            this.selectedLang = selectedLang;
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
                    <el-breadcrumb-item>票據辨識</el-breadcrumb-item>
                </el-breadcrumb>
                <br />
                <!-- Step -->
                <el-steps :active="step" align-center>
                    <el-step title="Step 1" description="圖檔上傳" />
                    <el-step title="Step 2" description="辨識結果" />
                </el-steps>
                <h5>匯款單辨識</h5>
                <p>請上傳一張，下一步會進行辨識並可以進行檢視。</p>
            </div>
        </div>
    </div>
    <BaseUploadImage v-if="step == 1" @nextStepEmit="nextStep" @uploadConfig="getUploadConfig" apiUrl="/remittance_ocr/remittance" :category="category" />
    <BaseOcrResultShow v-else-if="step == 2" @nextStepEmit="nextStep" baseUrl="remittance_ocr" />
</template>
