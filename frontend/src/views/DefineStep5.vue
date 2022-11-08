<template>
  <div class="step">
    Step.5 資訊確認
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
          v-for="(rec, index) in recs_block"
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
    <div class="contentWrapperSub">
      <div class="contentWrapperSub1 py-5">
        <div class="bar">
          <span class="content-title">文字辨識位置</span>
          <img :src="open_eye"/>
          <img :src="close_eye"/>
        </div>
        <div class="my-content2-small">
          <div class="my-table">
            <span class="no">No.</span>
            <span class="ele-name">要項名稱</span>
          </div>
          <div v-for="(rec, index) in recs" class="card" style="width: 18rem;">
            <div class="card-body">
              <h4 class="card-subtitle mb-2 text-muted">id: {{ index }}</h4>
              <h5 class="card-title">x: {{ rec.startPointX }}, y: {{ rec.startPointY }}</h5>
              <h5 class="card-title">width: {{ rec.width }}, height: {{ rec.height }}</h5>
            </div>
          </div>
        </div>
      </div>
      <div class="contentWrapperSub2 py-5">
        <div class="bar">
          <span class="content-title">核取方塊辨識位置</span>
          <img :src="open_eye"/>
          <img :src="close_eye"/>
        </div>
        <div class="my-content2-small">
          <div class="my-table">
            <span class="no">No.</span>
            <span class="ele-name">要項名稱</span>
          </div>
          <div v-for="(rec, index) in recs_block" class="card" style="width: 18rem;">
            <div class="card-body">
              <h4 class="card-subtitle mb-2 text-muted">id: {{ index }}</h4>
              <h5 class="card-title">x: {{ rec.startPointX }}, y: {{ rec.startPointY }}</h5>
              <h5 class="card-title">width: {{ rec.width }}, height: {{ rec.height }}</h5>
            </div>
          </div>
        </div>
      </div>
      <div class="template-description">
        模板說明
        <br>
        <input value="e.g. Happy 名片">
      </div>
    </div>
    </div>
  </div>
  <div class="buttons">
    <button type="button" class="btn bg-secondary btn-right" data-bs-toggle="modal" data-bs-target="#exampleModal">取消</button>
    <button type="button" class="btn bg-primary btn-right" data-bs-toggle="modal" data-bs-target="#exampleModal">上傳</button>
  </div>
  <!-- Modal -->
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">標題文字</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">請確認</div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            關閉
          </button>
          <button type="button" class="btn btn-primary">確定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '@/assets/css/content.css';
</style>
<script>
const width = window.innerWidth/2;
const height = window.innerHeight/2;
import open_eye from '@/assets/images/open_eye.svg'
import close_eye from '@/assets/images/close_eye.svg'

export default {
  name: 'DefineStep5',
  mounted() {
    this.recs = JSON.parse(sessionStorage.getItem('recs'))? JSON.parse(sessionStorage.getItem('recs')): [];
    this.recs_block = JSON.parse(sessionStorage.getItem('recs_block'))? JSON.parse(sessionStorage.getItem('recs_block')): [];
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
      open_eye: open_eye,
      close_eye: close_eye,
      recs: [],
      recs_block: [],
      stageSize: {
        width: width,
        height: height,
      },
      image: null,
    };
  },
  methods: {

  }

};
</script>