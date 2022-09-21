<template>
    <div class="content">
        <div class="contentWrapper container py-5 px-5">
            <form class="fillData_form">
                <div class="text-center">
                    <img src="../assets/images/reward.svg" alt="" class="mw-80">
                    <p class="form-grop-title py-1 fs-20 fw-500 color-primary mb-4">有獎徵答</p>
                </div>
                <div class="row pt-2 pb-4">
                    <div class="col-12 pb-1 mb-3">
                        <p class="color-primary fs-18 fw-500 mb-3">【智能投資健檢】測驗</p>
                        <label for="feature" class="input_label">請問下列哪一項是智能投資健檢的特色：</label>
                    </div>
                    <div class="col-6 pb-1">
                        <div class="col-12 p-0 mb-3">
                            <input type="radio" class="radio-input" id="feature01" name="feature">
                            <label class="radio-label d-flex" for="feature01"><p>提供不同資產配置建議</p></label>
                        </div>
                        <div class="col-12 p-0 mb-3">
                            <input type="radio" class="radio-input" id="feature02" name="feature">
                            <label class="radio-label d-flex" for="feature02"><p>市場變化時，以AI分析提供資產配置調整建議</p></label>
                        </div>
                    </div>
                    <div class="col-6 pb-1">
                        <div class="col-12 p-0 mb-3">
                            <input type="radio" class="radio-input" id="feature03" name="feature">
                            <label class="radio-label d-flex" for="feature03"><p>挑選最適合的基金</p></label>
                        </div>
                        <div class="col-12 p-0 mb-3">
                            <input type="radio" class="radio-input" id="feature04" name="feature">
                            <label class="radio-label d-flex" for="feature04"><p>提供報酬率最高的產品</p></label>
                        </div>
                    </div>
                </div>
                <div class="row pt-2 pb-4">
                    <div class="col-12 pb-1 mb-3">
                        <label for="feature" class="input_label">請問體驗後如欲購買或調整資產，可如何調整資產？</label>
                    </div>
                    <div class="col-6 pb-1">
                        <div class="col-12 p-0 mb-3">
                            <input type="radio" class="radio-input" id="assets01" name="assets">
                            <label class="radio-label d-flex" for="assets01"><p>使用玉山行動銀行</p></label>
                        </div>
                        <div class="col-12 p-0 mb-3">
                            <input type="radio" class="radio-input" id="assets02" name="assets">
                            <label class="radio-label d-flex" for="assets02"><p>使用玉山網路銀行</p></label>
                        </div>
                    </div>
                    <div class="col-6 pb-1">
                        <div class="col-12 p-0 mb-3">
                            <input type="radio" class="radio-input" id="assets03" name="assets">
                            <label class="radio-label d-flex" for="assets03"><p>洽詢所屬理專</p></label>
                        </div>
                        <div class="col-12 p-0 mb-3">
                            <input type="radio" class="radio-input" id="assets04" name="assets">
                            <label class="radio-label d-flex" for="assets04"><p>以上皆是</p></label>
                        </div>
                    </div>
                </div>

                <div class="d-flex justify-content-center">
                    <router-link to="/quizResult" class="btn bg-primary mt-4 mx-2">公布解答</router-link>
                    <router-link to="/" class="btn bg-primary mt-4 mx-2" @click="home">返回首頁</router-link>
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

    },
    methods: {
        home() {
            this.$store.commit('back');
        }
    }

}
</script>