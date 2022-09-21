<template>
    <div class="content">
        <!-- steps -->
        <div class="steps mb-3">
            <ul class="stepsList">
                <li class="stepsName">
                    <div class="stepsNum">1</div>
                    <div class="stepsTxt">現有資產</div>
                </li>
                <li class="stepsName todo">
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
                        <div class="col-4 col-lg-4 col-xl-4 pb-1 px-0">
                            <div class="inputBox w-90">{{add}}%</div>
                            <div class="inputAlert">錯訊</div>
                        </div>
                        <div v-if="errorShake" for="houseType" class="data-verify">資產部位加總超過 100 %</div>
                    </div>
                    <div class="row pt-2 pb-4 px-4">
                        <div class="col-6 pb-1 px-0">
                            <div class="row pr-3">
                                <div class="col-5">
                                    <label for="" class="input_label">1. 摩根中國A股基金</label>
                                </div>
                                <div class="col-7">
                                    <select name="city" id="city" class="w-100" v-model="e441">
                                        <option value="請選擇比例" disabled selected>請選擇比例</option>
                                        <option value="0">0</option>
                                        <option v-for="option in options" :value="option.val" :disabled="selectComputed[0]">{{option.item}}</option>
                                    </select>
                                    <div class="inputAlert">錯訊</div>
                                </div>
                            </div>
                            <div class="row pr-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">2. 亞馬遜公司債券</label>
                                </div>
                                <div class="col-7">
                                    <select name="city" id="city" class="w-100" v-model="a394">
                                        <option value="請選擇比例" disabled selected>請選擇比例</option>
                                        <option value=0>0</option>
                                        <option v-for="option in options" :value="option.val" :disabled="selectComputed[1]">{{option.item}}</option>
                                    </select>
                                    <div class="inputAlert">錯訊</div>
                                </div>
                            </div>
                            <div class="row pr-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">3. 貝萊德拉丁美洲基金(美元)</label>
                                </div>
                                <div class="col-7">
                                    <select name="city" id="city" class="w-100" v-model="ag01">
                                        <option value="請選擇比例" disabled selected>請選擇比例</option>
                                        <option value=0>0</option>
                                        <option v-for="option in options" :value="option.val" :disabled="selectComputed[2]">{{option.item}}</option>
                                    </select>
                                    <div class="inputAlert">錯訊</div>
                                </div>
                            </div>
                            <div class="row pr-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">4. NN(L)新興市場債券基金(X股美元)</label>
                                </div>
                                <div class="col-7">
                                    <select name="city" id="city" class="w-100" v-model="ap15">
                                        <option value="請選擇比例" disabled selected>請選擇比例</option>
                                        <option value=0>0</option>
                                        <option v-for="option in options" :value="option.val" :disabled="selectComputed[3]">{{option.item}}</option>
                                    </select>
                                    <div class="inputAlert">錯訊</div>
                                </div>
                            </div>
                        </div>
                        <div class="col-6 pb-1 px-0">
                            <div class="row pl-3">
                                <div class="col-5">
                                    <label for="" class="input_label">5. 安聯美元短年期非投資等級債券基金AM穩定月收類股(美元)</label>
                                </div>
                                <div class="col-7">
                                    <select name="city" id="city" class="w-100" v-model="bb74">
                                        <option value="請選擇比例" disabled selected>請選擇比例</option>
                                        <option value=0>0</option>
                                        <option v-for="option in options" :value="option.val" :disabled="selectComputed[4]">{{option.item}}</option>
                                    </select>
                                    <div class="inputAlert">錯訊</div>
                                </div>
                            </div>
                            <div class="row pl-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">6. 景順歐洲大陸企業基金A-年配息股(美元)</label>
                                </div>
                                <div class="col-7">
                                    <select name="city" id="city" class="w-100" v-model="ee62">
                                        <option value="請選擇比例" disabled selected>請選擇比例</option>
                                        <option value=0>0</option>
                                        <option v-for="option in options" :value="option.val" :disabled="selectComputed[5]">{{option.item}}</option>
                                    </select>
                                    <div class="inputAlert">錯訊</div>
                                </div>
                            </div>
                            <div class="row pl-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">7. 史坦普500指數基金SPDR</label>
                                </div>
                                <div class="col-7">
                                    <select name="city" id="city" class="w-100" v-model="et31">
                                        <option value="請選擇比例" disabled selected>請選擇比例</option>
                                        <option value=0>0</option>
                                        <option v-for="option in options" :value="option.val" :disabled="selectComputed[6]">{{option.item}}</option>
                                    </select>
                                    <div class="inputAlert">錯訊</div>
                                </div>
                            </div>
                            <div class="row pl-3 mt-4">
                                <div class="col-5">
                                    <label for="" class="input_label">8. 蘋果電腦</label>
                                </div>
                                <div class="col-7">
                                    <select name="city" id="city" class="w-100" v-model="st07">
                                        <option value="請選擇比例" disabled selected>請選擇比例</option>
                                        <option value=0>0</option>
                                        <option v-for="option in options" :value="option.val" :disabled="selectComputed[7]">{{option.item}}</option>
                                    </select>
                                    <div class="inputAlert">錯訊</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="d-flex justify-content-center">
                    <router-link v-if="equal100" to="/confirm" class="btn bg-primary mt-4" @click="SaveData" >下一步</router-link>
                    <router-link v-else="equal100" to="" class="btn bg-secondary mt-4">下一步</router-link>
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
      ap15: this.$store.state.cus_input["AP15"],
      st07: this.$store.state.cus_input["ST07"],
      ee62: this.$store.state.cus_input["EE62"],
      et31: this.$store.state.cus_input["ET31"],
      a394: this.$store.state.cus_input["A394"],
      bb74: this.$store.state.cus_input["BB74"],
      e441: this.$store.state.cus_input["E441"],
      ag01: this.$store.state.cus_input["AG01"],
      total: 0,
      cannotSelect: false,
      options: [{val: 10, item: "10"},
                {val: 20, item: "20"},
                {val: 30, item: "30"},
                {val: 40, item: "40"},
                {val: 50, item: "50"},
                {val: 60, item: "60"},
                {val: 70, item: "70"},
                {val: 80, item: "80"},
                {val: 90, item: "90"},
                {val: 100, item: "100"}]
      }
  },
  methods:{

  },
  computed:{
    add: function() {
        // 計算加總
        this.total = parseInt(this.ap15) + parseInt(this.st07) + parseInt(this.ee62) + parseInt(this.et31) + parseInt(this.a394) + parseInt(this.bb74) + parseInt(this.e441) + parseInt(this.ag01);
        return this.total
    },
    errorShake: function() {
        // 計算是否超過100並提醒
        if (this.total > 100) {
            return true
        }
        else {
            return false
        }
    },
    equal100: function() {
        // 計算是否超過100並提醒
        if (this.total === 100) {
            return true
        }
        else {
            return false
        }
    },
    selectComputed: function() {
        // 計算每個下拉式選單是否可以選
        const conditions = [this.e441, this.a394, this.ag01, this.ap15, this.bb74, this.ee62, this.et31, this.st07] ;
        const checkSelect = conditions.filter(i => i!=="0").length;
        if (checkSelect>=5){
            this.cannotSelect = true;
        }
        else {
            this.cannotSelect = false;
        }
        let selectStatus = [];
        for (var i = 0 ; i < conditions.length ; i++){
            if (conditions[i]==="0"&this.cannotSelect){
                selectStatus.push(true)
            }
            else{
                selectStatus.push(false)
            }
        }
        return selectStatus
    },
    SaveData: function() {
        const payload = {
                        "AP15": this.ap15,
                        "ST07": this.st07,
                        "EE62": this.ee62,
                        "ET31": this.et31,
                        "A394": this.a394,
                        "BB74": this.bb74,
                        "E441": this.e441,
                        "AG01": this.ag01
                    };
        this.$store.commit('step1', payload);
    }
  },
}

</script>
