<template>
    <div class="content">
        <!-- steps -->
        <div class="steps mb-3">
            <ul class="stepsList">
                <li class="stepsName todo">
                    <div class="stepsNum">1</div>
                    <div class="stepsTxt">現有資產</div>
                </li>
                <li class="stepsName todo">
                    <div class="stepsNum">2</div>
                    <div class="stepsTxt">確認內容</div>
                </li>
                <li class="stepsName">
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
                <p class="form-grop-title color-primary py-1 fs-18 fw-500 mb-4">在投資過程中，市場總是不斷的變化，請挑選以下一種市場事件，模擬市場變化。</p>
                <div class="row my-5">
                    <div class="col-4 px-2 px-lg-3">
                        <input type="radio" class="radio-input" id="event01" name="event" v-model="event" :value="'01'">
                        <label class="radio-label d-flex" for="event01">
                            <p>美國頁岩油增產且OPEC拒絕減產</p>
                        </label>
                        <img src="../assets/images/event01.jpg" alt="" class="w-100 mt-3">
                    </div>
                    <div class="col-4 px-2 px-lg-3">
                        <input type="radio" class="radio-input" id="event02" name="event" v-model="event" :value="'02'">
                        <label class="radio-label d-flex" for="event02">
                            <p>Fed宣布無限QE應對新冠疫情衝擊</p>
                        </label>
                        <img src="../assets/images/event02.jpg" alt="" class="w-100 mt-3">
                    </div>
                    <div class="col-4 px-2 px-lg-3">
                        <input type="radio" class="radio-input" id="event03" name="event" v-model="event" :value="'03'">
                        <label class="radio-label d-flex" for="event03">
                            <p>Fed啟動升息對抗通膨加劇</p>
                        </label>
                        <img src="../assets/images/event03.jpg" alt="" class="w-100 mt-3">
                    </div>
                </div>
                <div class="d-flex justify-content-center">
                    <router-link v-if="nextPage" to="/analyzing" class="btn bg-primary mt-4" @click="sendAPI">下一步</router-link>
                    <router-link v-else to="" class="btn bg-secondary mt-4">下一步</router-link>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped>
@import '../assets/css/form.css';
</style>

<script>
import axios from "axios"

export default {
    data() {
        return {
            event: this.$store.state.event,
            cus_input: this.$store.state.cus_input,
        }
    },
    methods: {
        async sendAPI() {
            this.$store.commit('step3', this.event);
            await axios.post("/calculate/", {
                                "cus_input": {
                                    "AP15": this.cus_input["AP15"]/100,
                                    "ST07": this.cus_input["ST07"]/100,
                                    "EE62": this.cus_input["EE62"]/100,
                                    "ET31": this.cus_input["ET31"]/100,
                                    "A394": this.cus_input["A394"]/100,
                                    "BB74": this.cus_input["BB74"]/100,
                                    "E441": this.cus_input["E441"]/100,
                                    "AG01": this.cus_input["AG01"]/100
                                    },
                                "event": this.event,
                            })
                            .then( (response) =>
                               {this.$store.commit('sendAPI', response.data);})
                            .catch( (error) => console.log(error))
        }
    },
    computed: {
        nextPage: function(){
            if (["01", "02", "03"].includes(this.event)) {
                return true
            }
            return false
        }
    }
}
</script>
