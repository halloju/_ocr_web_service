<template>
  <div class="step">
    Step.3 標註要向位置
  </div>
  <div class="buttons">
    <button class="next-button">➡ 下一步</button>
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
      <span class="content-title">核取方塊辨識位置</span>
    </div>
    <div class="my-content2">
    </div>
  </div>
  </div>
</template>

<style scoped>
.step {
  margin-top: 50px;
  margin-left: 50px;
  color: white;
  font-size: 21px;
  font-weight: bold;
}
.buttons {
  text-align: right;
  margin-right: 50px;
}
.buttons .next-button{
  background-color: #FF9B26;
  padding: 5px 20px;
  border-radius: 10px 10px 10px 10px;
  text-align: right;
  color: white;
  font-size: 15px;
  font-weight: bold;
}
.contentWrapper {
  display: flex;

  justify-content: center;
}
.contentWrapper1{
  flex-grow:4;
  background-color: white;
  max-width: 100%;
  height: 750px;
  margin-top: 25px;
  margin-bottom: 30px;
  margin-left: 30px;
  margin-right: 30px;
  border-radius: 30px 30px 30px 30px;
  padding: 0 0 0 0;
}
.contentWrapper2{
  flex-grow:1;
  background-color: white;
  max-width: 100%;
  height: 750px;
  margin-top: 25px;
  margin-bottom: 30px;
  margin-left: 30px;
  margin-right: 30px;
  border-radius: 30px 30px 30px 30px;
  padding: 0 0 0 0;
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
  height: 600px;
  background-color: black;
  color: #008b8b;
}
.my-content2 {
  width: 100%;
  height: 600px;
  color: #E2E6EA;
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