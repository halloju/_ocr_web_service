<script>
import Step1 from '@/components/general/step1.vue';
import Step2 from '@/components/general/step2.vue';

export default {
    components: {
        Step1,
        Step2
    },
    name: 'GeneralOCR',
    data() {
        return {
            step: 1,
            image_complexity: '',
            selectedLang: ''
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
                    <el-breadcrumb-item>全文辨識</el-breadcrumb-item>
                </el-breadcrumb>
                <br />
                <!-- Step -->
                <el-steps :active="step" align-center>
                    <el-step title="Step 1" description="圖檔上傳" />
                    <el-step title="Step 2" description="辨識結果" />
                </el-steps>
                <h5>通用辨識</h5>
                <p>請上傳一張或多張圖片，下一步會進行全部辨識並可以進行檢視。</p>
            </div>
        </div>
    </div>
    <Step1 v-if="step == 1" @nextStepEmit="nextStep" @uploadConfig="getUploadConfig" />
    <Step2 v-else-if="step == 2" @nextStepEmit="nextStep" />
</template>
