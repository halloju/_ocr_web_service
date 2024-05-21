<script>
import BaseUploadImage from '@/components/BaseUploadImage.vue';
import BaseOcrResultShow from '@/components/BaseOcrResultShow.vue';
import BaseOcrResultShowGeneral from '@/components/BaseOcrResultShowGeneral.vue';


export default {
    components: {
        BaseUploadImage,
        BaseOcrResultShow,
        BaseOcrResultShowGeneral
    },
    name: 'BaseOCR',
    props: {
        title: String,
        subName: String,
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
    data(props) {
        return {
            step: 1,
            selectedModel: ['tchinese', 'english', 'number', 'symbol'],
            imageUploadKey: 0,
            languages: [
                {
                    value: 'tchinese',
                    label: '繁體中文'
                },
                {
                    value: 'english',
                    label: '英文'
                },
                {
                    value: 'number',
                    label: '數字'
                },
                {
                    value: 'symbol',
                    label: '符號'
                }
            ],
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
            breadcrumbItems: [{ path: '/', label: '首頁' }, { label: this.title }, { label: this.subName, isCurrent: true }],
            detail_description: props.description
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
    <div class="layoutZoneContainer">
        <!-- Title -->
        <div v-if="step == 1" style="margin-bottom: 20px;">
            <p class="title">{{ subName }}</p>
            <div style="display: flex; align-items: center">
                <p v-if="useLanguage" style="margin-right: 2px; color: red">*</p>
                <div v-if="useLanguage" style="display: flex; align-items: center; margin-right: 20px">
                    <p style="margin-right: 10px; margin-bottom: 0px">選擇語言與類型：</p>
                    <div>
                        <el-select multiple v-model="selectedModel" collapse-tags collapse-tags-tooltip>
                            <el-option v-for="item in languages" :key="item.value" :label="item.label" :value="item.value" style="font-size: 16px;"></el-option>
                        </el-select>
                    </div>
                </div>
            </div>
        </div>

        <BaseUploadImage
            v-if="step == 1"
            @nextStepEmit="nextStep"
            @uploadConfig="$emit('update-upload-config', $event)"
            :apiUrl="apiUrl"
            :category="category"
            :selectedModel="selectedModel"
            :useLanguage="useLanguage"
            :key="imageUploadKey"
            :imageClass="imageClass"
            :defaultImgURL="defaultImgURL"
            :description="detail_description"
        />
        <BaseOcrResultShow v-else-if="step == 2 && title !== '全文辨識'" @nextStepEmit="nextStep" :hasTitle="hasTitle" />
        <BaseOcrResultShowGeneral v-else-if="step == 2 && title === '全文辨識'" @nextStepEmit="nextStep" :hasTitle="hasTitle" />
        </div>
</template>
