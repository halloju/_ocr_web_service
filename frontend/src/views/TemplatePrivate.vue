<template>
  <div class="contentWrapper">
  <div class="contentWrapper1 py-5 ">
    <div class="my-content">
    </div>
  </div>
  <div class="contentWrapper2 py-5">
    <div class="my-content2">
      檢視模板訊息
    </div>
  </div>
  </div>
</template>

<style scoped>
.contentWrapper {
  display: flex;
  height: 80vh;
  justify-content: center;
}
.contentWrapper1{
  flex-grow:4;
  background-color: rgba(226, 230, 234, 0.3);
  height: 90vh;
  margin-top: 1.5vh;
  margin-bottom: 1.5vh;
  margin-left: 2vw;
  margin-right: 1vw;
  border-radius: 3vw 3vw 3vw 3vw;
}
.contentWrapper2{
  flex-grow:1;
  background-color: rgba(226, 230, 234, 0.3);
  height: 90vh;
  margin-top: 1.5vh;
  margin-bottom: 1.5vh;
  margin-left: 1vw;
  margin-right: 2vw;
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
  color: #008b8b;
}
.my-content2 {
  position: relative;
  text-align: center;
  top: 50%;
  width: 100%;
  height: 80vh;
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