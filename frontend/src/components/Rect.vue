<template>
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
        fill: `rgb(${this.fillColor.r},${this.fillColor.g},${this.fillColor.b},${this.fillColor.a})`,
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
</template>

<style scope>
@import '@/assets/css/content.css';
</style>

<script>

export default {
  name: 'Rect',
  mounted(){
    this.recs = this.$store.state[this.boxName];
    console.log(this.recs);
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