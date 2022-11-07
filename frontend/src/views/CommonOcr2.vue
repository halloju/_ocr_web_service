<template>
  <div class="step">
    符合讀取規則的圖檔共 1000 張
  </div>
  <div class="sub-step">
    因為批次辨識時間較長，請確認辨識設定無誤。若無任何問題，請按開始全部辨識。
  </div>
  <div class="contentWrapperFlex">
    <div class="contentWrapper5 py-5 ">
    </div>
    <div class="contentWrapperSubFull">
    </div>
  </div>
  <div class="buttons">
    <button type="button" class="btn bg-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">全部辨識</button>
  </div>
  <!-- Modal -->
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">是否已確認單張項目</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">確認後將進行全部辨識，請勿關閉網頁。</div>
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
@import '@/assets/css/template.css';
</style>
<script>
export default {
  name: 'DefineStep1',
  data() {
    return {

    };
  },
  methods: {
    }

};
</script>