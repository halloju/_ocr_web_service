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
                <p>請上傳一張或多張圖片，下一步會先辨識第一張圖片讓您確認結果，再進行全部辨識。</p>
                <router-view />
            </div>
        </div>
    </div>

    <div class="grid p-fluid">
        <div class="col-12 md:col-9">
            <div class="card">
                <el-upload :file-list="fileList" 
                           list-type="picture-card" 
                           :on-change="fileChange" 
                           :on-remove="handleRemove" 
                           :auto-upload="false" 
                           :on-preview="handlePictureCardPreview"
                           accept="image/*">
                    <el-icon><Plus /></el-icon>
                </el-upload>
                <el-dialog v-model="dialogVisible" :width="dialogWidth">
                    <img :src="dialogImageUrl" alt="Preview Image" @load="onLoadImg" :width="imgWidth" />
                </el-dialog>
            </div>
        </div>
        <div class="col-12 md:col-3">
            <div class="card">
                <h5>選擇語言</h5>
                <Dropdown v-model="selectedLang" :options="languages" optionLabel="name" placeholder="Select" />

                <h5>使用高精準度模型</h5>
                <p>注意：當您使用高精準模型時耗時會較久</p>
                <InputSwitch v-model="switchValue" />

                <h5></h5>
                <Button label="圖檔提交" class="mr-2 mb-2" @click="submit" :disabled="disableUpload"></Button>
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
                { name: '繁體中文', code: 'zhant' },
                { name: '英語', code: 'english' }
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
            fileList: [],
            dialogVisible: false,
            imaWidth: '',
            dialogWidth: '',
            imageSource: '',
        };
    },
    computed: {
        disableUpload() {
            if (this.fileList.length === 0 | this.selectedLang===null) {
                return true;
            } else {
                return false;
            }
        }
    },
    methods: {
        submit() {
            this.$store.commit('generalImageUpdate', this.fileList);
            this.$router.push({ path: '/features/general/step2' });
        },
        fileChange(file, resfileList) {
            console.log('fileChange');

            // allows image only
            if (file.raw.type.indexOf('image/') >= 0) {
                    var reader = new FileReader();
                    reader.onload = (f) => {
                        this.imageSource = f.target.result;
                        file.reader = f.target.result;
                    };
                    reader.readAsDataURL(file.raw);
            }
            console.log(file)
            this.fileList.push(file)
            console.log(this.fileList)

        },
        handleRemove(file) {
            console.log('handleRemove');
            for (let i = 0; i < this.fileList.length; i++) {
                if (this.fileList[i]['uid'] === file.uid) {
                    this.fileList.splice(i, 1);
                    break;
                }
            }
        },
        handlePictureCardPreview(file) {
            console.log(file);
            this.dialogImageUrl = file.url;
            this.dialogVisible = true;
        },
        onLoadImg(e) {
            const img = e.target;
            let width = 0;
            if (img.fileSize > 0 || (img.naturalWidth > 1 && img.naturalHeight > 1)) {
                width = img.naturalWidth;
            }
            if (img.naturalWidth < 200) {
                width = 200;
            } else if (img.naturalHeight > img.naturalWidth && width > 370) {
                width = 370;
            } else {
                width = 500;
            }
            this.imgWidth = width;
            this.dialogWidth = width + 40;
        }
    }
};
</script>
