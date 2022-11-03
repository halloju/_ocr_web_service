<template>
  <div class="step">
    Step 3. 標註要項位置
  </div>
  <div class="contentWrapper">
  <div class="contentWrapper1 py-5 ">
    <div class="bar">
      <span class="content-title">上傳圖片</span> &nbsp; <span class="content-subtitle">a.jpg</span>
    </div>
    <div class="my-content">
    </div>
  </div>
  <div class="contentWrapper2 py-5">
    <div class="bar">
      <span class="content-title">核取方塊位置</span>
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
    <router-link to="/define/step4" class="btn bg-orange">➡ 下一步</router-link>
  </div>
</template>

<style scoped>
.step {
  margin-top: 1.5vh;
  margin-left: 3vw;
  margin-right: 3vw;
  color: white;
  font-size: 21px;
  font-weight: bold;
}
.buttons {
  display: flex;
  justify-content: center;
  font-size: 1.5rem;
}
.buttons .config-button{
  background-color: #10A0A7;
  padding: 5px 20px;
  border-radius: 1vw 1vw 1vw 1vw;
  text-align: right;
  margin-right: 30px;
  color: white;
  font-size: 15px;
  font-weight: bold;
  height: 100%;
}
.buttons .next-button{
  background-color: #FF9B26;
  padding: 5px 20px;
  border-radius: 1vw 1vw 1vw 1vw;
  text-align: right;
  color: white;
  font-size: 15px;
  font-weight: bold;
}
.contentWrapper {
  display: flex;
  justify-content: center;
  height: 80vh;
  margin-top: 1vh;
  margin-bottom: 1vh;
  margin-left: 2vw;
  margin-right: 1vw;
}
.contentWrapper1{
  flex-grow:4;
  background-color: white;
  height: 100%;
  border-radius: 3vw 3vw 0vw 0vw;
  overflow: hidden;
}
.contentWrapper2{
  flex-grow:1;
  background-color: white;
  height: 100%;
  margin-left: 1.5vw;
  margin-right: 0.5vw;
  border-radius: 3vw 3vw 3vw 3vw;
}
.bar {
  background-color: white;
  margin-bottom: 20px;
  text-align: left;
}
.bar .content-title {
  margin-left: 30px;
  color: #008b8b;
  font-size: 1.3rem;
  font-weight: bold;
}
.bar .content-subtitle {
  color: grey;
  font-size: 1.1rem;
}
.my-content {
  width: 100%;
  height: 80vh;
  background-color: black;
  color: #008b8b;
}
.my-content2 {
  width: 100%;
  height: 50vh;
  color: #E2E6EA;
}
.my-content2 .my-table{
  background-color: #09747A;
  width: 80%;
  border-radius: 3vw 3vw 3vw 3vw;
  margin-left: 10%;
}
.my-content2 span {
  color: white;
  font-weight: bold;
}
.my-content2 .no {
  margin-left: 10%;
}
.my-content2 .ele-name{
  margin-left: 20%;
}
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