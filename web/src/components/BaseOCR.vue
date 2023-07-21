<script>
import BaseUploadImage from '@/components/BaseUploadImage.vue';
import BaseOcrResultShow from '@/components/BaseOcrResultShow.vue';

import id_example from '@/assets/img/ocr_example/id.png';
import driver_example from '@/assets/img/ocr_example/driver.png';
import health_example from '@/assets/img/ocr_example/health.png';
import ws_example from '@/assets/img/ocr_example/ws.png';
import fs_example from '@/assets/img/ocr_example/fs.png';
import remittance_example from '@/assets/img/ocr_example/remittance.png';
import check_front_example from '@/assets/img/ocr_example/check_front.png';
import check_back_example from '@/assets/img/ocr_example/check_back.png';

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
        useModelComplexity: Boolean,
        useLanguage: Boolean,
        imageClass: String,
        defaultImgURL: Object,
        explanation: String,
        idx: {
            type: Number,
            default: null
        }
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
            imageUploadKey: 0,
            file_url: [id_example, driver_example, health_example, ws_example, fs_example, check_front_example, check_back_example, remittance_example]
        };
    },
    watch: {
        $route: {
            handler() {
                this.reset();
            },
            immediate: true,
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
                <img v-if="idx != null && !isNaN(idx)" :src="file_url[idx]" :style="{ width: '300px' }"/>
                <p v-html="explanation"></p>
                <h5>{{ subtitle }}</h5>
                <p>{{ description }}</p>
            </div>
        </div>
    </div>
    <BaseUploadImage v-if="step == 1" @nextStepEmit="nextStep" @uploadConfig="$emit('update-upload-config', $event)" :apiUrl="apiUrl" :category="category" :useModelComplexity="useModelComplexity" :useLanguage="useLanguage" :key="imageUploadKey" :imageClass="imageClass" :defaultImgURL="defaultImgURL"/>
    <BaseOcrResultShow v-else-if="step == 2" @nextStepEmit="nextStep" />
</template>
