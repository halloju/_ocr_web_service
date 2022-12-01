<script>


export default {
  components: {
  },
  name: 'General1',
  data() {
    return {
        nestedRouteItems: [
                                {
                                    label: '圖檔上傳',
                                    to: '/features/general/step1'
                                },
                                {
                                    label: '單張結果確認',
                                    to: '/features/general/step2'
                                },
                            ],
        breadcrumbHome: { icon: 'pi pi-home', to: '/' },
        breadcrumbItems: [{ label: '主要功能', to: '#' }, { label: '通用文件辨識', to: '#' }, { label: '通用辨識', to: '#' }, { label: '圖檔上傳', to: '#' }],
        switchValue: false,

    };
  },
  methods: {
    submit() {
                this.$router.push({path:"/features/general/step2"})
            }
    }

};
</script>
<template>
    <div class="grid p-fluid">
        <div class="col-12">
            <div class="card card-w-title">
                <!-- Breadcrumb -->
                <Breadcrumb :home="breadcrumbHome" :model="breadcrumbItems" style="border-width: 0px;"/>
                <br>
                <!-- Step -->
                <Steps :model="nestedRouteItems" :readonly="true" />
                <h5>通用辨識</h5>
                <p>請上傳一張或多張圖片。</p>
                <router-view />
            </div>
        </div>
    </div>
    
    <div class="grid p-fluid">
        <div class="col-12 md:col-9">
            <div class="card">
                <FileUpload name="demo[]" url="./upload" :maxFileSize="1000000" :fileLimit="3" :previewWidth="500" chooseLabel="選擇檔案" uploadLabel="上傳檔案" cancelLabel="取消上傳檔案" />
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
                <Button label="提交" class="mr-2 mb-2" @click="submit"></Button>
            </div>
        </div>
    </div>
</template>