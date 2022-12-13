<template>
    <div class="grid p-fluid">
        <div class="col-12">
            <div class="card card-w-title">
                <!-- Breadcrumb -->
                <Breadcrumb :home="breadcrumbHome" :model="breadcrumbItems" style="border-width: 0px" />
                <br />
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
                <el-upload action="#" list-type="picture-card" :auto-upload="false">
                    <el-icon><Plus /></el-icon>
                    <template #file="{ file }">
                    <div>
                        <img class="el-upload-list__item-thumbnail" :src="file.url" alt="" />
                        <span class="el-upload-list__item-actions">
                        <span
                            class="el-upload-list__item-preview"
                            @click="handlePictureCardPreview(file)"
                        >
                            <el-icon><zoom-in /></el-icon>
                        </span>
                        <span
                            v-if="!disabled"
                            class="el-upload-list__item-delete"
                            @click="handleDownload(file)"
                        >
                            <el-icon><Download /></el-icon>
                        </span>
                        <span
                            v-if="!disabled"
                            class="el-upload-list__item-delete"
                            @click="handleRemove(file)"
                        >
                            <el-icon><Delete /></el-icon>
                        </span>
                        </span>
                    </div>
                    </template>
                </el-upload>

                <el-dialog v-model="dialogVisible">
                    <img :src="dialogImageUrl" alt="Preview Image" style="width:400px"/>
                </el-dialog>
            </div>
        </div>

        <div class="col-12 md:col-3">
            <div class="card">
                <h5>選擇語言</h5>
                <Dropdown v-model="selectedLang" :options="languages" optionLabel="name" placeholder="Select" />

                <h5>是否使用高精準度模型(耗時較久)</h5>
                <InputSwitch v-model="switchValue" />

                <h5></h5>
                <Button label="提交" class="mr-2 mb-2" @click="submit"></Button>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    components: {},
    name: 'General1',
    data() {
        return {
            selectedLang: null,
            languages: [
                {name: '繁體中文', code: 'zhant'},
                {name: '英語', code: 'english'},
            ],
            nestedRouteItems: [
                {
                    label: '圖檔上傳',
                    to: '/features/general/step1'
                },
                {
                    label: '單張結果確認',
                    to: '/features/general/step2'
                }
            ],
            breadcrumbHome: { icon: 'pi pi-home', to: '/' },
            breadcrumbItems: [
                { label: '主要功能', to: '#' },
                { label: '通用文件辨識', to: '#' },
                { label: '通用辨識', to: '#' },
                { label: '圖檔上傳', to: '#' }
            ],
            switchValue: false,
            idCardImgUrl: '',
            idCardIsUpload: false,
            idCardUploadPercentage: 0,
            errorImgUrls: [],
            dialogVisible: false,
        };
    },
    props: {
    /*可以在使用组件的时候传入一个支持上传的图片格式的数组进来，不传默认default数组*/
        supportType: {//支持上传文件的格式
        default: () => ['image/jpeg', 'image/jpg', 'image/png'],
        type: Array
        }
    },
    methods: {
        submit() {
            this.$router.push({ path: '/features/general/step2' });
        },
        handlePictureCardPreview(file) {
            this.dialogImageUrl = file.url
            this.dialogVisible = true
        }

    }
};
</script>
