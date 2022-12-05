<template>
  <v-group
    v-for="(rec, index) in recs"
    :key="index"
    :config="{
      x: Math.min(rec.startPointX, rec.startPointX + rec.width),
      y: Math.min(rec.startPointY, rec.startPointY + rec.height),
    }"
    draggable="true"
  >
    <v-rect
      :key="index"
      :name="rec.name"
      :config="{
        width: Math.abs(rec.width),
        height: Math.abs(rec.height),
        fill: `rgb(${this.fillColor.r},${this.fillColor.g},${this.fillColor.b},${this.fillColor.a})`,
        stroke: 'rgb(20,20,200,1)',
        strokeWidth: 3,
      }"
      @transformend="handleTransformEnd"
    />
    <v-text
      :config="{
        text: index,
        fontSize: 30,
        fill: 'rgb(20,20,200,1)',
        x: 0,
        y: 0,
      }"
    />
  </v-group>
</template>

<style scope>
@import '@/assets/css/content.css';
</style>

<script>

export default {
  name: 'Rect',
  mounted(){
    this.recs = this.$store.state[this.boxName];
  },
  components: {
  },
  data(){
  },
  computed:{
    recs(){
      return this.$store.state[this.boxName];
    },
  },
  methods:{
    handleTransformEnd(e) {
      // shape is transformed, let us save new attrs back to the node
      // find element in our state
      const rect = this.recs.find(
        (r) => r.name === this.selectedShapeName
      );
      // update the state
      rect.x = e.target.x();
      rect.y = e.target.y();
      rect.rotation = e.target.rotation();
      rect.scaleX = e.target.scaleX();
      rect.scaleY = e.target.scaleY();
    }
  },
  props: {
    boxName: {
      type: String,
      required: true,
    },
    fillColor: {
      type: Object,
      default: {
        r: 0,
        g: 0,
        b: 0,
        a: 0.3,
      },
    },
  },
}
</script>