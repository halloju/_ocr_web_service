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
                <li class="stepsName todo">
                    <div class="stepsNum">3</div>
                    <div class="stepsTxt">市場事件</div>
                </li>
                <li class="stepsName todo">
                    <div class="stepsNum">4</div>
                    <div class="stepsTxt">AI模型運算</div>
                </li>
                <li class="stepsName">
                    <div class="stepsNum">5</div>
                    <div class="stepsTxt">資產配置健檢</div>
                </li>
            </ul>
        </div>
        <!-- steps -->
        <div class="contentWrapper container py-5 px-5">
            <form class="fillData_form">
                <p class="form-grop-title py-1 fs-20 fw-500 color-primary mb-4">您的資產配置健檢結果</p>
                <p class="mb-4">親愛的顧客您好，依據您所預設的資產配置，在遇到<span class="color-primary">帶入顧客選擇情境</span>時，提供您因應市場變化的資產配置建議如下：</p>
                <!-- 市場展望 -->
                <div class="row mt-5 mb-2">
                    <div class="col-md-12 pb-1">
                        <p class="color-primary">市場展望</p>
                    </div>
                </div>
                <!-- 整體市場評論 -->
                <div class="row pt-2 pb-4">
                    <div class="col-md-2 pb-1">
                        <label for="" class="input_label">整體市場評論</label>
                    </div>
                    <div class="col-md-10 pb-1 d-flex">
                        <p class="confirmText">{{macro_market}}</p>
                    </div>
                </div>
                <!-- 各個股票 -->
                <div class="row pt-2 pb-4" v-for="(key, val) in market_des">
                    <div class="col-md-2 pb-1">
                        <label for="" class="input_label">{{val}}</label>
                    </div>
                    <div class="col-md-10 pb-1 d-flex">
                        <p class="confirmText">{{key}}</p>
                    </div>
                </div>
                 <!-- 投資組合資產配置說明 -->
                <div class="row mt-5 mb-2">
                    <div class="col-md-12 pb-1">
                        <p class="color-primary">投資組合資產配置說明</p>
                    </div>
                </div>
                <div class="row mt-3 mb-2">
                    <div class="col-md-12 pb-1">
                        <table class="greenHead">
                            <thead>
                                <tr>
                                    <th>資產類型</th>
                                    <th>股票類/國家</th>
                                    <th>股票類/產業</th>
                                    <th>債券類/國家</th>
                                    <th>債券類/信評</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>{{allocation["原投組問題說明_SAA資產類型"][0]}}</td>
                                    <td>{{allocation["原投組問題說明_SAA股國家"][0]}}</td>
                                    <td>{{allocation["原投組問題說明_SAA股產業"][0]}}</td>
                                    <td>{{allocation["原投組問題說明_SAA債國家"][0]}}</td>
                                    <td>{{allocation["原投組問題說明_SAA債信評"][0]}}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="row mt-5 mb-2">
                    <div class="col-md-6 pb-1">
                        <p class="color-primary mb-2">投資組合資產類型分布</p>
                        <Bar class="px-3"
                            :chart-options="chartOptions"
                            :chart-data="chartData"
                            :chart-id="chartId"
                            :dataset-id-key="datasetIdKey"
                            :plugins="plugins"
                            :css-classes="cssClasses"
                            :styles="styles"
                            :width="width"
                            :height="height"
                        />
                    </div>
                    <div class="col-md-6 pb-1">
                        <p class="color-primary mb-2">投資組合波動度風險</p>
                        <Bar class="px-3"
                            :chart-options="chartOptions"
                            :chart-data="chartData2"
                            :chart-id="chartId"
                            :dataset-id-key="datasetIdKey"
                            :plugins="plugins"
                            :css-classes="cssClasses"
                            :styles="styles"
                            :width="width"
                            :height="height"
                        />
                    </div>
                </div>
                <!-- 資產配置明細表 -->
                <div class="row mt-5 mb-2">
                    <div class="col-md-12 pb-1">
                        <p class="color-primary">資產配置明細表</p>
                    </div>
                </div>
                <div class="row mt-3 mb-2">
                    <div class="col-md-12 pb-1">
                        <table class="greenHead">
                            <thead>
                                <tr>
                                    <th rowspan="2">狀態</th>
                                    <th rowspan="2">調整建議</th>
                                    <th rowspan="2">產品名稱</th>
                                    <th rowspan="2">調整折台金額(元)</th>
                                    <th colspan="2">調整佔比(%)</th>
                                    <th colspan="5">資產配置問題影響</th>
                                </tr>
                                <tr>
                                    <th>目前配置</th>
                                    <th>建議配置</th>
                                    <th>資產類型</th>
                                    <th>股票類/國家</th>
                                    <th>股票類/產業</th>
                                    <th>債券類/國家</th>
                                    <th>債券類/信評</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in tableData">
                                    <td class="text-center" style="width: 60px">{{item['標的狀態']}}</td>
                                    <td class="text-center" style="width: 75px">{{item['調整建議']}}</td>
                                    <td>{{item['產品名稱']}}<br><small>(本基金得投資於非投資等級之高風險債券基金且配息來源可能為本金)</small></td>
                                    <td class="text-right">{{item['調整金額(折台)']}}</td>
                                    <td class="text-right">{{item['目前投資佔比']}}</td>
                                    <td class="text-right">{{item['目標金額佔比']}}</td>
                                    <td>{{item['投組問題說明_SAA資產類型']}}</td>
                                    <td>{{item['投組問題說明_SAA股國家']}}</td>
                                    <td>{{item['投組問題說明_SAA股產業']}}</td>
                                    <td>{{item['投組問題說明_SAA債國家']}}</td>
                                    <td>{{item['投組問題說明_SAA債信評']}}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </form>
            <div class="d-flex justify-content-center">
                <router-link to="/quiz" class="btn bg-primary mt-4">前往有獎徵答</router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>
