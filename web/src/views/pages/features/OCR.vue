<script>
import BaseOCR from '@/components/BaseOCR.vue';

export default {
    components: {
        BaseOCR
    },
    data() {
        return {
            category: {
                name: 'general',
                limit: 20
            },
            title: '',
            subtitle: '',
            description: '',
            apiUrl: '',
            template_id: this.$store.state.template_id
        };
    },
    created() {
        const type = this.$route.params.type;
        const ocrConfig = this.getOcrConfig(type);

        this.title = ocrConfig.title;
        this.apiUrl = ocrConfig.apiUrl;
        this.subtitle = ocrConfig.subtitle;
        this.description = ocrConfig.description;
        this.useModelComplexity = ocrConfig.useModelComplexity;
    },
    watch: {
        $route(to, from) {
            const type = to.params.type;
            const ocrConfig = this.getOcrConfig(type);

            this.title = ocrConfig.title;
            this.apiUrl = ocrConfig.apiUrl;
            this.subtitle = ocrConfig.subtitle;
            this.description = ocrConfig.description;
            this.useModelComplexity = ocrConfig.useModelComplexity;
        }
    },
    methods: {
        getOcrConfig(type) {
            const ocrTypes = {
                general: {
                    title: '全文辨識',
                    subtitle: '通用辨識',
                    description: '請上傳一張或多張圖片，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/gp_ocr',
                    useModelComplexity: true
                },
                template: {
                    title: '模板辨識',
                    subtitle: `模板編號：${this.template_id}`,
                    description: '請上傳一張或多張圖片，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/template_ocr',
                    useModelComplexity: false
                },
                remittance: {
                    title: '票據辨識',
                    subtitle: '匯款單辨識',
                    description: '請上傳一張，下一步會進行辨識並可以進行檢視。',
                    apiUrl: '/remittance_ocr/remittance',
                    useModelComplexity: false
                },
                check_front: {
                    title: '票據辨識',
                    subtitle: '支票正面辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/check_front',
                    useModelComplexity: false
                },
                check_back: {
                    title: '票據辨識',
                    subtitle: '支票背面辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/check_back',
                    useModelComplexity: false
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
        <BaseOCR :apiUrl="apiUrl" :category="category" :title="title" :subtitle="subtitle" :description="description" :useModelComplexity="useModelComplexity" />
    </div>
</template>
