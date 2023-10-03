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
        file: Object,
        hasTitle: Boolean
    },
    methods: {
        nextStep(step) {
            this.step = step;
        },
        reset() {
            this.imageUploadKey += 1;
            this.step = 1;
        },
        toggleSwitch() {
            this.switchValue = !this.switchValue;
        }
    },
    data() {
        return {
            step: 1,
            imageComplexity: 'medium',
            selectedModel: ['tchinese', 'english', 'number', 'symbol'],
            imageUploadKey: 0,
            languages: [{ value: ['tchinese', 'english', 'number', 'symbol'], text: '繁體中文 + 英數字' }],
            selectType: 'basic',
            placeholder: '繁體中文 + 英數字',
            type: 'switch',
            highPrecision: [
                {
                    value: 'high',
                    text: '是'
                },
                {
                    value: 'medium',
                    text: '否'
                }
            ],
            switchValue: false,
            breadcrumbItems: [{ path: '/', label: '首頁' }, { label: this.title }, { label: this.subtitle, isCurrent: true }]
        };
    },
    watch: {
        $route: {
            handler() {
                this.reset();
            },
            immediate: true
        },
        switchValue(newVal) {
            if (newVal) {
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

        <!-- Title -->
        <div v-if="step == 1" style="margin-bottom: 20px;">
            <p class="title">{{ subtitle }}</p>
            <div style="display: flex; align-items: center">
                <p v-if="useLanguage" style="margin-right: 2px; color: red">*</p>
                <div v-if="useLanguage" style="display: flex; align-items: center; margin-right: 20px">
                    <p style="margin-right: 10px; margin-bottom: 0px">選擇語言：</p>
                    <div>
                        <select class="selectField dropdownBtn" v-model="selectedModel">
                            <option v-for="option in languages" :value="option.value" style="font-size: 16px;">&nbsp;&nbsp;{{ option.text }}</option>
                        </select>
                    </div>
                </div>
                <div v-if="useModelComplexity" style="display: flex; align-items: center">
                    <p style="margin-right: 10px; margin-bottom: 0px">使用高精準度模型：</p>
                    <div class="switchField">
                        <label class="switch">
                            <input type="checkbox" id="switch" v-model="switchValue" />
                            <span class="slider round"></span>
                        </label>
                    </div>
                </div>
                <p v-if="useModelComplexity" style="margin-left: 10px; color: red">*注意，當您使用高精準度模型時會耗時較久</p>
            </div>
        </div>

        <BaseUploadImage
            v-if="step == 1"
            @nextStepEmit="nextStep"
            @uploadConfig="$emit('update-upload-config', $event)"
            :apiUrl="apiUrl"
            :category="category"
            :selectedModel="selectedModel"
            :imageComplexity="imageComplexity"
            :useLanguage="useLanguage"
            :key="imageUploadKey"
            :imageClass="imageClass"
            :defaultImgURL="defaultImgURL"
        />
        <BaseOcrResultShow v-else-if="step == 2" @nextStepEmit="nextStep" :hasTitle="hasTitle" />
    </div>
</template>
