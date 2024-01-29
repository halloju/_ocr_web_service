<script>
import BaseOCR from '@/components/BaseOCR.vue';
import remittance from '@/assets/img/example/remittance.jpg';
import check_front from '@/assets/img/example/check_front.jpg';
import check_back from '@/assets/img/example/check_back.jpg';
import driver_license from '@/assets/img/example/driver_license.jpg';
import health_insurance from '@/assets/img/example/health_insurance.png';
import id from '@/assets/img/example/id.jpg';
import fs from '@/assets/img/example/fs.jpg';
import ws from '@/assets/img/example/ws.jpg';
import { OCR_ROOT } from '@/url';
import id_example from '@/assets/img/ocr_example/id_example.png';
import driver_example from '@/assets/img/ocr_example/driver_example.png';
import health_example from '@/assets/img/ocr_example/health_example.png';
import ws_example from '@/assets/img/ocr_example/ws_example.png';
import fs_example from '@/assets/img/ocr_example/fs_example.png';
import remittance_example from '@/assets/img/ocr_example/remittance_example.png';
import check_front_example from '@/assets/img/ocr_example/check_front_example.png';
import check_back_example from '@/assets/img/ocr_example/check_back_example.png';

export default {
    components: {
        BaseOCR
    },
    data() {
        return {
            title: '',
            subName: '',
            description: '',
            apiUrl: '',
            template_id: this.$store.state.template_id
        };
    },
    created() {
        const type = this.$route.params.type;
        const ocrConfig = this.getOcrConfig(type);
        this.key = ocrConfig.key;
        this.title = ocrConfig.title;
        this.apiUrl = ocrConfig.apiUrl;
        this.subName = ocrConfig.subName;
        this.description = ocrConfig.description;
        this.useModelComplexity = ocrConfig.useModelComplexity;
        this.useLanguage = ocrConfig.useLanguage;
        this.imageClass = ocrConfig.imageClass;
        this.defaultImgURL = ocrConfig.defaultImgURL;
        this.category = ocrConfig.category;
        this.explanation = ocrConfig.explanation;
        this.file = ocrConfig.file;
        this.hasTitle = ocrConfig.hasTitle;
    },
    watch: {
        $route(to, from) {
            const type = to.params.type;
            const ocrConfig = this.getOcrConfig(type);
            this.key = ocrConfig.key;
            this.title = ocrConfig.title;
            this.apiUrl = ocrConfig.apiUrl;
            this.subName = ocrConfig.subName;
            this.description = ocrConfig.description;
            this.useModelComplexity = ocrConfig.useModelComplexity;
            this.useLanguage = ocrConfig.useLanguage;
            this.imageClass = ocrConfig.imageClass;
            this.defaultImgURL = ocrConfig.defaultImgURL;
            this.category = ocrConfig.category;
            this.explanation = ocrConfig.explanation;
            this.file = ocrConfig.file;
            this.hasTitle = ocrConfig.hasTitle;
        }
    },
    methods: {
        getOcrConfig(type) {
            const ocrTypes = {
                general: {
                    key: 0,
                    title: '全文辨識',
                    subName: '全文辨識',
                    description: '請上傳一張或多張圖片，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: `${OCR_ROOT}/gp_ocr`,
                    useModelComplexity: true,
                    useLanguage: true,
                    defaultImgURL: '',
                    category: {
                        name: 'general',
                        limit: 50
                    },
                    explanation: '',
                    file: null,
                    hasTitle: false
                },
                template: {
                    key: 1,
                    title: '模板辨識',
                    subName: `模板編號：${this.template_id}`,
                    description: '請上傳一張或多張圖片，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: `${OCR_ROOT}/template_ocr`,
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: '',
                    category: {
                        name: 'general',
                        limit: 50
                    },
                    explanation: '',
                    file: null,
                    hasTitle: true
                },
                remittance: {
                    key: 2,
                    title: '票據辨識',
                    subName: '匯款單辨識',
                    description: '請上傳一張，下一步會進行辨識並可以進行檢視。',
                    apiUrl: `${OCR_ROOT}/remittance`,
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: remittance,
                    category: {
                        name: 'special',
                        limit: 1
                    },
                    explanation: '1.匯款序號 (remitno)<br/>2.匯款金額 (amount)<br/>3.收款帳號 (receiveacc)<br/>4.收款行帳號 (receivebank)<br/>5.匯款人 ID (remitterid)<br/>6.是否有附言 (remark)<br/>7.代理人 ID (agentid)',
                    file: remittance_example,
                    hasTitle: true
                },
                check_front: {
                    key: 3,
                    title: '票據辨識',
                    subName: '支票正面辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: `${OCR_ROOT}/check_front`,
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: check_front,
                    category: {
                        name: 'special',
                        limit: 1
                    },
                    explanation: '1.支票金額 (amount)<br/>2.支票到期日 (due_date)',
                    file: check_front_example,
                    hasTitle: true
                },
                check_back: {
                    key: 4,
                    title: '票據辨識',
                    subName: '支票背面辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: `${OCR_ROOT}/check_back`,
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: check_back,
                    category: {
                        name: 'special',
                        limit: 1
                    },
                    explanation: '帳號 (account)',
                    file: check_back_example,
                    hasTitle: true
                },
                id: {
                    key: 5,
                    title: '人證辨識',
                    subName: '身分證辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: `${OCR_ROOT}/cv-ocr`,
                    imageClass: 'ID',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: id,
                    category: {
                        name: 'special',
                        limit: 1
                    },
                    explanation: '1.姓名 (name)<br/>2.出生年月日 (date_of_birth)<br/>3.發證日期 (date_of_issue)<br/>4.發證地點 (place_of_issue)<br/>5.發證類別 (type_of_issue)<br/>6.性別 (sex)<br/>7.統一編號 (id_no)',
                    file: id_example,
                    hasTitle: true
                },
                driver_license: {
                    key: 6,
                    title: '人證辨識',
                    subName: '駕照辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: `${OCR_ROOT}/cv-ocr`,
                    imageClass: 'DRIVER_LICENSE',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: driver_license,
                    category: {
                        name: 'special',
                        limit: 1
                    },
                    explanation: '1.駕照號碼 (id_no)<br/>2.姓名 (name)<br/>3.出生日期 (date_of_birth)',
                    file: driver_example,
                    hasTitle: true
                },
                health_insurance: {
                    key: 7,
                    title: '人證辨識',
                    subName: '健保卡辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: `${OCR_ROOT}/cv-ocr`,
                    imageClass: 'HEALTH_INSURANCE',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: health_insurance,
                    category: {
                        name: 'special',
                        limit: 1
                    },
                    explanation: '1.姓名 (name)<br/>2.身分證字號 (id_no)<br/>3.出生年月日 (date_of_birth)',
                    file: health_example,
                    hasTitle: true
                },
                withholding: {
                    key: 8,
                    title: '財證辨識',
                    subName: '扣繳憑單辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: `${OCR_ROOT}/cv-ocr`,
                    imageClass: 'WITHHOLDING_STATEMENT',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: ws,
                    category: {
                        name: 'special',
                        limit: 1
                    },
                    explanation: '1.扣繳單位統一編號 (company)<br/>2.所得人統一編號 (id)<br/>3.所得所屬起始年月 (start_date)<br/>4.所得所屬結束年月 (end_date)<br/>5.所得給付年度 (year)<br/>6.給付總額 (income)',
                    file: ws_example,
                    hasTitle: true
                },
                financial_statement: {
                    key: 9,
                    title: '財證辨識',
                    subName: '國稅局個人所得清單辨識',
                    description: '請上傳一張，下一步會進行全部辨識並可以進行檢視。',
                    apiUrl: `${OCR_ROOT}/cv-ocr`,
                    imageClass: 'NTB_FINANCIAL_STATEMENT',
                    useModelComplexity: false,
                    useLanguage: false,
                    defaultImgURL: fs,
                    category: {
                        name: 'special',
                        limit: 1
                    },
                    explanation: '1.財政年度 (year)<br/>2.清單種類 (title)<br/>3.顧客統一編號 (idValue)<br/>4.所得類別 (incomeType)<br/>5.公司統一編號 (company)<br/>6.所得額合計 (incomeValue)',
                    file: fs_example,
                    hasTitle: true
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
        <BaseOCR
            :apiUrl="apiUrl"
            :category="category"
            :title="title"
            :subName="subName"
            :description="description"
            :useModelComplexity="useModelComplexity"
            :useLanguage="useLanguage"
            :imageClass="imageClass"
            :defaultImgURL="defaultImgURL"
            :explanation="explanation"
            :file="file"
            :hasTitle="hasTitle"
            :key="key"
        />
    </div>
</template>
