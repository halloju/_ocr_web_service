<script>
import { mapState } from 'vuex';

export default {
    name: 'BoxCard',
    data() {
        return {
            newName: ''
        };
    },
    computed: {
        ...mapState(['selfDefinedRecs']),
        recs() {
            return this.selfDefinedRecs[this.boxName];
        }
    },
    methods: {
        deleteRec(index) {
            this.$store.commit('recsDelete', {
                type: this.boxName,
                index: index
            });
        },
        editRec(index, oldName) {
            this.newName = oldName;
            this.$store.commit('recsNameEdit', {
                type: this.boxName,
                index: index,
                name: '',
                canEdit: false,
                canSave: true
            });
        },
        saveRec(index) {
            this.$store.commit('recsNameSave', {
                type: this.boxName,
                index: index,
                name: this.newName,
                canEdit: true,
                canSave: false
            });
        }
    },
    props: {
        boxName: {
            type: String
        },
        boxTitle: {
            type: String
        },
        canEdit: {
            type: Boolean
        }
    }
};
</script>
<template>
    <div v-for="(rec, index) in this.recs" :key="index">
        <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap" name="rec.name">
            <div class="text-500 w-6 md:w-2 font-medium">{{ index }}</div>
            <div v-if="!rec.canSave" class="text-900 w-full md:w-4 md:flex-order-0 flex-order-1">{{ rec.name }}</div>
            <div v-else class="text-900 w-full md:w-4 md:flex-order-0 flex-order-1"><InputText type="text" placeholder="請輸入新名稱" v-model="this.newName" /></div>
            <div v-if="this.canEdit" class="w-6 md:w-3 flex justify-content-end">
                <!-- 編輯 -->
                <Button v-if="!rec.canSave" label="" icon="pi pi-pencil" class="p-button-info" @click="editRec(index, rec.name)" style="margin-right: 5px" :disabled="!rec.canEdit"></Button>
                <!-- 存檔 -->
                <Button v-else label="" icon="pi pi-save" class="p-button-info" @click="saveRec(index)" style="margin-right: 5px" :disabled="!rec.canSave"></Button>
                <!-- 刪除 -->
                <Button label="" icon="pi pi-times" class="p-button-danger" @click="deleteRec(index)" :disabled="!rec.canDelete"></Button>
            </div>
        </li>
    </div>
</template>
