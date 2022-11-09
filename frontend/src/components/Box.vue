<template>

  <v-stage
  ref="stage"
  :config="stageConfig"
  @wheel="wheelForScale($event)"
  @mousemove="handleMouseMove"
  @mouseDown="handleMouseDown"
  @mouseUp="handleMouseUp"
  >
  <v-layer ref="layer">
    <v-image
        :config="{
          x: 0,
          y: 0,
          width: this.imageConfig.width,
          height: this.imageConfig.height,
          image: this.image,
          opacity: this.imageConfig.opacity,
        }" ref="image"
    />
    <v-rect
      :config ="{
        x: 0,
        y: 0,
        width: this.imageConfig.width,
        height: this.imageConfig.width,
        fill: 'rgb(0,0,0,0)',
        stroke: 'black',
        strokeWidth: 3,
      }"
    />
    <v-group
      v-for="(rec, index) in recs"
      :key="index"
      :config="{
        x: Math.min(rec.startPointX, rec.startPointX + rec.width),
        y: Math.min(rec.startPointY, rec.startPointY + rec.height),
      }"
      @click="showEventInfoModal(rec.name)"
    >
    <v-rect
      :key="index"
      :config="{
        width: Math.abs(rec.width),
        height: Math.abs(rec.height),
        fill: 'rgb(256,256,256,0.1)',
        stroke: 'rgb(20,20,200,1)',
        strokeWidth: 3,
      }"
    />
    <v-text
      :config="{
        text: index,
        fontSize: 30,
        fill: 'rgb(20,20,200,1)',
        x: -20,
        y: 0,
      }"
    />
    </v-group>
  </v-layer>
  
  
  
  </v-stage>
  <form v-if="isInputing">
    <div class="form-group" >
      <input class="form-control" type="text" placeholder="text name" ref="rec_name">
    </div>
    <button type="submit" class="btn" @click="setRecName">Submit</button>
  </form>
</template>

<style scope>
@import '@/assets/css/content.css';
</style>

<script>
const width = window.innerWidth * 0.6;
const height = window.innerHeight * 0.6;

export default {
  name: 'Box',
  mounted(){
    this.image = new window.Image();
    this.image.src = sessionStorage.imageSource;
    this.image.onload = () => {
      this.imageConfig = {
        width: this.image.width,
        height: this.image.height,
      }
    };
    this.recs = this.$store.state[this.boxName];
  },
  components: {
  },
  data(){
    return {
      recs: [],
      image: null,
      stageConfig: {
        x: 10,
        y: 30,
        width: width,
        height: height,
      },
      imageConfig: {
        width: null,
        height: null,
      },
      isDrawing: false,
      isInputing: false,
      filters: [Konva.Filters.Blur]
    };
  },
  computed:{
  },
  methods:{
    handleMouseDown(event) {
      this.isDrawing = true;
      const pos = this.$refs.stage.getNode().getPointerPosition();
      this.setRecs([
        ...this.recs,
        { startPointX: pos.x, startPointY: pos.y, width: 0, height: 0 },
      ]);
      this.$store.state[this.boxName] = this.recs;
    },
    handleMouseUp() {
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
  },
  props: {
    boxName: {
      type: String
    }
  },
}
</script>