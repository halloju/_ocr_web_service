<template>
  <div class="step">
    Step 4. 編輯遮罩：遮住會變動區域
  </div>
  <div class="contentWrapperFlex">
  <div class="contentWrapper1 py-5 ">
    <div class="bar">
      <span class="content-title">上傳圖片</span> &nbsp; <span class="content-subtitle">a.jpg</span>
    </div>
    <div class="my-content1">
    </div>
  </div>
  </div>
  <div class="buttons">
    <router-link to="/define/step5" class="btn bg-primary"><i class="fa fa-save">&nbsp;&nbsp;</i>完成</router-link>
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