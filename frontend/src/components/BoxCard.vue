<template>
  <div class="contentWrapper2">
      <div class="bar">
        <span class="content-title">{{ boxTitle }}</span>
      </div>
      <div class="my-content2">
        <div class="my-table">
          <span class="no">No.</span>
          <span class="ele-name">要項名稱</span>
        </div>
        <Card v-if="canDelete"
          :boxName="boxName"
        />
        <Card v-else v-for="box in otherBoxes"
          :boxName="box.boxName"
          :boxTitle="box.boxTitle"
          :canDelete="canDelete"
        />
      </div>
      </div>
</template>

<style scope>
@import '@/assets/css/content.css';
</style>

<script>
import Card from '@/components/Card.vue';

export default {
  name: 'BoxCard',
  mounted(){
    this.recs = this.$store.state[this.boxName];
  },
  components: {
    Card,
  },
  computed:{
    recs(){
      return this.$store.state[this.boxName];
    },
  },
  methods:{
    deleteRec(index) {
      this.recs.splice(index, 1);
      this.$store.state[this.boxName] = this.recs;
    },
    saveRects() {
      sessionStorage.setItem(this.boxName, JSON.stringify(this.recs));
    },
  },
  props: {
    boxName: {
      type: String
    },
    boxTitle: {
      type: String
    },
    canDelete: {
      type: Boolean,
      default: true,
    },
    otherBoxes: {
      type: Object,
      required: false,
    },
  },
}
</script>