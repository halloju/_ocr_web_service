<template>
    <div class="content">
        <div class="contentWrapper container py-5 px-5">
            <form class="fillData_form">
                <div class="text-center">
                    <p class="form-grop-title py-1 fs-20 fw-500 color-primary mb-5">{{correct.title}}</p>
                    <img :src="correct.imgSrc" alt="" class="w-100 mw-400">
                    <p v-html="correct.textHtml" class="mt-4 lh-30"></p>
                </div>
                <div class="d-flex justify-content-center">
                    <router-link to="/" class="btn bg-primary mt-4" @click="home" >返回首頁</router-link>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
@import '../assets/css/form.css';
</style>
<script>
export default {
    data() {
        return {
            correct:{
                title: '恭喜您正確回答！',
                imgSrc: '../src/assets/images/img01.svg',
                textHtml: '恭喜您完成【智能金融】區智能投資健檢測驗<br>另有智能房屋價值試算體驗等您來挑戰！<br>【數位銀行】、【多元支付】區也有精采互動，集章可兌換精美禮品！'
            },
            wrong:{
                title: '差一點就成功了…',
                imgSrc: '../src/assets/images/img02.svg',
                textHtml: '感謝您完成【智能金融】區智能投資健檢體驗，另有智能房屋價值試算體驗等您來挑戰！<br>【數位銀行】、【多元支付】區也有精采互動，集章可兌換精美禮品！'
            }
        }
    },
    methods: {
        home() {
            this.$store.commit('back');
        }
    }
}
</script>