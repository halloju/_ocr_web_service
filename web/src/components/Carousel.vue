<script >
import { ref, watch } from 'vue';
export default {
  name: 'Carousel',
  props: {
    contents: {
      type: String,
    },
    title: {
      type: String,
    },
    show :{
      type: Boolean
    }
  },
  setup(props) {
    const dialogVisible = ref(props.show);
    watch(() => props.show, (newShowValue) => {
      dialogVisible.value = newShowValue;
    });
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
      <el-carousel  arrow="always" :autoplay="false">
        <el-carousel-item v-for="item in 4" :key="item">
          <p class="pop-header">標題 </p>
          <div class="MessageContainer">
            
            <p  justify="center">{{ item }}</p>
          </div>
        </el-carousel-item>
      </el-carousel>
      <div class="dialog-footer">
        <button  class="uiStyle btnDarkBlue sizeM relative" @click="dialogVisible = false">
          略過
        </button>
      </div>
    </el-dialog>
  </div>
</template>



<style scoped>

.Dialog ::v-deep .el-dialog {
  border-radius: 10px;
	box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
	-webkit-box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
	-moz-box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
	-ms-box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
	-o-box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
	margin: 100px auto;
	width: 60%;
	max-width: 960px;
	min-width: 860px;
}


.dialog-center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 16px;
}

.MessageContainer {
	padding: 10px 60px 60px;
	text-align: center;
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

.pop-header {
	font-size: 22px;
	font-weight: bold;
	color: #3c4c5e;
	text-align: center;
}
</style>