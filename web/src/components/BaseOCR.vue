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
        useModelComplexity: Boolean,
        useLanguage: Boolean,
        imageClass: String,
        defaultImgURL: Object,
        explanation: String,
        file: Object
    },
    methods: {
        nextStep(step) {
            this.step = step;
        },
        reset() {
            this.imageUploadKey += 1;
            this.step = 1;
        }
    },
    data() {
        return {
            step: 1,
            imageComplexity: 'medium',
            selectedModel: 'dbnet_v0+cht_ppocr_v1',
            imageUploadKey: 0,
            languages: [
                { value: 'dbnet_v0+cht_ppocr_v1', text: '繁體中文 + 英數字' },
                { value: 'dbnet_v0+en_ppocr_v0', text: '英數字' }
            ],
            selectType: 'basic',
            placeholder: '繁體中文 + 英數字',
            type: 'switch',
            highPrecision: [
                {
                    value: 'high', text: '是'
                },
                {
                    value: 'medium', text: '否'
                }
            ],
            switchValue: false
        };
    },
    watch: {
        $route: {
            handler() {
                this.reset();
            },
            immediate: true,
        },
        switchValue(newVal) {
            if (newVal==='true') {
                this.imageComplexity = 'high';
            } else {
                
                this.imageComplexity = 'medium';
            }
        }
    }
};
</script>

<template>
    <div class="layoutZoneContainer">
        <div class="breadcrumbContainer">
            <ul><li :to="{ path: '/' }">首頁</li>
                <li>{{ title }}</li>
                <li class="now" >{{ subtitle }}</li>
            </ul>    
        </div>
                <!-- Title -->
        <div v-if="step == 1" style="margin-bottom: 20px; margin-top: 20px;">
            <h1>{{ subtitle }}</h1>
            <div style="display: flex; align-items: center;" >
                <p v-if="useLanguage" style="margin-right: 2px; color: red;">*</p>
                <div v-if="useLanguage" style="display: flex; align-items: center; margin-right: 20px;" >
                    <h4 style="margin-right: 10px;">選擇語言：</h4>
                    <esb-select :selectType="selectType" :options="languages" :placeholder="placeholder" v-model="selectedModel" />
                </div>
                <div v-if="useModelComplexity" style="display: flex; align-items: center;">
                    <h4 style="margin-right: 10px;">使用高精準度模型：</h4>
                    <esb-radio :type="type" :options="highPrecision" v-model="switchValue"/>
                </div>
                <p v-if="useModelComplexity" style="margin-left: 10px; color: red;">*注意，當您使用高精準度模型時會耗時較久</p>
            </div>
        
        </div>
    
    <BaseUploadImage v-if="step == 1" @nextStepEmit="nextStep" @uploadConfig="$emit('update-upload-config', $event)" :apiUrl="apiUrl" :category="category" :selectedModel="selectedModel" :imageComplexity="imageComplexity" :useLanguage="useLanguage" :key="imageUploadKey" :imageClass="imageClass" :defaultImgURL="defaultImgURL"/>
    <BaseOcrResultShow v-else-if="step == 2" @nextStepEmit="nextStep" />
</div>
</template>
