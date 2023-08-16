<script setup>
import { ref } from 'vue';
const model = ref([
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
            }
]);

const selectedMainItem = ref(null);
const selectedSubItem = ref(null);

function toggleMainSelect(label){
    if (selectedMainItem.value === label) {
        selectedMainItem.value = null; // Deselect if the same item is clicked again
    } else {
        selectedMainItem.value = label;
    }
    selectedSubItem.value = null;
};

function toggleSubSelect(label){
    if (selectedSubItem.value === label) {
    selectedSubItem.value = null; // Deselect if the same subitem is clicked again
    } else {
    selectedSubItem.value = label;
    }
};
</script>

<template>
<div id="sideMenuContainer">
    <ul class="sideMainMenu">
    <li v-for="mainItem in model" 
        :key="mainItem.label" 
        :class="{ 'withSubMenu': true, 'select': selectedMainItem === mainItem.label }" 
        @click="toggleMainSelect(mainItem.label)">
        {{ mainItem.label }}
        <ul v-if="mainItem.items && mainItem.items.length" class="sideSubMenu">
        <li v-for="subItem in mainItem.items" 
            :key="subItem.label" 
            :class="{ 'select': selectedSubItem === subItem.label }" 
            @click.stop="toggleSubSelect(subItem.label)">
            <router-link :to="subItem.to">{{ subItem.label }}</router-link>
        </li>
        </ul>
    </li>
    </ul>
</div>
</template>
    

<style lang="scss" scoped></style>
