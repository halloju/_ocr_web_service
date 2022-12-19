<template>
    <div class="grid p-fluid">
        <div class="col-12">
            <div class="card card-w-title">
                <!-- Breadcrumb -->
                <Breadcrumb :home="breadcrumbHome" :model="breadcrumbItems" style="border-width: 0px" />
                <br />
                <!-- Step -->
                <Steps :model="nestedRouteItems" :readonly="true" />
                <h5>確認您的圖片</h5>
                <p>由於批次辨識時間較長，請確認辨識設定；若無任何問題，請點選開始辨識全部檔案。</p>
                <router-view />
            </div>
        </div>
    </div>

    <div class="grid p-fluid">
        <div class="col-12 md:col-7" >
            <div class="card" style="overflow-x:scroll;overflow-y:scroll;">
                <h5>上傳圖檔之一</h5>
                <Image :src="firstImage.reader" alt="Image" width="500" preview />
            </div>
        </div>

        <div class="col-12 md:col-5">
            <div class="card">
                <h5>辨識結果</h5>
                <DataTable :value="getRegData" :scrollable="true" scrollHeight="400px" :loading="loading">
                    <Column field="text" header="text" style="min-width:50px"></Column>
                    <Column field="points" header="points" style="min-width:50px"></Column>
                    <Column field="tag" header="tag" style="min-width:50px"></Column>
                    <Column field="det_prob" header="det_prob" style="min-width:50px"></Column>
                    <Column field="rec_prob" header="rec_prob" style="min-width:50px"></Column>
                </DataTable>

                <h5>已確認單張結果</h5>
                <InputSwitch v-model="switchValue" />
                <br>
                <Button label="開始辨識全部檔案" class="mr-2 mb-2" @click="submit" :disabled="!switchValue"></Button>
                <!-- Progress Bar -->
                <el-progress
                :text-inside="true"
                :stroke-width="24"
                :percentage="uploadPercentage"
                status="success"
                />
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios";

export default {
    components: {},
    name: 'General2',
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
                { label: '單張結果確認', to: '#' }
            ],
            switchValue: false,
            // 前一步驟上傳的圖檔
            firstImage: this.$store.state.general_upload_image[0],
            regData: [{"points": [[1,2],[1,3],[1,5],[1,8]], 
                       "text": "玉山金控與子公司", 
                       "tag": "名稱",
                       "det_prob": 0.9586760401725769,
                       "rec_prob": 0.9586760401725769},
                      {"points":[], 
                       "text": "出生日期",
                       "tag": "出生抬頭",
                       "det_prob": 0.9586760401725769,
                       "rec_prob": 0.9586760401725769}, 
                      {"points":[], 
                       "text": "聯絡電話",
                       "tag": "電話抬頭",
                       "det_prob": 0.9586760401725769,
                       "rec_prob": 0.9586760401725769}],
            uploadPercentage: 0,
        };
    },
    computed: {
        getFile() {
            this.firstImage = this.$store.state.general_upload_image[0];
            return this.firstImage;
        },
        getRegData() {
            for (let i = 0; i < this.regData.length; i++) {
                console.log(this.regData[i])
                this.regData[i].det_prob = this.regData[i].det_prob.toFixed(2);
                this.regData[i].rec_prob = this.regData[i].rec_prob.toFixed(2);
            }
            return this.regData
        }
    },
    methods: {
        submit() {
            let formData = new FormData();
            formData.append('file', this.file);
            axios.post( '/file-progress',
                formData,
                    { headers: {'Content-Type': 'multipart/form-data'},
                onUploadProgress: function( progressEvent ) {
                    this.uploadPercentage = parseInt( Math.round( ( progressEvent.loaded / progressEvent.total ) * 100 ) );
                    }.bind(this)
                }
            ).then(function(){
                console.log('SUCCESS!!');
            })
            .catch(function(){
                console.log('FAILURE!!');
            });
        }
    }
};
</script>