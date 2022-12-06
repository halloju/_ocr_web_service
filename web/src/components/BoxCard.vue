<template>
    <div class="surface-section" style="height:700px; overflow-y: scroll;">
      {{this.recs}}
      <div class="font-medium text-3xl text-900 mb-3">{{ boxTitle }}</div>
      <ul class="list-none p-0 m-0">
          <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
              <div class="text-500 w-6 md:w-2 font-medium">No.</div>
              <div class="text-900 w-full md:w-3 md:flex-order-0 flex-order-1">要項名稱</div>
              <div class="text-900 w-6 md:w-3 flex justify-content-end">操作</div>
          </li>
          
          <Card 
          :boxName="boxName"
          />
      </ul>
    </div>
</template>

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