<template>
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
</template>

<style scope>
@import '@/assets/css/content.css';
</style>

<script>
const width = window.innerWidth/2;
const height = window.innerHeight/2;
export default {
  name: 'Box',
  mounted(){
    this.image = new window.Image();
    this.image.src = sessionStorage.imageSource;
    this.image.onload = () => {
      this.stageSize = {
        width: width,
        height: height,
      };
    };
    this.recs = this.$store.state[this.boxName];
  },
  components: {
  },
  data(){
    return {
      recs: [],
      image: null,
      stageSize: {
        width: width,
        height: height,
      },
      isDrawing: false,
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
  },
  props: {
    boxName: {
      type: String
    }
  },
}
</script>