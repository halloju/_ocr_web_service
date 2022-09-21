<template>
  <div class="d-lg-flex align-items-center justify-content-center my-3">
    <img src="../assets/images/main.svg" alt="" class="mx-5" />
    <div class="mx-5">
      <p class="color-primary mb-2">Fintech Taipei 期間限定</p>
      <h1 class="color-primary">智能投資健檢</h1>
      <p class="my-2">市場變動時，AI告訴您如何調整資產配置</p>
      <router-link to="/question" class="btn bg-primary mt-4" @click="home">立即體驗</router-link>
    </div>
  </div>
  <div class="notice container mt-5 p-4">
    <h4 class="mb-2">注意事項</h4>
    <p class="notice_content">
      以上所提供之分析資訊僅供參考，本行盡力提供正確模擬結果，但對其完整性、即時性和正確性不做任何擔保。任何人因信賴此等資料而做出或改變投資決策，應審慎衡量本身之需求及投資風險，並就投資結果自行負責。本行茲依據「個人資料保護法」及其他相關法令之規定，說明蒐集、處理、利用及國際傳輸申請人個人資料之管理方針，以及申請人所享有之權利或服務，詳依   玉山官網公告之「<span class="color-primary">個人資料運用法定告知事項</span>」及「<span class="color-primary">顧客資料保密措施聲明</span>」為準。
    </p>
  </div>
</template>

<style scoped>
@import '../assets/css/home.css';
</style>
<script>
export default {
  data() {
    return {

    };
  },
  methods: {
      home() {
          this.$store.commit('back');
      }
    }

};
</script>