<template>
        <div class="content">
        <!-- steps -->
        <div class="steps mb-3">
            <ul class="stepsList">
                <li class="stepsName todo">
                    <div class="stepsNum">1</div>
                    <div class="stepsTxt">現有資產</div>
                </li>
                <li class="stepsName">
                    <div class="stepsNum">2</div>
                    <div class="stepsTxt">確認內容</div>
                </li>
                <li class="stepsName todo">
                    <div class="stepsNum">3</div>
                    <div class="stepsTxt">市場事件</div>
                </li>
                <li class="stepsName todo">
                    <div class="stepsNum">4</div>
                    <div class="stepsTxt">AI模型運算</div>
                </li>
                <li class="stepsName todo">
                    <div class="stepsNum">5</div>
                    <div class="stepsTxt">資產配置健檢</div>
                </li>
            </ul>
        </div>
        <!-- steps -->
        <div class="contentWrapper container py-5 px-5">
            <form class="fillData_form">
                <p class="form-grop-title py-1 fs-18 fw-500 mb-4">在開始體驗前，請先預設現有的資產比例，您可挑選<span class="color-primary">5檔產品</span>，所有產品<span class="color-primary">相加為100%</span>。</p>
                <!-- 我的投資部位組合 -->
                <div class="bg-grey p-4">
                    <div class="row pt-2 pb-4 px-4">
                        <div class="col-6 col-lg-6 col-xl-4 pb-1 pl-0">
                            <label for="houseType" class="input_label">現有資產共100萬元新台幣，已配置資產部位加總</label>
                        </div>
                        <div class="col-6 col-lg-4 col-xl-4 pb-1 px-0">
                            <div class="inputBox w-100">
                                <p>100%</p>
                            </div>
                        </div>
                    </div>
                    <div class="row pt-2 pb-4 px-4">
                        <div class="col-6 pb-1 px-0">
                            <div class="row pr-3">
                                <div class="col-5">
                                    <label for="" class="input_label">1. 摩根中國A股基金</label>
                                </div>
                                <div class="col-7">
                                    <p>{{cus_input["E441"]}}%</p>
                                </div>
                            </div>
                            <div class="row pr-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">2. 亞馬遜公司債券</label>
                                </div>
                                <div class="col-7">
                                    <p>{{cus_input["A394"]}}%</p>
                                </div>
                            </div>
                            <div class="row pr-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">3. 貝萊德拉丁美洲基金(美元)</label>
                                </div>
                                <div class="col-7">
                                    <p>{{cus_input["AG01"]}}%</p>
                                </div>
                            </div>
                            <div class="row pr-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">4. NN(L)新興市場債券基金(X股美元)</label>
                                </div>
                                <div class="col-7">
                                    <p>{{cus_input["AP15"]}}%</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6 pb-1 px-0">
                            <div class="row pl-3">
                                <div class="col-5">
                                    <label for="" class="input_label">5. 安聯美元短年期非投資等級債券基金AM穩定月收類股(美元)</label>
                                </div>
                                <div class="col-7">
                                    <p>{{cus_input["BB74"]}}%</p>
                                </div>
                            </div>
                            <div class="row pl-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">6. 景順歐洲大陸企業基金A-年配息股(美元)</label>
                                </div>
                                <div class="col-7">
                                    <p>{{cus_input["EE62"]}}%</p>
                                </div>
                            </div>
                            <div class="row pl-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">7. 史坦普500指數基金SPDR</label>
                                </div>
                                <div class="col-7">
                                    <p>{{cus_input["ET31"]}}%</p>
                                </div>
                            </div>
                            <div class="row pl-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">8. 蘋果電腦</label>
                                </div>
                                <div class="col-7">
                                    <p>{{cus_input["ST07"]}}%</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="d-flex justify-content-center">
                    <router-link to="/question" class="btn bg-primary mt-4 mx-2">修改</router-link>
                    <router-link to="/market" class="btn bg-primary mt-4 mx-2">確定</router-link>
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
            cus_input: this.$store.state.cus_input,
        }
    }
}
</script>