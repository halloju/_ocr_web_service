<template>
  <div class="" ref="img_block">
  <form v-if="isInputing">
    <div class="form-group" >
      <h5>方框命名</h5>
      <input class="form-control" type="text" placeholder="請命名" ref="rec_name">
    </div>
    <br>
    <Button label=" 確定" class="pi pi-check p-button-success" @click="setRecName" v-tooltip="'請框好圖片後點擊'" style="width: 12em; height: 4em;"></Button>
  </form>
  <v-stage
  ref="stage"
  
  :config="stageConfig"
  @mousemove="handleMouseMove"
  @mouseDown="handleMouseDown"
  @mouseUp="handleMouseUp"
  @wheel="wheelForScale($event)"
  >
    <v-layer ref="layer">
      <v-image
          :config="{
            width: this.imageConfig.width,
            height: this.imageConfig.height,
            image: this.image,
            opacity: this.imageConfig.opacity,
            x: this.imageConfig.x,
            y: this.imageConfig.y,
          }" ref="image"
      />
      <Rect v-if="canDraw"
        :boxName="boxName"
        :fillColor="fillColor"
      />
      <Rect v-else v-for="box in otherBoxes"
        :key="box.boxName"
        :boxName="box.boxName"
        :fillColor="box.fillColor"
      />
      <v-transformer ref="transformer" />
    </v-layer>
  </v-stage>
  </div>
  <div class="flex flex-wrap gap-2">
    <Button icon="pi pi-search-plus" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'放大圖片'" @click="photoPlus" />
    <Button icon="pi pi-search-minus" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'縮小圖片'" @click="photoMinus" />
    <Button icon="pi pi-undo" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'還原圖片大小'" @click="resetSize" />
  </div>
  
</template>

<style scope>
@import '@/assets/css/content.css';
</style>

<script>
import Rect from '@/components/Rect.vue'
const ratio = 1;
const innerWidth = window.innerWidth;
const innerHeight = window.innerHeight;

export default {
  name: 'Box',
  mounted(){
    this.image = new window.Image();
    this.image.src = sessionStorage.imageSource;
    const resize = Math.min(this.$refs.img_block.clientWidth/this.image.width, this.$refs.img_block.clientHeight/this.image.height);
    this.image.onload = () => {
      this.imageConfig = {
        width: this.image.width * resize * ratio,
        height: this.image.height * resize * ratio,
        x: (this.$refs.img_block.clientWidth - this.image.width * resize * ratio) / 2,
        y: (this.$refs.img_block.clientHeight - this.image.height * resize * ratio) / 2,
      }
    };
    this.recs = this.$store.state[this.boxName];
  },
  components: {
    Rect,
  },
  data(){
    return {
      recs: [],
      image: null,
      stageConfig: {
        x: 0,
        y: 0,
        width: innerWidth,
        height: innerHeight,
      },
      imageConfig: {
        width: null,
        height: null,
        x: 10,
        y: 20,
      },
      isDrawing: false,
      isInputing: false,
      isTransforming: false,
    };
  },
  computed:{
  },
  methods:{
    handleMouseDown(event) {
      if (!this.canDraw) return;
      if (event.target === event.target.getStage()) return;
      if (this.isTransforming & event.target.className === 'Image') {
            this.selectedShapeName = '';
            this.updateTransformer();
            this.isTransforming = false;
            return;
          }

      // transform rect    
      if (event.target.className === 'Rect') {
          this.isTransforming = true;

          // // clicked on transformer - do nothing
          const clickedOnTransformer =
            event.target.getParent().className === 'Transformer';
          if (clickedOnTransformer) {
            return;
          }

          // find clicked rect by its name
          const name = event.target.name();
          console.log(name)
          const rect = this.recs.find((r) => r.name === name);
          if (rect) {
            this.selectedShapeName = name;
          } else {
            this.selectedShapeName = '';
          }
          this.updateTransformer();
          return;
      }

      // draw rect
      this.isDrawing = true;
      const pos = this.$refs.stage.getNode().getPointerPosition();
      this.setRecs([
        ...this.recs,
        { startPointX: pos.x, startPointY: pos.y, width: 0, height: 0 },
      ]);
      this.$store.state[this.boxName] = this.recs;
    },
    updateTransformer() {
      // here we need to manually attach or detach Transformer node
      const transformerNode = this.$refs.transformer.getNode();
      const stage = transformerNode.getStage();
      const { selectedShapeName } = this;

      const selectedNode = stage.findOne('.' + selectedShapeName);
      // do nothing if selected node is already attached
      if (selectedNode === transformerNode.node()) {
        return;
      }

      if (selectedNode) {
        // attach to another node
        transformerNode.nodes([selectedNode]);
      } else {
        // remove transformer
        transformerNode.nodes([]);
      }
    },
    handleMouseUp(event) {
      console.log(event);
      if(!this.canDraw) return;
      if(!this.isDrawing) return;
      this.isDrawing = false;
      this.inputText();
    },
    inputText(){
      this.isInputing = true;
      this.$nextTick(() => {
        this.$refs.rec_name.focus();
      });
    },
    setRecName(){
      this.isInputing = false;
      this.recs[this.recs.length - 1].name = this.$refs.rec_name.value;
      this.$refs.rec_name.value = '';
      this.$store.state[this.boxName] = this.recs;
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
    photoPlus(){
      let i = 0.01;
      this.$refs.stage.getNode().scaleX(this.$refs.stage.getNode().scaleX() + i);
      this.$refs.stage.getNode().scaleY(this.$refs.stage.getNode().scaleY() + i);
    },
    photoMinus(){
      console.log(this.$refs.stage.getNode().scaleX())
      console.log(this.$refs.stage.getNode().scaleY())
      let i = 0.01;
      this.$refs.stage.getNode().scaleX(this.$refs.stage.getNode().scaleX() - i);
      this.$refs.stage.getNode().scaleY(this.$refs.stage.getNode().scaleY() - i);
    },
    resetSize(){
      this.$refs.stage.getNode().scaleX(1);
      this.$refs.stage.getNode().scaleY(1);
    },
    wheelForScale(event) {
      if (event.evt.wheelDelta > 0) {
        let i = 0.01;
        this.$refs.stage.getNode().scaleX(this.$refs.stage.getNode().scaleX() + i);
        this.$refs.stage.getNode().scaleY(this.$refs.stage.getNode().scaleY() + i);
        i++;
      } else {
        let i = 0.01;
        this.$refs.stage.getNode().scaleX(this.$refs.stage.getNode().scaleX() - i);
        this.$refs.stage.getNode().scaleY(this.$refs.stage.getNode().scaleY() - i);
        i++;
      }
    },
    showEventInfoModal(name) {
      this.$store.state.eventInfoModal = true;
      this.$store.state.eventInfoModalName = name;
    },
    centreRectShape(){
      this.imageConfig.x = this.$refs.img_block.getBoundingClientRect().left + (this.$refs.img_block.clientWidth- this.imageConfig.width)/2;
      this.imageConfig.y = this.$refs.img_block.getBoundingClientRect().top + (this.$refs.img_block.clientHeight - this.imageConfig.height)/2;
      console.log(this.imageConfig.x, this.imageConfig.y);
    }
  },
  props: {
    boxName: {
      type: String,
      required: true,
    },
    canDraw: {
      type: Boolean,
      default: true,
    },
    fillColor: {
      type: Object,
      required: false,
    },
    otherBoxes: {
      type: Object,
      required: false,
   },
  },
}
</script>