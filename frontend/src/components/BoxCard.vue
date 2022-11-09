<template>
  <div class="contentWrapper2 py-5">
      <div class="bar">
        <span class="content-title">{{ BoxTitle }}</span>
      </div>
      <div class="my-content2">
        <div class="my-table">
          <span class="no">No.</span>
          <span class="ele-name">要項名稱</span>
        </div>
        <div v-for="(rec, index) in recs" class="card" style="width: 18rem;">
          <div class="card-body">
            <h4 class="card-subtitle mb-2 text-muted">id: {{ index }}</h4>
            <h5 class="card-title">name: {{ rec.name }}</h5>
            <button type="button" class="btn btn-primary btn-sm" @click="deleteRec(index)">刪除</button>
          </div>
        </div>
      <!-- <button class="btn bg-primary btn-sm align-middle" @click="saveRects">儲存</button> -->
      </div>
    </div>
</template>

<style scope>
@import '@/assets/css/content.css';
</style>

<script>

export default {
  name: 'BoxCard',
  mounted(){
    this.recs = this.$store.state[this.boxName];
    console.log(this.recs);
  },
  components: {
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
    BoxTitle: {
      type: String
    },
  },
}
</script>