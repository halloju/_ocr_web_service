<template>
  <div class="contentWrapperBlock py-5 "
    :class="getClasses" 
    @dragover.prevent="dragOver" 
    @dragleave.prevent="dragLeave"
    @drop.prevent="drop($event)">

      <img :src="imageSource" v-if="imageSource" />
      <div class="my-content" v-if="wrongFile">Wrong file type</div>
      <div class="my-content" v-if="!imageSource && !isDragging && !wrongFile">Drop an image</div>

</div>
</template>

<style scope>
@import '@/assets/css/content.css';
</style>

<script>

export default {
  name: 'DropAnImage',
  mounted(){
    if (sessionStorage.imageSource) {
      this.imageSource = sessionStorage.imageSource;
    }
  },
  components: {
  },
  data(){
    return{
      isDragging:false,
      wrongFile:false,
      imageSource:null
    }
  },
  computed:{
    getClasses(){
      return {isDragging: this.isDragging}
    }
  },
  methods:{
    dragOver(){
      if (this.isUploaded) {
        this.isDragging = true;
      }
    },
    dragLeave(){
      this.isDragging = false
    },
    drop(e){
      if (!this.isUploaded) {
        e.preventDefault()
        return
      }
      let files = e.dataTransfer.files
      this.wrongFile = false
      // allows only 1 file
      if (files.length === 1) {
        let file = files[0]
        // allows image only
        if (file.type.indexOf('image/') >= 0) {
          var reader = new FileReader()
          reader.onload = f => {
            this.imageSource = f.target.result
            this.isDragging = false
            sessionStorage.imageSource = this.imageSource
          }
          reader.readAsDataURL(file)
        }else{
          this.wrongFile = true
          this.imageSource = null
          this.isDragging = false
        }
      }
    },
    onRequestUploadFiles(){
      
    }
  },
  props: {
    isUploaded: {
      type: Boolean,
      default: false
    }
  },
}
</script>