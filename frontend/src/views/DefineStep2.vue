<template>
  <div class="step">
    Step 2. 標註要項位置
  </div>
  <div class="contentWrapperFlex">

    <DropAnImage
      :isUploaded="false"
    />

  <div class="contentWrapper2 py-5">
    <div class="bar">
      <span class="content-title">文字辨識位置</span>
    </div>
    <div class="my-content2">
      <div class="my-table">
        <span class="no">No.</span>
        <span class="ele-name">要項名稱</span>
      </div>
    </div>
  </div>
  </div>
  <div class="buttons">
    <router-link to="/define/step3" class="btn bg-primary">➡ 下一步</router-link>
    <router-link to="" class="btn bg-orange btn-right">⬆ 上傳設定檔</router-link>
  </div>
</template>

<style scoped>
@import '@/assets/css/content.css';
</style>
<script>
import DropAnImage from '@/components/DropAnImage.vue'
export default {
  name: 'DefineStep2',
  components: {
    DropAnImage
  },
  data() {
    return {
      imageSource:sessionStorage.imageSource
    };
  },
  methods: {
    checkDrop(e){
      e.preventDefault()
    },
    
  }

};
</script>