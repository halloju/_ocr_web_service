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
    <img w-full :src="dialogImageUrl" alt="Preview Image" />
  </el-dialog>
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
<script>
import { Delete, Download, Plus, ZoomIn } from '@element-plus/icons-vue'
import 'element-plus/es/components/icon/style/css'

export default {
    components: {},
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
                }
            ],
            breadcrumbHome: { icon: 'pi pi-home', to: '/' },
            breadcrumbItems: [
                { label: '主要功能', to: '#' },
                { label: '通用文件辨識', to: '#' },
                { label: '通用辨識', to: '#' },
                { label: '圖檔上傳', to: '#' }
            ],
            switchValue: false
        };
    },
    methods: {
        submit() {
            this.$router.push({ path: '/features/general/step2' });
        }
    }
};
</script>
