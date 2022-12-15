<template>
    <div v-for="(rec, index) in this.recs">
        <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap" name="rec.name">
            <div class="text-500 w-6 md:w-2 font-medium">{{ index }}</div>
            <div v-if="!rec.canSave" class="text-900 w-full md:w-3 md:flex-order-0 flex-order-1">{{ rec.name }}</div>
            <div v-else class="text-900 w-full md:w-3 md:flex-order-0 flex-order-1"><InputText type="text" placeholder="請輸入新名稱" v-model="newName"></InputText></div>
            <div class="w-6 md:w-3 flex justify-content-end">
                <!-- 編輯 -->
                <Button v-if="!rec.canSave" label="" icon="pi pi-pencil" class="p-button-info" @click="editRec(index)" style="margin-right: 5px;" :disabled="!rec.canEdit"></Button>
                <!-- 存檔 -->
                <Button v-else label="" icon="pi pi-save" class="p-button-info" @click="saveRec(index, newName)" style="margin-right: 5px;" :disabled="!rec.canSave"></Button>
                <!-- 刪除 -->
                <Button label="" icon="pi pi-times" class="p-button-danger" @click="deleteRec(index)" :disabled="!rec.canDelete"></Button>
            </div>
        </li>
    </div>
</template>
<script>

export default {
    name: 'BoxCard',
    mounted() {
        this.recs = this.$store.state[this.boxName];
        console.log(this.recs);
    },
    components: {},
    computed: {
        recs() {
            return this.$store.state[this.boxName];
        }
    },
    data (){
        return {
            newName: '',
        }
    },
    methods: {
        deleteRec(index) {
            this.recs.splice(index, 1);
            this.$store.state[this.boxName] = this.recs;
        },
        editRec(index) {
            this.newName = '';
            for (let i = 0; i < this.recs.length; i++) {
                if (index === i) {
                    this.recs[i].canSave = true;
                    this.recs[i].canEdit = false;
                    break;
                }
            }
        },
        saveRec(index, newName) {
            for (let i = 0; i < this.recs.length; i++) {
                    if (index === i) {
                        this.recs[i].canSave = false;
                        this.recs[i].canEdit = true;
                        if (newName.length!==0){
                            this.recs[i].name = newName;
                        } else {
                            break;
                        }
                    }
                }
            this.$store.state[this.boxName] = this.recs;
        },

    },
    props: {
        boxName: {
            type: String
        },
        boxTitle: {
            type: String
        }
    }
};
</script>
