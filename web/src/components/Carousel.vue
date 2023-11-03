<script >
import { ref } from 'vue';
export default {
  name: 'Carousel',
  props: {
    contents: {
      type: String,
    },
    title: {
      type: String,
    }
  },
  setup(props) {
    const dialogVisible = ref(true);
    return {
      dialogVisible,
      fullContent: props.contents,
      selfTitle: props.title,
    };
  }
};
</script>

<template>
  <div class="Dialog">
    <el-dialog v-model="dialogVisible" center :fullscreen="false" width="50%" :close-on-click-modal="true" top="30vh"
      :close-on-press-escape="true" :show-close="true" class="agreement-dialog">
      <el-carousel :interval="5000" arrow="always">
        <el-carousel-item v-for="item in 4" :key="item">
          <h3 text="2xl" justify="center">{{ item }}</h3>
        </el-carousel-item>
      </el-carousel>
      <div class="dialog-footer">
      <button  class="uiStyle btnGreen sizeS relative" @click="dialogVisible = false">
          取消
        </button>
      </div>
    </el-dialog>
  </div>
</template>



<style scoped>

.dialog-center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 16px;
}

.box-card {
  width: 80%;

}

.card-header {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.card_body {
  margin: 10px;
  height: 50vh;
  overflow-y: scroll;
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
  text-align: center;
}
.dialog-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.el-dialog {
  background-color: rgba(0, 0, 0) !important;
}
</style>