<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: '主要功能',
        items: [
            {
                label: '通用辨識',
                icon: 'pi pi-th-large',
                items: [
                    {
                        label: '全文辨識',
                        icon: 'pi pi-th-large',
                        to: '/features/ocr/general'
                    },
                    {
                        label: '模板辨識',
                        icon: 'pi pi-list',
                        to: '/features/general/model-list'
                    }
                ]
            },
            {
                label: '票據辨識',
                icon: 'pi pi-th-large',
                items: [
                    {
                        label: '匯款單辨識',
                        icon: 'pi pi-th-large',
                        to: '/features/ocr/remittance'
                    },
                    {
                        label: '支票正面辨識',
                        icon: 'pi pi-list',
                        to: '/features/ocr/check_front'
                    },
                    {
                        label: '支票背面辨識',
                        icon: 'pi pi-list',
                        to: '/features/ocr/check_back'
                },
                ]
            },
            {
                label: '人證辨識',
                icon: 'pi pi-users',
                items: [
                    {
                        label: '身份證辨識',
                        icon: 'pi pi-id-card',
                        to: '/features/ocr/id'
                    },
                    {
                        label: '駕照辨識',
                        icon: 'pi pi-car',
                        to: '/features/ocr/driver_license'
                    },
                    {
                        label: '健保卡辨識',
                        icon: 'pi pi-credit-card',
                        to: '/features/ocr/health_insurance'
                    }
                ]
            },
            {
                label: '財證辨識',
                icon: 'pi pi-dollar',
                items: [
                    {
                        label: '所得清單辨識',
                        icon: 'pi pi-id-card',
                        to: '/features/ocr/financial_statement'
                    },
                    {
                        label: '扣繳憑單辨識',
                        icon: 'pi pi-envelope',
                        to: '/features/ocr/withholding'
                    }
                ]
            },
            {
                label: '檔案轉換',
                icon: 'pi pi-file',
                items: [
                    {
                        label: 'PDF to Image',
                        icon: 'pi pi-images',
                        to: '/features/pdf2image'
                    }
                ]
            }
        ]
    }
]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>
