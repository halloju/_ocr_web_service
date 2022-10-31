<template>
  <div class="contentWrapper">
  <div class="contentWrapper1 py-5 ">
    <div class="bar">
      <span class="content-title">上傳圖片</span> &nbsp; <span class="content-subtitle">a.jpg</span>
    </div>
    <div class="my-content">
    </div>
  </div>
  <div class="contentWrapperSub">
    <div class="contentWrapper3 py-5">
      <div class="bar">
        <span class="content-title">文字辨識位置</span>
      </div>
      <div class="my-content2">
      </div>
    </div>
    <div class="contentWrapper4 py-5">
      <div class="bar">
        <span class="content-title">核取方塊辨識位置</span>
      </div>
      <div class="my-content2">
      </div>
    </div>
    <div class="template-description">
      模板說明
      <br>
      <input value="e.g. Happy 名片">
    </div>
    <div class="buttons">
      <button class="config-button"> Cancel </button>
      <button class="next-button"> 上傳 </button>
    </div>
  </div>
  </div>
</template>

<style scoped>
.contentWrapper {
  display: flex;
  height: 100vh;
  justify-content: center;
}
.contentWrapper1{
  flex-grow:4;
  background-color: white;
  max-width: 100%;
  height: 90vh;
  margin-top: 1.5vh;
  margin-bottom: 1.5vh;
  margin-left: 2vw;
  margin-right: 1vw;
  border-radius: 3vw 3vw 3vw 3vw;
  padding: 0 0 0 0;
}
.contentWrapperSub{
  flex-grow:1;
}
.contentWrapper3{
  background-color: white;
  max-width: 100%;
  height: 30vh;
  margin-top: 1.5vh;
  margin-left: 2vw;
  margin-right: 1vw;
  border-radius: 3vw 3vw 3vw 3vw;
}
.contentWrapper4{
  background-color: white;
  max-width: 100%;
  height: 30vh;
  margin-top: 2vh;
  margin-bottom: 1.5vh;
  margin-left: 2vw;
  margin-right: 1vw;
  border-radius: 3vw 3vw 3vw 3vw;
  padding: 0 0;
}
.bar {
  background-color: white;
  margin-bottom: 20px;
  text-align: left;
}
.bar .content-title {
  margin-left: 30px;
  color: #008b8b;
  font-size: 17px;
  font-weight: bold;
}
.bar .content-subtitle {
  color: grey;
  font-size: 17px;
}
.my-content {
  width: 100%;
  height: 30vh;
  background-color: black;
  color: #008b8b;
}
.my-content2 {
  width: 100%;
  height: 30vh;
  color: #E2E6EA;
}
.template-description{
  color: white;
  font-weight: bold;
  margin-top: 3vh;
  margin-left: 3vw;
}
.template-description input{
  width: 20vw;
  margin-top: 3vh;
}
.buttons {
  text-align: left;
  margin-top: 3vh;
  margin-left: 3vw;
  max-width: 27vw;
}
.buttons .config-button{
  background-color: #10A0A7;
  padding: 5px 20px;
  border-radius: 1vw 1vw 1vw 1vw;
  margin-right: 1vw;
  text-align: left;
  color: white;
  font-size: 15px;
  font-weight: bold;
  height: 100%;
}
.buttons .next-button{
  background-color: #FF9B26;
  padding: 5px 20px;
  margin-left: 1vw;
  border-radius: 1vw 1vw 1vw 1vw;
  text-align: right;
  color: white;
  font-size: 15px;
  font-weight: bold;
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