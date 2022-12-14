<script>
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
            firstImage: this.$store.state.general_upload_image[0],
        };
    },
    computed: {
        getFile() {
            this.firstImage = this.$store.state.general_upload_image[0]
            return  this.firstImage
        }
    },
    methods: {
        submit() {
            this.$router.push({ path: '/features/general/step2' });
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
                <Steps :model="nestedRouteItems" :readonly="true" />
                <h5>確認您的圖片</h5>
                <p>由於批次辨識時間較長，請確認辨識設定；若無任何問題，請點選開始辨識全部檔案。</p>
                <router-view />
            </div>
        </div>
    </div>

    <div class="grid p-fluid">
        <div class="col-12 md:col-9">
            <div class="card">
                <h5>上傳圖檔之一</h5>
                <Image src="" alt="Image" width="500" preview />
            </div>
        </div>

        <div class="col-12 md:col-3">
            <div class="card">
                <h5>辨識結果</h5>
                <ScrollPanel :style="{ width: '200px', height: '400px' }">
                    <p>
                        {"points": [[1,2],[1,3],[1,5],[1,8]], “text”: ”玉山金控與子公司", “tag”: “名稱”, "det_prob": 0.9586760401725769, "rec_prob": 0.9586760401725769}, {"points":[], "text": " 出生日期 ", “tag”: “出生抬頭”, "det_prob":
                        0.9586760401725769, "rec_prob": 0.9586760401725769}, {"points":[], "text": " 聯絡電話", “tag”: “電話抬頭”, "det_prob": 0.9586760401725769, "rec_prob": 0.9586760401725769} ]
                    </p>
                    <ScrollTop target="parent" :threshold="100" icon="pi pi-arrow-up"></ScrollTop>
                </ScrollPanel>

                <h5>已確認單張結果</h5>
                <InputSwitch v-model="switchValue" />

                <h5></h5>
                <Button label="開始辨識全部檔案" class="mr-2 mb-2" @click="submit" :disabled="!switchValue"></Button>
            </div>
        </div>
        <div class="col-12">
            <ProgressBar value="50" />
        </div>
    </div>
</template>
