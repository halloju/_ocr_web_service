<template>
  <Navbar />
  <div class="my-home">
      <!-- ======= Hero Section ======= -->
    <section id="hero" class="d-flex align-items-flex-start">
      <div class="container">
        <div class="row">
          <div class="col-lg-6 d-flex flex-column justify-content-center pt-4 pt-lg-0 order-2 order-lg-1" data-aos="fade-up" data-aos-delay="200">
            <h1>玉山智能辨識系統</h1>
            <h2>由智金處電腦視覺專家研發設計，解決行內 PDF、身份證、健保卡圖片辨識等問題</h2>
            <div class="d-flex justify-content-center justify-content-lg-start">
              <a href="#about" class="btn-get-started scrollto">立即體驗</a>
              </div>
          </div>
          <div class="col-lg-6 order-1 order-lg-2 hero-img" data-aos="zoom-in" data-aos-delay="200">
            <img src="@/assets/images/hero-img.png" class="img-fluid animated" alt="">
          </div>
        </div>
        
        <!-- Services -->
        <div class="row">

          <div class="section-title">
            <h2>Services</h2>
            <p>我們服務包含以下功能，可以提供您完整的光學字元辨識體驗，點選不同的功能體驗看看吧！</p>
          </div>

          <div class="col-xl-4 col-md-6 d-flex align-items-stretch mt-4 mt-md-0" data-aos="zoom-in" data-aos-delay="200">
            <div class="icon-box">
              <div class="icon"><i class="bx bx-file"></i></div>
              <h4><a href="">通用文件識別功能</a></h4>
              <p>產品功能敘述、產品功能敘述、產品功能敘述、產品功能敘述、產品功能敘述</p>
            </div>
          </div>

          <div class="col-xl-4 col-md-6 d-flex align-items-stretch mt-4 mt-xl-0" data-aos="zoom-in" data-aos-delay="300">
            <div class="icon-box">
              <div class="icon"><i class="bx bx-tachometer"></i></div>
              <h4><a href="">自定義模板</a></h4>
              <p>產品功能敘述、產品功能敘述、產品功能敘述、產品功能敘述、產品功能敘述</p>
            </div>
          </div>

          <div class="col-xl-4 col-md-6 d-flex align-items-stretch mt-4 mt-xl-0" data-aos="zoom-in" data-aos-delay="400">
            <div class="icon-box">
              <div class="icon"><i class="bx bx-layer"></i></div>
              <h4><a href="">特殊文件辨別功能</a></h4>
              <p>產品功能敘述、產品功能敘述、產品功能敘述、產品功能敘述、產品功能敘述</p>
            </div>
          </div>

        </div>
      </div>
 
    </section><!-- End Hero -->
    
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