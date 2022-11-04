<template>
  <div class="step">
    Step 1. 上傳範例圖片
  </div>
  <div class="contentWrapperBlock">
    <div class="my-content0">
      Click your browser or <br>
      drag and drop your files
    </div>
  </div>
  <div class="buttons">
    <router-link to="/define/step2" class="btn bg-primary">➡ 下一步</router-link>
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