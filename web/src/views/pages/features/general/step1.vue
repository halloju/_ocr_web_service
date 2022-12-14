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
            {{fileList}}
            {{dialogVisible}}
            <div class="card">
                <el-upload
                    :file-list="fileList"
                    list-type="picture-card"
                    :on-change="fileChange"
                    :on-remove="handleRemove"
                    :auto-upload="false"
                    :on-preview="handlePictureCardPreview"
                >
                    <el-icon><Plus /></el-icon>
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
            // upload 參數
            fileList: this.$store.state.general_upload_image,
            dialogVisible: false,

        };
    },
    methods: {
        submit() {
            this.$router.push({ path: '/features/general/step2' });
        },
        fileChange(file, resfileList){
            console.log('fileChange')
            console.log(resfileList)
            
            this.$store.commit('generalImageUpdate', resfileList);
            this.fileList = resfileList;
        },
        handleRemove(file){
            console.log('handleRemove')
            for (let i = 0; i < this.fileList.length; i++) {
                if (this.fileList[i]['uid'] === file.uid) {
                this.fileList.splice(i, 1);
                break;
                }
            }
            this.$store.commit('generalImageUpdate', this.fileList);

        },
        handlePictureCardPreview(file){
            console.log(file)
            this.dialogImageUrl = file.url;
            this.dialogVisible = true;
        },

    }
};
</script>
