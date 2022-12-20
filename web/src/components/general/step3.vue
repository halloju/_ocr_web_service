<template>
    <div class="grid p-fluid">
        <div class="col-12" >
            <div class="card" style="overflow-x:scroll;overflow-y:scroll;">
                <Document style="width: 10em;"/> 成功辨識：ＸＸ張，共耗時 XX 秒
                <br><br>
                <Button label=" 下載 excel 檔案" class="mr-2 mb-2 pi pi-download" @click="submit" style="width:200px;"></Button>
                <Button label=" 繼續圖檔上傳" class="mr-2 mb-2 pi pi-play" @click="back" style="width:200px;"></Button>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios";

export default {
    components: {},
    name: 'General3',
    data() {
        return {
            isDownload: false,
        };
    },
    computed: {

    },
    methods: {
        submit() {
            const imageLen = this.allImage.length
            const stepPercentage = 100 / imageLen
            const generalImageResponseList = []
            for (let i = 0; i < imageLen; i++) {

                // 前綴拿掉
                const base64Image = this.allImage[i].reader.split(',')[1]
                // 一張一張打
                axios.post("/ocr/gpocr", {
                                "image": base64Image,
                                "image_complexity": 'medium',
                                "language": 'Chinese',
                            })
                            .then( (response) =>
                               {
                                generalImageResponseList.push(response)
                                // 進度條
                                this.uploadPercentage = (this.uploadPercentage + stepPercentage)
                                })
                            .catch( (error) => {
                                console.log(error)
                                if(error.code === 'ERR_NETWORK'){
                                    this.status = 'network';
                                }
                })
                this.$store.commit('generalImageResponse', generalImageResponseList);
            }

            // Go to next page
            // this.$emit('nextStepEmit', 3)
            this.isDownload = true;
        },
        back() {
            this.$emit('nextStepEmit', 1)
        }
    }
};
</script>