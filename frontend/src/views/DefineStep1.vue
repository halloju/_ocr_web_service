<template>
  <div class="step">
    Step.1 上傳範例圖片
  </div>
  <div class="contentWrapper py-5 px-4">
    <div class="bar">
      <button class="btn"> New Upload </button>
    </div>
    <div class="my-content">
      Click your browser or <br>
      drag and drop your files
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
.contentWrapper{
  display: block;
  background-color: rgba(0, 0, 0, 0.1);
  max-width: 95%;
  height: 80vh;
  margin-top: 3vh;
  margin-bottom: 10%;
  margin-left: 3vw;
  margin-right: 3vw;
  border-radius: 3vw 3vw 3vw 3vw;
}
.bar {
  margin-left: 25vw;
  margin-bottom: 2vh;
}
.bar button {
  background-color: black;
  border-radius: 3vw 3vw 3vw 3vw;
  border: 5px solid white;
  font-weight: bold;
  text-align: center;

}
.my-content {
  width: 100%;
  height: 60vh;
  background-color: rgba(16,160,167, 0.5);
  padding: 0 0 0 0;
  color: #E2E6EA;
  font-size: 25px;
  display: flex;
  justify-content: center;
  align-items: center; 

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