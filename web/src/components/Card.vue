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
    methods: {
        deleteRec(index) {
            this.recs.splice(index, 1);
            this.$store.state[this.boxName] = this.recs;
        },
        editRec(index) {
            this.recs.splice(index, 1);
            this.$store.state[this.boxName] = this.recs;
        }
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

<template>
    <div v-for="(rec, index) in recs">
        <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
            <div class="text-500 w-6 md:w-2 font-medium">{{ index }}</div>
            <div class="text-900 w-full md:w-3 md:flex-order-0 flex-order-1">{{ rec.name }}</div>
            <div class="w-6 md:w-6 flex justify-content-end">
                <!-- <Button label="Edit" icon="pi pi-pencil" class="p-button-info" @click="editRec(index)" style="margin-right: 5px;"></Button> -->
                <Button label="Delete" icon="pi pi-times" class="p-button-danger" @click="deleteRec(index)" :disabled="!rec.canDelete"></Button>
            </div>
        </li>
    </div>
</template>
