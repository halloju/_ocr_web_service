<script>
import axios from 'axios';
import { ElLoading } from 'element-plus';

export default {
    components: {},
    name: 'General2',
    data() {
        return {
            // 前一步驟上傳的圖檔
            firstImage: this.$store.state.general_upload_image[0],
            allImage: this.$store.state.general_upload_image,
            regData: this.$store.state.general_upload_res.data.ocr_results,
            uploadPercentage: 0,
            isDownload: false,
            switchValue: false,
            switchButton: false,
            selectButtonValue: { name: '詳細資訊' },
            selectButtonValues: [{ name: '詳細資訊' }, { name: '文字' }]
        };
    },
    watch: {
        selectButtonValue: function (newVal) {
            if (newVal.name === '詳細資訊') {
                this.switchButton = false;
            } else {
                this.switchButton = true;
            }
        }
    },
    computed: {
        getFile() {
            this.firstImage = this.$store.state.general_upload_image[0];
            return this.firstImage;
        }
    },
    methods: {
        copyText() {
            const range = document.createRange();
            range.selectNode(this.$refs.message);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
            document.execCommand('copy');
        },
        submit() {
            const imageLen = this.allImage.length;
            const stepPercentage = 100 / imageLen;
            const generalImageResponseList = [];
            // 成功張數
            let count = 0;
            // 耗時秒數
            for (let i = 0; i < imageLen; i++) {
                // 前綴拿掉
                const base64Image = this.allImage[i].reader.split(',')[1];
                // 一張一張打
                axios
                    .post('/ocr/gpocr', {
                        image: base64Image,
                        image_complexity: 'medium',
                        language: 'Chinese'
                    })
                    .then((response) => {
                        generalImageResponseList.push(response);
                        this.uploadPercentage = this.uploadPercentage + stepPercentage;
                        count = count + 1;
                    })
                    .catch((error) => {
                        console.log(error);
                        if (error.code === 'ERR_NETWORK') {
                            this.status = 'network';
                        }
                    });
            }
            const loading = ElLoading.service({
                lock: true,
                text: 'Loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            setTimeout(() => {
                // 下一步
                this.$emit('nextStepEmit', 3);
                this.$store.commit('generalImageResponse', generalImageResponseList);
                loading.close();
            }, 2500);
        },
        back() {
            this.$emit('nextStepEmit', 1);
        }
    }
};
</script>
<template>
    <div class="grid p-fluid">
        <div class="col-12 md:col-7">
            <div class="card" style="overflow-x: scroll; overflow-y: scroll">
                <h5>第一個檔案</h5>
                <Image :src="firstImage.reader" alt="Image" width="500" preview />
            </div>
        </div>

        <div class="col-12 md:col-5">
            <div class="card">
                <div class="flex justify-content-between">
                    <h5>Response</h5>
                    <Button v-if="!switchButton" icon="pi pi-copy" class="p-button-text" @click="copyText"></Button>
                </div>
                <SelectButton v-model="selectButtonValue" :options="selectButtonValues" optionLabel="name" />
                <div v-if="!switchButton">
                    <div ref="message">
                        {{ regData }}
                    </div>
                </div>
                <div v-else>
                    <DataTable :value="regData" :scrollable="true" scrollHeight="400px" :loading="loading">
                        <Column field="text" header="text" style="min-width: 50px"></Column>
                        <Column field="tag" header="tag" style="min-width: 100px"></Column>
                    </DataTable>
                </div>

                <h5>我已確認單張結果</h5>
                <InputSwitch v-model="switchValue" :disabled="isDownload" />
                <br />
                <Button label=" 開始辨識全部檔案" class="mr-2 mb-2 pi pi-images" @click="submit" :disabled="!switchValue"></Button>
                <Button label=" 重新上傳" class="mr-2 mb-2 pi pi-upload" @click="back"></Button>
                <!-- <Button label=" 開始辨識全部檔案" class="mr-2 mb-2 pi pi-images" @click="submit" :disabled="!switchValue | isDownload"></Button> -->
                <!-- <Button label=" 下載 excel 檔" class="mr-2 mb-2 pi pi-download" @click="submit" :disabled="!isDownload"></Button> -->

                <!-- Progress Bar -->
                <el-progress :text-inside="true" :stroke-width="24" :percentage="uploadPercentage" status="success" color="#3b82f6" />
            </div>
        </div>
    </div>
</template>