@import '../assets/css/form.css';
@import '../assets/css/table.css';
</style>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, registerables } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
ChartJS.register(...registerables);
ChartJS.register(ChartDataLabels);

export default {
  name: 'BarChart',
  components: { Bar },
  props: {
    chartId: {
      type: String,
      default: 'bar-chart'
    },
    datasetIdKey: {
      type: String,
      default: 'label'
    },
    width: {
      type: Number,
      default: 400
    },
    height: {
      type: Number,
      default: 220
    },
    cssClasses: {
      default: '',
      type: String
    },
    styles: {
      type: Object,
      default: () => {}
    },
    plugins: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      macro_market: this.$store.state.response["macro_market"],
      market_des: this.$store.state.response["market_des"],
      allocation: this.$store.state.response["allocation"],
      asset_type: this.$store.state.response["asset_type"],
      fluctuation: this.$store.state.response["fluctuation"],
      detail: this.$store.state.response["detail"],
      chartOptions: {
        responsive: true,
        scales: {
            y: {
                ticks: {
                    format: {
                        style: 'percent'
                    }
                }
            }
        },
      }
    }
  },
  computed: {
    chartData: function(){
        return {
        labels: [
            '股票類',
            '債券類',
            '流動資產',
            '特殊類',
        ],
        datasets: [
            {
                label: '建議區間',
                backgroundColor: '#D3D3D3',
                data: [[this.asset_type['lower_stock'][0], this.asset_type['upper_stock'][0]], [ this.asset_type['lower_bond'][0], this.asset_type['upper_bond'][0]], [ this.asset_type['lower_money'][0], this.asset_type['upper_money'][0]], [this.asset_type['lower_other'][0], this.asset_type['upper_other'][0]]],
                type: 'bar',
                order: 2,
                datalabels: {
                    display: false,
                }
            },
            {
                label: '目前',
                data: [this.asset_type['原投組配置_股票類'][0], this.asset_type['原投組配置_債券類'][0], this.asset_type['原投組配置_流動資產'][0], this.asset_type['原投組配置_特殊類'][0]],
                backgroundColor: '#F28500',
                fill: false,
                type: 'line',
                pointStyle: 'circle',
                pointRadius: 5,
                showLine: false, //<- set this
                order: 1,
                datalabels: {
                    color: '#F28500',
                    formatter: function(value, context) {
                        return Math.round(value*100) + '%';
                    },
                    anchor: 'center',
                    align: 'left',
                }
            },
            {
                label: '建議配置',
                data: [this.asset_type['新投組配置_股票類'][0], this.asset_type['新投組配置_債券類'][0], this.asset_type['新投組配置_流動資產'][0], this.asset_type['新投組配置_特殊類'][0]],
                backgroundColor: '#00A19B',
                fill: false,
                type: 'line',
                pointStyle: 'circle',
                pointRadius: 5,
                showLine: false, //<- set this
                order: 0,
                datalabels: {
                    color: '#00A19B',
                    formatter: function(value, context) {
                        return Math.round(value*100) + '%';
                    },
                    anchor: 'center ',
                    align: 'left',
                }
            }
        ],
      }
    },
    chartData2: function() {
        return {
        labels: [
            '投資組合波動度',
        ],
        datasets: [
            {
                label: '建議區間',
                backgroundColor: '#D3D3D3',
                data: [[this.fluctuation['lower'], this.fluctuation['upper']]],
                type: 'bar',
                order: 2,
                datalabels: {
                    display: false,
                },
            },
            {
                label: '目前',
                data: [this.fluctuation['原投組_投組波動度'][0]],
                backgroundColor: '#F28500',
                fill: false,
                type: 'line',
                pointStyle: 'circle',
                pointRadius: 5,
                showLine: false, //<- set this
                order: 1,
                datalabels: {
                    color: '#F28500',
                    formatter: function(value, context) {
                        return Math.round(value*100) + '%';
                    },
                    anchor: 'center',
                    align: 'left',
                }
            },
            {
                label: '建議配置',
                data: [this.fluctuation['新投組_投組波動度'][0]],
                backgroundColor: '#00A19B',
                fill: false,
                type: 'line',
                pointStyle: 'circle',
                pointRadius: 5,
                showLine: false, //<- set this
                order: 0,
                datalabels: {
                    color: '#00A19B',
                    formatter: function(value, context) {
                        return Math.round(value*100) + '%';
                    },
                    anchor: 'center',
                    align: 'left',
                }
            }
        ],
      }
    },
    tableData: function() {
        let myData = [];
        for (var i = 0 ; i < 4; i++){
            let temp = {}
            temp["標的狀態"] = this.detail["標的狀態"][i];
            temp["調整建議"] = this.detail["調整建議"][i];
            temp["產品名稱"] = this.detail["產品名稱"][i] ;
            temp["調整金額(折台)"] = this.detail["調整金額(折台)"][i];
            temp["目前投資佔比"] = this.detail["目前投資佔比"][i];
            temp["目標金額佔比"] = this.detail["目標金額佔比"][i];
            temp["投組問題說明_SAA資產類型"] = this.detail["投組問題說明_SAA資產類型"][i];
            temp["投組問題說明_SAA股國家"] = this.detail["投組問題說明_SAA股國家"][i];
            temp["投組問題說明_SAA股產業"] = this.detail["投組問題說明_SAA股產業"][i];
            temp["投組問題說明_SAA債國家"] = this.detail["投組問題說明_SAA債國家"][i];
            temp["投組問題說明_SAA債信評"] = this.detail["投組問題說明_SAA債信評"][i];
            myData.push(temp)
        }
        return myData
    }
  }
}
</script>