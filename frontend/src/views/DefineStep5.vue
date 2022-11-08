<template>
  <div class="step">
    Step.5 資訊確認
  </div>
  <div class="contentWrapperFlex">
    <Box :boxName="'recs_text'" />
    <div class="contentWrapper2 py-5">
      <div class="contentWrapperSub">
        <BoxCard :BoxTitle="'文字辨識位置'" :boxName="'recs_text'"/>
        <BoxCard :boxName="'recs_block'" :BoxTitle="'核取方塊位置'"/>
        <div class="template-description">
          模板說明
          <br>
          <input value="e.g. Happy 名片">
      </div>
    </div>
    </div>
  </div>
  <div class="buttons">
    <button type="button" class="btn bg-secondary btn-right" data-bs-toggle="modal" data-bs-target="#exampleModal">取消</button>
    <button type="button" class="btn bg-primary btn-right" data-bs-toggle="modal" data-bs-target="#exampleModal">上傳</button>
  </div>
  <!-- Modal -->
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">標題文字</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">請確認</div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            關閉
          </button>
          <button type="button" class="btn btn-primary">確定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '@/assets/css/content.css';
</style>
<script>
import open_eye from '@/assets/images/open_eye.svg'
import close_eye from '@/assets/images/close_eye.svg'
import Box from '@/components/Box.vue'
import BoxCard from '@/components/BoxCard.vue'

export default {
    name: "DefineStep5",
    mounted() {
    },
    data() {
      return {
        open_eye: open_eye,
        close_eye: close_eye,
      };
    },
    methods: {},
    components: { 
      BoxCard,
      Box,
    }
};
</script>