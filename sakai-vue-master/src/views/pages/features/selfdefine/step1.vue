<script setup>
import { ref } from 'vue';

const menu = ref(null);
const contextMenu = ref(null);
const switchValue = ref(false);
const breadcrumbHome = ref({ icon: 'pi pi-home', to: '/' });
const breadcrumbItems = ref([{ label: '主要功能', to: '#' }, { label: '通用文件辨識', to: '#' }, { label: '通用辨識', to: '#' }]);
const nestedRouteItems = ref([
    {
        label: '圖檔上傳',
        to: '#'
    },
    {
        label: '單張結果確認',
        to: '#'
    },
]);

</script>

<template>
    <div class="grid p-fluid">
        <!-- Breadcrumb -->
        <div class="col-12">
            <Breadcrumb :home="breadcrumbHome" :model="breadcrumbItems" />
            
        </div>
        <!-- Step -->
        <div class="col-12">
            <div class="card card-w-title">
                <h5>辨識流程</h5>
                <p>依照以下流程就可以輕鬆取得辨識結果！</p>
                <Steps :model="nestedRouteItems" :readonly="false" />
                <router-view />
            </div>
        </div>
    </div>
    
    <div class="grid p-fluid">
        <div class="col-12 md:col-9">
            <div class="card">
                <FileUpload name="demo[]" url="./upload" :maxFileSize="1000000" :fileLimit="3" :previewWidth="500" />
            </div>

        </div>

        <div class="col-12 md:col-3">
            <div class="card">

                <h5>選擇語言</h5>
                <Dropdown v-model="dropdownValue" :options="dropdownValues" optionLabel="name" placeholder="Select" />

                <h5>選擇模板</h5>
                <Dropdown v-model="dropdownValue" :options="dropdownValues" optionLabel="name" placeholder="Select" />

                <h5>是否使用高精準度模型(耗時較久)</h5>
                <InputSwitch v-model="switchValue" />

                <h5></h5>
                <Button label="提交" class="mr-2 mb-2"></Button>
            </div>
        </div>
    </div>
</template>