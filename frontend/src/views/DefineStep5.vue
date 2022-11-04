<template>
  <div class="step">
    Step.5 資訊確認
  </div>
  <div class="contentWrapperFlex">
  <div class="contentWrapper1 py-5 ">
    <div class="bar">
      <span class="content-title">上傳圖片</span> &nbsp; <span class="content-subtitle">a.jpg</span>
    </div>
    <div class="my-content1">
    </div>
  </div>
  <div class="contentWrapperSub">
    <div class="contentWrapperSub1 py-5">
      <div class="bar">
        <span class="content-title">文字辨識位置</span>
      </div>
      <div class="my-content2-small">
        <div class="my-table">
          <span class="no">No.</span>
          <span class="ele-name">要項名稱</span>
        </div>
      </div>
    </div>
    <div class="contentWrapperSub2 py-5">
      <div class="bar">
        <span class="content-title">核取方塊辨識位置</span>
      </div>
      <div class="my-content2-small">
        <div class="my-table">
          <span class="no">No.</span>
          <span class="ele-name">要項名稱</span>
        </div>
      </div>
    </div>
    <div class="template-description">
      模板說明
      <br>
      <input value="e.g. Happy 名片">
    </div>
  </div>
  </div>
  <div class="buttons">
    <router-link to="" class="btn bg-primary">Cancel</router-link>
    <router-link to="" class="btn bg-orange btn-right">上傳</router-link>
  </div>
</template>

<style scoped>
@import '@/assets/css/content.css';
</style>
<script>
export default {
  name: 'DefineStep1',
  data() {
    return {

    };
  },
  methods: {
    }

};
</script>