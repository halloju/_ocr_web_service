<script>
export default {
  data() {
    return {

    }
  },
  mounted() {
    setTimeout(() => {
        this.$router.push({name:"Result"})
    }, 5000)
  }
}
</script>
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
                <li class="stepsName">
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
        <div class="container text-center py-5 px-5">
            <p class="color-primary fw-500 fs-20 mb-4">模型預測分析中，即將完成！</p>
            <img src="../assets/images/animation.gif" alt="" class="mw-1000 w-60"/>
        </div>
    </div>
</template>

<style scoped>
@import '../assets/css/form.css';
</style>
