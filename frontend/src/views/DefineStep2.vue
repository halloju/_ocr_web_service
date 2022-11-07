<template>
  <div class="step">
    Step 2. 標註要項位置
  </div>
  <div class="contentWrapperFlex">
    <div class="contentWrapperBlock py-5">
      <v-stage
      ref="stage"
      :config="stageSize"
      @mousemove="handleMouseMove"
      @mouseDown="handleMouseDown"
      @mouseUp="handleMouseUp"
      >
      <v-layer ref="dragLayer">
        <v-image
            :config="{
              image: image,
              x: 0,
              y: 0,
              width: stageSize.width,
              height: stageSize.height,
            }"
        />
      </v-layer>
      <v-layer ref="layer">
        <v-rect
          v-for="(rec, index) in recs"
          :key="index"
          :config="{
            x: Math.min(rec.startPointX, rec.startPointX + rec.width),
            y: Math.min(rec.startPointY, rec.startPointY + rec.height),
            width: Math.abs(rec.width),
            height: Math.abs(rec.height),
            fill: 'rgb(0,0,0,0)',
            stroke: 'black',
            strokeWidth: 3,
          }"
        />
      </v-layer>
    </v-stage>
    </div>
    
    <div class="contentWrapper2 py-5">
      <div class="bar">
        <span class="content-title">文字辨識位置</span>
      </div>
      <div class="my-content2">
        <div class="my-table">
          <span class="no">No.</span>
          <span class="ele-name">要項名稱</span>
        </div>
        <div v-for="(rec, index) in recs" class="card" style="width: 18rem;">
          <div class="card-body">
            <h4 class="card-subtitle mb-2 text-muted">id: {{ index }}</h4>
            <h5 class="card-title">x: {{ rec.startPointX }}, y: {{ rec.startPointY }}</h5>
            <h5 class="card-title">width: {{ rec.width }}, height: {{ rec.height }}</h5>
            <button type="button" class="btn btn-primary btn-sm" @click="deleteRec(index)">刪除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="buttons">
    <router-link to="/define/step3" class="btn bg-primary">➡ 下一步</router-link>
    <router-link to="" class="btn bg-orange btn-right">⬆ 上傳設定檔</router-link>
  </div>
</template>

<style scoped>
@import '@/assets/css/content.css';
</style>

<script>
const width = window.innerWidth/2;
const height = window.innerHeight/2;

export default {
  name: 'DefineStep2',
  components: {
  },
  mounted() {
    this.image = new window.Image();
    this.image.src = sessionStorage.imageSource;
    this.image.onload = () => {
      this.stageSize = {
        width: width,
        height: height,
      };
    };
  },
  data() {
    return {
      stageSize: {
        width: width,
        height: height,
      },
      image: null,
      text: "Try to draw a rectangle",
      lines: [],
      isDrawing: false,
      recs: [],
    };
  },
  methods: {
    handleMouseDown(event) {
      this.isDrawing = true;
      const pos = this.$refs.stage.getNode().getPointerPosition();
      this.setRecs([
        ...this.recs,
        { startPointX: pos.x, startPointY: pos.y, width: 0, height: 0 },
      ]);
    },
    handleMouseUp() {
      this.isDrawing = false;
    },
    setRecs(element) {
      this.recs = element;
    },
    handleMouseMove(event) {
      // no drawing - skipping
      if (!this.isDrawing) {
        return;
      }
      // console.log(event);
      const point = this.$refs.stage.getNode().getPointerPosition();
      // handle  rectangle part
      let curRec = this.recs[this.recs.length - 1];
      curRec.width = point.x - curRec.startPointX;
      curRec.height = point.y - curRec.startPointY;
    },
    deleteRec(index) {
      this.recs.splice(index, 1);
    },
  },
};
</script>