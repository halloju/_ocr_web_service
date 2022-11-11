<template>
  <div class="contentWrapperBlock y-5" ref="img_block">
  <v-stage
  ref="stage"
  :config="stageConfig"
  @mousemove="handleMouseMove"
  @mouseDown="handleMouseDown"
  @mouseUp="handleMouseUp"
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
    </v-layer>
  </v-stage>
  <form v-if="isInputing">
    <div class="form-group" >
      <input class="form-control" type="text" placeholder="text name" ref="rec_name">
    </div>
    <button type="submit" class="btn" @click="setRecName">Submit</button>
  </form>
  </div>
  
</template>

<style scope>
@import '@/assets/css/content.css';
</style>

<script>
const ratio = 0.95;
import Rect from '@/components/Rect.vue'

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
        width: 1000,
        height: 720,
      },
      imageConfig: {
        width: null,
        height: null,
        x: 10,
        y: 20,
      },
      isDrawing: false,
      isInputing: false,
    };
  },
  computed:{
  },
  methods:{
    handleMouseDown(event) {
      if(!this.canDraw) return;
      this.isDrawing = true;
      const pos = this.$refs.stage.getNode().getPointerPosition();
      this.setRecs([
        ...this.recs,
        { startPointX: pos.x, startPointY: pos.y, width: 0, height: 0 },
      ]);
      this.$store.state[this.boxName] = this.recs;
    },
    handleMouseUp() {
      if(!this.canDraw) return;
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