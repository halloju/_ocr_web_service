<template>
  <div v-for="(rec, index) in recs" class="card mb-7" style="width: 18rem;">
    <div class="row g-8">
      <div class="col-md-6">
        <div class="card-body">
          <h5 class="card-subtitle mb-2 text-muted">id: {{ index }} </h5>
          <h5 class="card-subtitle mb-2 text-muted">name: {{ rec.name }}</h5>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card-body">
          <button v-if="canDelete" type="button" class="delete-btn" @click="deleteRec(index)">刪除</button>
          <div v-else class="card-subtitle mb-2 text-muted">{{ boxTitle }}</div>
        </div>
      </div>
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
  },
}
</script>