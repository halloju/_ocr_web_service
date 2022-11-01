<template>
  <div class="my-home">
    <div class="introductionWrapper">
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
        <button class="start-button">開始使用</button>
      </div>
      <div class="feature-title">
        Our Services
      </div>
      <div class="productWrapper">
        <div class="feature1">
          <img src="@/assets/images/feature1-black.svg" class="feature-icon"/>
          <p class="feature-sub">通用文件辨識功能</p>
          <div>
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 1</span>
          </div>
          <div>
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 2</span>
          </div>
          <div>
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 3</span>
          </div>
        </div>
        <div class="feature2">
          <img src="@/assets/images/feature2-black.svg" class="feature-icon"/>
          <p class="feature-sub">自定義模板</p>
          <div>
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 1</span>
          </div>
          <div>
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 2</span>
          </div>
          <div>
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 3</span>
          </div>
        </div>
        <div class="feature3">
          <img src="@/assets/images/feature3-black.svg" class="feature-icon"/>
          <p class="feature-sub">特殊文件辨別功能</p>
          <div>
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 1</span>
          </div>
          <div>
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 2</span>
          </div>
          <div>
            <img src="@/assets/images/tick.svg" class="tick-icon">
            <span class="feature-content">產品特色 3</span>
          </div>
        </div>
      </div>  
    </div> 
  </div>
</template>

<style scoped>
.my-home {
    background: url('@/assets/images/dashborad-bg.svg') no-repeat;
    background-size: 130%;
    background-position: bottom;
    background-color: #09747A;
    border-radius: 0px;
    height: 100vh;
}
.home-logo {
  text-align: center;
}
.home-logo img{
  width: 30vw;
  height: 10vh;
  text-align: center;
  margin-top: 2vh;
}
.sub-title {
  font-size: 1.5rem;
  text-align: center;
  margin-top: 2vh;
  color: white;
}
.title {
  font-size: 3rem;
  text-align: center;
  margin-top: 1vh;
  color: white;
}
.buttons {
  text-align: center;
  margin-right: 1vw;
}
.buttons .start-button{
  background-image: linear-gradient(155deg,#F79E0E, #EEBD23);
  padding: 15px 50px;
  border-radius: 0.5vw 0.5vw 0.5vw 0.5vw;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  margin-top: 1vw;
  border: none;
}
.feature-title {
  font-weight: bold;
  font-size: 1.5rem;
  color: #F79E0E;
  text-align: center;
  margin-top: 1.5vw;
  margin-bottom: 1.5vw;
}
.productWrapper {
  display: flex;
  justify-content: space-around;
}
.productWrapper .feature1,.feature2,.feature3{
  background-color: white;
  height: 45vh;
  width: 25vw;
  max-width: 350px;
  border-radius: 2vw 2vw 2vw 2vw;
  text-align: center;
}
.productWrapper .feature-icon {
  margin-top: 5vh;
  width: 6vw;
}
.productWrapper .feature-sub {
  margin-top: 5vh;
  margin-bottom: 3vh;
  color: #E1A325;
  font-weight: bold;
  font-size: 1.5rem;
}
.productWrapper .tick-icon {
  margin-right: 2vw;
}
.productWrapper span {
  font-weight: 500;
  font-size: 1.2rem;
  color: #11482E;
}
</style>
<script>
export default {
  name: 'Home',
  data() {
    return {

    };
  },
  methods: {
    }

};
</script>