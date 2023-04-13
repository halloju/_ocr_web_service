<script>
import BaseUploadImage from '@/components/BaseUploadImage.vue';
import BaseOcrResultShow from '@/components/BaseOcrResultShow.vue';

export default {
    components: {
        BaseUploadImage,
        BaseOcrResultShow
    },
    name: 'BaseOCR',
    props: {
        title: String,
        subtitle: String,
        description: String,
        apiUrl: String,
        category: Object,
        baseUrl: String
    },
    methods: {
        nextStep(step) {
            this.step = step;
        },
        updateUploadConfig({ image_complexity, selectedLang }) {
            this.image_complexity = image_complexity;
            this.selectedLang = selectedLang;
        },
        reset() {
            this.imageUploadKey += 1;
            this.step = 1;
        }
    },
    data() {
        return {
            step: 1,
            image_complexity: '',
            selectedLang: '',
            imageUploadKey: 0
        };
    },
    watch: {
        $route: {
            handler() {
                this.reset();
            },
            immediate: true
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
                    <el-breadcrumb-item>{{ title }}</el-breadcrumb-item>
                </el-breadcrumb>
                <br />
                <!-- Step -->
                <el-steps :active="step" align-center>
                    <el-step title="Step 1" description="圖檔上傳" />
                    <el-step title="Step 2" description="辨識結果" />
                </el-steps>
                <h5>{{ subtitle }}</h5>
                <p>{{ description }}</p>
            </div>
        </div>
    </div>
    <BaseUploadImage v-if="step == 1" @nextStepEmit="nextStep" @uploadConfig="$emit('update-upload-config', $event)" :apiUrl="apiUrl" :category="category" :key="imageUploadKey" />
    <BaseOcrResultShow v-else-if="step == 2" @nextStepEmit="nextStep" :baseUrl="baseUrl" />
</template>
