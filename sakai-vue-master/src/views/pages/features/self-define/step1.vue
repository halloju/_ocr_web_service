<script>


export default {
  components: {
  },
  name: 'SelfDefine1',
  data() {
    return {
        nestedRouteItems: [
                            {
                            label: '模板圖檔上傳',
                            to: '/features/self-define/step1'
                            },
                            {
                            label: '文字位置標註',
                            to: '/features/self-define/step2'
                            },
                            {
                            label: '方塊位置標註',
                            to: '/features/self-define/step3'
                            },
                            {
                            label: '遮罩位置標註',
                            to: '/features/self-define/step4'
                            },
                            {
                            label: '確認',
                            to: '/features/self-define/step5'
                            },
                        ],
        breadcrumbHome: { icon: 'pi pi-home', to: '/' },
        breadcrumbItems: [{ label: '主要功能', to: '#' }, { label: '自定義模板', to: '#' }, { label: '新增自定義模板', to: '#' }, { label: '模板圖檔上傳', to: '#' }],
        switchValue: false,

    };
  },
  methods: {
    next() {
                this.$router.push({path:"/features/self-define/step2"})
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
                <h5>新增自定義模板</h5>
                <p>上傳一張清晰的圖片進行標注，並於後續步驟框選標註需辨識的區域位於哪一個區域。</p>
                <router-view />
            </div>
        </div>
    </div>
    
    <div class="grid p-fluid">
        <div class="col-12 md:col-9">
            <div class="card">
                <FileUpload name="demo[]" url="./upload" :maxFileSize="1000000" :fileLimit="3" :previewWidth="500" chooseLabel="選擇檔案" uploadLabel="上傳檔案" cancelLabel="取消上傳" />
            </div>

        </div>

        <div class="col-12 md:col-3">
            <div class="card">

                <h5>是否匯入預先設定檔</h5>
                <FileUpload mode="basic" name="demo[]" url="./upload" :auto="true" chooseLabel="匯入"/>
                <h5></h5>
                <Button label="下一步" class="p-button-info mr-2 mb-2" @click="next"></Button>
            </div>
        </div>
    </div>
</template>