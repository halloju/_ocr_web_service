<template>
  <div class="step">
    Step 1. 上傳範例圖片
  </div>
  <div class="contentWrapper py-5 px-4">
    <div class="my-content">
      Click your browser or <br>
      drag and drop your files
    </div>
  </div>
  <div class="buttons">
    <router-link to="/define/step2" class="btn bg-orange">➡ 下一步</router-link>
  </div>
</template>

<style scoped>
.step {
  margin-top: 1.5vh;
  margin-left: 3vw;
  color: white;
  font-size: 21px;
  font-weight: bold;
}
.buttons {
  display: flex;
  justify-content: center;
  font-size: 1.5rem;
}
.contentWrapper{
  display: block;
  background-color: rgba(226, 230, 234, 0.3);
  max-width: 95%;
  height: 80vh;
  margin-top: 1vh;
  margin-bottom: 1vh;
  margin-left: 2vw;
  margin-right: 2vw;
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
  height: 70vh;
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