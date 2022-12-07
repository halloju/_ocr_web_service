<template>
    <div class="grid">
      <div class="col-7">
        <div class="card" style="height:850px; overflow-y: scroll;">
        <h2>公用模板檢視</h2>
        <el-table :data="tableData" style="width: 100%">
            <el-table-column
            :prop="item.prop"
            :label="item.label"
            v-for="(item, index) in tableHeader"
            :key="item.prop"
            :width="item.width"
            >
            <template #default="scope">
                <div
                v-show="item.editable || scope.row.editable"
                class="editable-row"
                >
                <template v-if="item.type === 'input'">
                    <el-input
                    size="small"
                    v-model="scope.row[item.prop]"
                    :placeholder="`請輸入 ${item.label}`"
                    @change="handleEdit(scope.$index, scope.row)"
                    />
                </template>
                <template v-if="item.type === 'date'">
                    <el-date-picker
                    v-model="scope.row[item.prop]"
                    type="date"
                    value-format="YYYY-MM-DD"
                    :placeholder="`請輸入 ${item.label}`"
                    @change="handleEdit(scope.$index, scope.row)"
                    />
                </template>
                </div>
                <div
                v-show="!item.editable && !scope.row.editable"
                class="editable-row"
                >
                <span class="editable-row-span">{{ scope.row[item.prop] }}</span>

                </div>
            </template>
            </el-table-column>
            <el-table-column label="操作" width="320px">
            <template #default="scope">
                <el-button
                v-show="!scope.row.editable"
                size="big"
                @click="scope.row.editable = true"
                >編輯</el-button
                >
                <el-button
                v-show="scope.row.editable"
                size="small"
                type="success"
                @click="scope.row.editable = false"
                >確認</el-button
                >
                <el-button
                size="big"
                type="info"
                @click=""
                >檢視</el-button
                >
                <el-button
                size="big"
                type="danger"
                @click="handleDelete(scope.$index)"
                >删除</el-button
                >
            </template>
            </el-table-column>
        </el-table>
        </div>
      </div>
      <div class="col-5">
        <div class="card"  style="height:850px; overflow-y: scroll;">
            <h5>請選擇模式</h5>
            <div class="flex flex-column card-container">
                <div class="flex align-items-center justify-content-center h-4rem font-bold border-round m-2">
                    <SelectButton v-model="myModel" :options="models" optionLabel="name" />
                </div>
                <div class="flex align-items-center justify-content-center h-4rem font-bold border-round m-2">
                    <Button icon="pi pi-download" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'下載模板設定檔'" @click="" />
                    <Button icon="pi pi-pencil" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'編輯模版'" @click="" />
                    <Button icon="pi pi-trash" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'刪除模板'" @click="" disabled="true"/>
                </div>
                <div class="flex align-items-center justify-content-center h-100rem font-bold border-round m-2">
                    <Image src="../src/assets/img/card-visa.jpg" alt="Image" width="500" preview />
                </div>
                <div class="flex align-items-center justify-content-center h-100rem font-bold border-round m-2">
                    <BoxCard boxName="recs_text" :boxTitle="myModel.name" />
                </div>
            </div>
        </div>
      </div>
    </div> 
</template>
<script>
import PhotoService from '@/service/PhotoService';
import BoxCard from '@/components/BoxCard.vue';

  const item = {
    name: '',
    birth: '',
    province: "",
    city: "",
    address: '',
    phone: "",
  }
  const header = {
    prop: "key",
    label: "自定義",
    editable: false,
    type: "input",
  }
  export default {
    name: "public",
    components: {
        BoxCard,
    },
    created() {
		this.galleriaService = new PhotoService();
	},
	mounted() {
        this.galleriaService.getImages().then(data => this.images = data);
    },
    data() {
      return {
        models: [{ name: '文字位置標註' }, { name: '方塊位置標註' }, { name: '遮罩位置標註' }],
        myModel: { name: '文字' },
        images: null,
        tableHeader: [
          {
            prop: "no",
            label: "No.",
            editable: false,
            type: "number",
            width: "50px",
          },
          {
            prop: "name",
            label: "姓名",
            editable: false,
            type: "input",
            width: "250px",
          },
          {
            prop: "date",
            label: "更新日期",
            editable: false,
            type: "date",
            width: "130px",
          },
        ],
        tableData: [{
          no: 1,
          name: '企鵝不捨',
          date: '2016-05-02',
        }, {
          no: 2,
          name: '企噗噗',
          date: '2016-05-04',
        }, {
          no: 3,
          name: '我就小企',
          date: '2016-05-01',
        }, {
          no: 4,
          name: '我真的生企了',
          date: '2016-05-03',
        }]
      }
    },
    methods: {
      handleEdit(row) {
        row.editable = true;
      },
      handleDelete(index) {
        this.tableData.splice(index, 1);
      },
      prepend(index) {
        item.editable = true
        this.tableData.splice(index, 0, item);
      },
      append(index) {
        item.editable = true
        this.tableData.splice(index + 1, 0, item);
      },
      deleteCurrentColumn(index) {
        this.tableHeader.splice(index, 1);
      },
      insertBefore(index) {
        header.editable = true;
        this.tableHeader.splice(index, 0, header);
      }
  }
}
</script>