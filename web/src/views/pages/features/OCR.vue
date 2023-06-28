<script>
import BaseOCR from '@/components/BaseOCR.vue';

export default {
    components: {
        BaseOCR
    },
    data() {
        return {
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
        this.useLanguage = ocrConfig.useLanguage;
        this.imageClass = ocrConfig.imageClass;
        this.defaultImgURL = ocrConfig.defaultImgURL;
        this.category = ocrConfig.category;
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
            this.useLanguage = ocrConfig.useLanguage;
            this.imageClass = ocrConfig.imageClass;
            this.defaultImgURL = ocrConfig.defaultImgURL;
            this.category = ocrConfig.category;
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
                    useModelComplexity: true,
                    useLanguage: true,
                    defaultImgURL: '',
                    category: {
                        name: 'general',
                        limit: 20
                    }
                },
                template: {
                    title: '模板辨識',
                    subtitle: `模板編號：${this.template_id}`,
                    description: '請上傳一張或多張圖片，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/template_ocr',
                    useModelComplexity: false,
                    useLanguage: true,
                    defaultImgURL: '',
                    category: {
                        name: 'general',
                        limit: 20
                    }
                },
                remittance: {
                    title: '票據辨識',
                    subtitle: '匯款單辨識',
                    description: '請上傳一張，下一步會進行辨識並可以進行檢視。',
                    apiUrl: '/ocr/remittance',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: 'src/assets/img/example/remittance.jpg',
                    category: {
                        name: 'special',
                        limit: 1
                    }
                },
                check_front: {
                    title: '票據辨識',
                    subtitle: '支票正面辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/check_front',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: 'src/assets/img/example/check_front.jpg',
                    category: {
                        name: 'special',
                        limit: 1
                    }
                },
                check_back: {
                    title: '票據辨識',
                    subtitle: '支票背面辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/check_back',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: 'src/assets/img/example/check_back.jpg',
                    category: {
                        name: 'special',
                        limit: 1
                    }
                },
                id: {
                    title: '人證辨識',
                    subtitle: '身分證辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/cv-ocr',
                    imageClass: 'ID',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: 'src/assets/img/example/id.jpg',
                    category: {
                        name: 'special',
                        limit: 1
                    }
                },
                driver_license: {
                    title: '人證辨識',
                    subtitle: '駕照辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/cv-ocr',
                    imageClass: 'DRIVER_LICENSE',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: 'src/assets/img/example/driver_license.jpg',
                    category: {
                        name: 'special',
                        limit: 1
                    }
                },
                health_insurance: {
                    title: '人證辨識',
                    subtitle: '健保卡辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/cv-ocr',
                    imageClass: 'HEALTH_INSURANCE',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: 'src/assets/img/example/health_insurance.jpg',
                    category: {
                        name: 'special',
                        limit: 1
                    }
                },
                withholding: {
                    title: '財證辨識',
                    subtitle: '扣繳憑單辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/cv-ocr',
                    imageClass: 'WITHHOLDING_STATEMENT',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: 'src/assets/img/example/ws.jpg',
                    category: {
                        name: 'special',
                        limit: 1
                    }
                },
                financial_statement: {
                    title: '財證辨識',
                    subtitle: '國稅局個人所得清單辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: '/ocr/cv-ocr',
                    imageClass: 'NTB_FINANCIAL_STATEMENT',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: 'src/assets/img/example/fs.jpg',
                    category: {
                        name: 'special',
                        limit: 1
                    }
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
        <BaseOCR :apiUrl="apiUrl" :category="category" :title="title" :subtitle="subtitle" :description="description" :useModelComplexity="useModelComplexity" :useLanguage="useLanguage" :imageClass="imageClass" :defaultImgURL="defaultImgURL" />
    </div>
</template>
