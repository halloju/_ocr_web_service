<template>
  <div class="step">
    Step.4 編輯遮罩：遮住會變動區域
  </div>
  <div class="buttons">
    <button class="complete-button"><i class="fa fa-save">&nbsp;&nbsp;</i>完成</button>
  </div>
  <div class="contentWrapper">
  <div class="contentWrapper1 py-5 ">
    <div class="bar">
      <span class="content-title">上傳圖片</span> &nbsp; <span class="content-subtitle">a.jpg</span>
    </div>
    <div class="my-content">
    </div>
  </div>
  </div>
</template>

<style scoped>
.step {
  margin-top: 3vh;
  margin-left: 3vw;
  color: white;
  font-size: 21px;
  font-weight: bold;
}
.buttons {
  text-align: right;
  margin-right: 1vw;
}
.buttons .complete-button{
  background-color: #FF9B26;
  padding: 5px 25px;
  border-radius: 1vw 1vw 1vw 1vw;
  text-align: right;
  color: white;
  font-size: 15px;
  font-weight: bold;
}
.buttons .fa {
  color: white;
  font-size: 17px;
  font-weight: 600;
}
.contentWrapper {
  display: flex;
  height: 80vh;
  justify-content: flex-start;
}
.contentWrapper1{
  flex:auto;
  background-color: white;
  height: 80vh;
  margin-top: 1.5vh;
  margin-bottom: 1.5vh;
  margin-left: 2vw;
  margin-right: 1vw;
  border-radius: 3vw 3vw 0vw 0vw;
  overflow: hidden;
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
  height: 75vh;
  background-color: black;
  color: #008b8b;
}
.my-content2 {
  width: 100%;
  height: 50vh;
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