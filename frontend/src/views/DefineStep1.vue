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
  margin-top: 50px;
  margin-left: 50px;
  color: white;
  font-size: 21px;
  font-weight: bold;
}
.contentWrapper{
  display: block;
  background-color: rgba(0, 0, 0, 0.1);
  max-width: 95%;
  height: 600px;
  margin-top: 100px;
  margin-bottom: 30px;
  margin-left: 30px;
  margin-right: 30px;
  border-radius: 30px 30px 30px 30px;
  padding: 0 0 0 0;
}
.bar {
  margin-left: 40%;
  margin-bottom: 20px;
  text-align: center;
}
.bar button {
  background-color: black;
  border-radius: 30px 30px 30px 30px;
  border: 5px solid white;
  font-weight: bold;

}
.my-content {
  width: 100%;
  height: 450px;
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