<script>
export default {
    components: {},
    name: 'SelfDefine3',
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
                }
            ],
            breadcrumbHome: { icon: 'pi pi-home', to: '/' },
            breadcrumbItems: [
                { label: '主要功能', to: '#' },
                { label: '自定義模板', to: '#' },
                { label: '新增自定義模板', to: '#' },
                { label: '模板圖檔上傳', to: '#' }
            ],
            switchValue: false
        };
    },
    methods: {
        next() {
            this.$router.push({ path: '/features/self-define/step4' });
        }
    }
};
</script>
<template>
    <div class="grid p-fluid">
        <div class="col-12">
            <div class="card card-w-title">
                <!-- Breadcrumb -->
                <Breadcrumb :home="breadcrumbHome" :model="breadcrumbItems" style="border-width: 0px" />
                <br />
                <!-- Step -->
                <Steps :model="nestedRouteItems" :readonly="false" />
                <h5>核取方塊位置標註</h5>
                <p>辨識圖片中核取方塊區域和上傳的模板圖片中核取方塊區域是否相同，e.g. 空白和是否有打勾。</p>
                <p>建議：模板圖片方塊位置為空白，這樣在辨識區域時是否有其他痕跡時，不會受限於痕跡種類。</p>
                <router-view />
            </div>
        </div>
    </div>

    <div class="grid p-fluid">
        <div class="col-12 md:col-8">
            <div class="card"></div>
        </div>

        <div class="col-12 md:col-4">
            <div class="card">
                <div class="surface-section">
                    <div class="font-medium text-3xl text-900 mb-3">核取方塊辨識位置</div>
                    <ul class="list-none p-0 m-0">
                        <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                            <div class="text-500 w-6 md:w-2 font-medium">No.</div>
                            <div class="text-900 w-full md:w-3 md:flex-order-0 flex-order-1">要項名稱</div>
                            <div class="w-6 md:w-2 flex justify-content-end">操作</div>
                        </li>
                        <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                            <div class="text-500 w-6 md:w-2 font-medium">1.</div>
                            <div class="text-900 w-full md:w-3 md:flex-order-0 flex-order-1">姓名</div>
                            <div class="w-6 md:w-6 flex justify-content-end">
                                <Button label="Edit" icon="pi pi-pencil" class="p-button-info" style="margin-right: 5px"></Button>
                                <Button label="Delete" icon="pi pi-times" class="p-button-danger"></Button>
                            </div>
                        </li>
                        <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                            <div class="text-500 w-6 md:w-2 font-medium">2.</div>
                            <div class="text-900 w-full md:w-3 md:flex-order-0 flex-order-1">電話號碼</div>
                            <div class="w-6 md:w-6 flex justify-content-end">
                                <Button label="Edit" icon="pi pi-pencil" class="p-button-info" style="margin-right: 5px"></Button>
                                <Button label="Delete" icon="pi pi-times" class="p-button-danger"></Button>
                            </div>
                        </li>
                        <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                            <div class="text-500 w-6 md:w-2 font-medium">3.</div>
                            <div class="text-900 w-full md:w-3 md:flex-order-0 flex-order-1">標註C</div>
                            <div class="w-6 md:w-6 flex justify-content-end">
                                <Button label="Edit" icon="pi pi-pencil" class="p-button-info" style="margin-right: 5px"></Button>
                                <Button label="Delete" icon="pi pi-times" class="p-button-danger"></Button>
                            </div>
                        </li>
                        <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                            <div class="text-500 w-6 md:w-2 font-medium">4.</div>
                            <div class="text-900 w-full md:w-3 md:flex-order-0 flex-order-1">標註B</div>
                            <div class="w-6 md:w-6 flex justify-content-end">
                                <Button label="Edit" icon="pi pi-pencil" class="p-button-info" style="margin-right: 5px"></Button>
                                <Button label="Delete" icon="pi pi-times" class="p-button-danger"></Button>
                            </div>
                        </li>
                        <li class="flex align-items-center py-3 px-2 border-top-1 border-bottom-1 surface-border flex-wrap">
                            <div class="text-500 w-6 md:w-2 font-medium">5.</div>
                            <div class="text-900 w-full md:w-3 md:flex-order-0 flex-order-1 line-height-3">標註A</div>
                            <div class="w-6 md:w-6 flex justify-content-end">
                                <Button label="Edit" icon="pi pi-pencil" class="p-button-info" style="margin-right: 5px"></Button>
                                <Button label="Delete" icon="pi pi-times" class="p-button-danger"></Button>
                            </div>
                        </li>
                    </ul>
                </div>
                <Button label="下一步" class="p-button-info mr-2 mb-2" @click="next"></Button>
            </div>
        </div>
    </div>
</template>
