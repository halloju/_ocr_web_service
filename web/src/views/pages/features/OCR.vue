<script>
import BaseOCR from '@/components/BaseOCR.vue';

export default {
    components: {
        BaseOCR
    },
    data() {
        return {
            category: {
                name: 'limited',
                limit: 1
            },
            title: '',
            subtitle: '',
            description: '',
            apiUrl: '',
            baseUrl: '',
            template_id: this.$store.state.template_id
        };
    },
    created() {
        const type = this.$route.params.type;
        const ocrConfig = this.getOcrConfig(type);

        this.title = ocrConfig.title;
        this.apiUrl = ocrConfig.apiUrl;
        this.baseUrl = ocrConfig.baseUrl;
        this.subtitle = ocrConfig.subtitle;
        this.description = ocrConfig.description;
    },
    watch: {
        $route(to, from) {
            const type = to.params.type;
            const ocrConfig = this.getOcrConfig(type);

            this.title = ocrConfig.title;
            this.apiUrl = ocrConfig.apiUrl;
            this.baseUrl = ocrConfig.baseUrl;
            this.subtitle = ocrConfig.subtitle;
            this.description = ocrConfig.description;
        }
    },
    methods: {
        getOcrConfig(type) {
            const ocrTypes = {
                general: {
                    title: '全文辨識',
                    subtitle: '通用辨識',
                    description: '請上傳一張或多張圖片，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/gp_ocr/predict_images',
                    baseUrl: 'gp_ocr'
                },
                template: {
                    title: '模板辨識',
                    subtitle: `模板編號：${this.template_id}`,
                    description: '請上傳一張或多張圖片，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/template_ocr/predict_images',
                    baseUrl: 'template_ocr'
                },
                remittance: {
                    title: '票據辨識',
                    subtitle: '匯款單辨識',
                    description: '請上傳一張，下一步會進行辨識並可以進行檢視。',
                    apiUrl: '/remittance_ocr/remittance',
                    baseUrl: 'remittance_ocr'
                },
                check_front: {
                    title: '票據辨識',
                    subtitle: '支票正面辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/check_front_ocr/check_front',
                    baseUrl: 'check_front_ocr'
                },
                check_back: {
                    title: '票據辨識',
                    subtitle: '支票背面辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/check_back_ocr/check_back',
                    baseUrl: 'check_back_ocr'
                }
                // Add more OCR types here
            };
            return ocrTypes[type] || {}; // Return an empty object if the type is not found
        }
    }
};
</script>

<template>
    <div>
        <BaseOCR :apiUrl="apiUrl" :category="category" :baseUrl="baseUrl" :title="title" :subtitle="subtitle" :description="description" />
    </div>
</template>
