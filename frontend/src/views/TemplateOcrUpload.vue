<template>
  <div class="step">
    單張或多張圖片上傳
  </div>
  <div class="contentWrapperFlex">
    <div class="contentWrapper5 py-5 ">
    </div>
    <div class="contentWrapperSubFull">
      <div class="contentWrapperSub1 py-5">
        <div class="bar">
          <span class="content-title">辨識設定</span>
        </div>
        <div class="my-content3-small">
          <div class="content-item">
            選擇語言
          </div>
          <select class="select-item">
            <option>請選擇辨識語言</option>
            <option>英語</option>
            <option>繁體中文</option>
            <option>日文</option>
          </select>
          <div class="content-item">
            選擇模板
          </div>
          <select class="select-item">
              <option>請選擇辨識模板</option>
              <option>Template 1</option>
              <option>Template 2</option>
              <option>Template 3</option>
          </select>
          <div class="content-item">
            <input type="checkbox"> 使用高精度模型(耗時較久)
          </div>
        </div>
      </div>
      <div class="contentWrapperSub2">
        <div class="bar">
          <span class="content-title">上傳資訊</span>
        </div>
        <div class="content-item">本次上傳總份數： 1 份 </div>
        <div class="content-item">本次上傳大小： 50 MB </div>
        <div class="content-item">已上傳總份數： 50 份 </div>
        <div class="content-item">已上傳大小： 50 MB </div>
        <div class="content-item">上傳剩餘容量： 450 MB </div>
      </div>
    </div>
  </div>
  <div class="buttons">
      <router-link to="" class="btn bg-primary">辨識</router-link>
  </div>
</template>

<style scoped>
@import '@/assets/css/content.css';
@import '@/assets/css/template.css';
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