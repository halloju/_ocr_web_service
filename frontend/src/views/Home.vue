<template>
  <Navbar />
  <div class="my-home">
      <div class="home-logo">
        <img src="@/assets/images/esun-ocr-logo.svg" alt="logo">
      </div>
      <div class="sub-title">
        由智金處研究開發
      </div>
      <div class="title">
        一款專屬玉山場景的辨識工具
      </div>
      <div class="buttons">
        <button class="start-button">開始體驗</button>
      </div>
      <div class="feature-title">
        Our Services
      </div>
      <div class="productWrapper">
        <div class="feature1">
          <div class="product-content">
            <img src="@/assets/images/feature1-black.svg" class="feature-icon"/>
          </div>
          <div class="product-content">
            <p class="feature-sub">通用文件辨識功能</p>
          </div>
          <div class="product-content">
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 1</span>
          </div>
          <div class="product-content">
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 2</span>
          </div>
          <div class="product-content">
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 3</span>
          </div>
        </div>
        <div class="feature2">
          <div class="product-content">
            <img src="@/assets/images/feature2-black.svg" class="feature-icon"/>
          </div>
          <div class="product-content">
            <p class="feature-sub">自定義模板</p>
          </div>
          <div class="product-content">
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 1</span>
          </div>
          <div class="product-content">
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 2</span>
          </div>
          <div class="product-content">
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 3</span>
          </div>
        </div>
        <div class="feature3">
          <div class="product-content">
            <img src="@/assets/images/feature3-black.svg" class="feature-icon"/>
          </div>
          <div class="product-content">
            <p class="feature-sub">特殊文件辨別功能</p>
          </div>
          <div class="product-content">
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 1</span>
          </div>
          <div class="product-content">
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 2</span>
          </div>
          <div class="product-content">
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 3</span>
          </div>
        </div>
      </div>
  </div>
</template>

<style scoped>
@import '@/assets/css/home.css';
</style>
<script>
import Navbar from '../components/Navbar.vue'
export default {
  components: {
    Navbar
  },
  name: 'Home',
  data() {
    return {

    };
  },
  methods: {
    }

};
</script>