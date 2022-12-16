<template>
    <div class="" ref="img_block">
        <div class="flex card-container overflow-hidden">
            <v-stage ref="stage" :config="stageConfig" @mousemove="handleMouseMove" @mouseDown="handleMouseDown" @mouseUp="handleMouseUp" @wheel="imgZoom">
                <v-layer ref="layer">
                    <v-image
                        :config="{
                            width: this.imageConfig.width,
                            height: this.imageConfig.height,
                            image: this.image,
                            opacity: this.imageConfig.opacity,
                            x: this.imageConfig.x,
                            y: this.imageConfig.y
                        }"
                        ref="image"
                    />
                    <!-- <Rect v-if="canDraw" :boxName="boxName" :fillColor="fillColor" /> -->
                    <Rect v-for="box in this.Boxes" :key="box.name" :boxName="box.name" :fillColor="box.fillColor" />
                    <v-transformer ref="transformer" :rotateEnabled="false" :keepRatio="false" :enabledAnchors="['top-left', 'top-right', 'bottom-left', 'bottom-right']" />
                </v-layer>
            </v-stage>
        </div>
        <div class="flex align-items-stretch flex-wrap card-container blue-container" style="min-height: 70px">
            <div class="flex align-items-center justify-content-center font-bold text-white border-round m-2" style="min-width: 200px; min-height: 50px">
                <Button icon="pi pi-search-plus" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'放大圖片'" @click="photoPlus" />
                <Button icon="pi pi-search-minus" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'縮小圖片'" @click="photoMinus" />
                <Button icon="pi pi-undo" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'還原圖片大小'" @click="resetSize" />
            </div>
            <div class="flex align-items-center justify-content-center font-bold text-white border-round m-2" style="min-width: 200px; min-height: 50px">
                <div v-if="isInputing" class="p-inputgroup">
                    <input class="form-control" type="text" placeholder="請輸入 Label 名稱(不可重複)" ref="rec_name" :disabled="!isInputing" />
                    <Button label="GO! 命名" @click="setRecName" v-tooltip="'請先框好圖片再點擊'" style="width: 250px" :disabled="!isInputing"></Button>
                </div>
            </div>
            <div class="flex align-items-center justify-content-center font-bold text-white border-round m-2" style="min-width: 200px; min-height: 50px">
                <InlineMessage v-if="isWarning">請至少輸入一個文字，謝謝配合。</InlineMessage>
            </div>
        </div>
    </div>
</template>
<script>
import Rect from '@/components/Rect.vue';
const ratio = 1;

export default {
    name: 'Box',
    mounted() {
        this.image = new window.Image();
        this.image.src = sessionStorage.imageSource;
        const resize = Math.min(this.$refs.img_block.clientWidth / this.image.width, this.$refs.img_block.clientHeight / this.image.height);
        this.image.onload = () => {
            this.imageConfig = {
                width: this.image.width * resize * ratio,
                height: this.image.height * resize * ratio,
                x: (this.$refs.img_block.clientWidth - this.image.width * resize * ratio) / 2,
                y: (this.$refs.img_block.clientHeight - this.image.height * resize * ratio) / 2
            };
        };
        this.recs = this.$store.state[this.Boxes[0].name];
        this.canDraw = this.Boxes.length <= 1;
    },
    components: {
        Rect
    },
    data() {
        return {
            recs: [],
            image: null,
            stageConfig: {
                x: 0,
                y: 0,
                width: 800,
                height: 600
            },
            imageConfig: {
                width: null,
                height: null,
                x: 10,
                y: 20
            },
            isDrawing: false,
            isInputing: false,
            isNamingOk: true,
            isTransforming: false,
            isWarning: false,
            canDraw: true
        };
    },
    watch: {
        $route() {
            this.recs = [];
        }
    },
    methods: {
        handleMouseDown(event) {
            if (!this.isNamingOk) return;
            if (!this.canDraw) return;
            if (event.target === event.target.getStage()) return;
            if (this.isTransforming & (event.target.className === 'Image')) {
                this.selectedShapeName = '';
                this.updateTransformer();
                this.isTransforming = false;
                return;
            }

            // transform rect
            if (event.target.className === 'Rect') {
                this.isTransforming = true;

                // // clicked on transformer - do nothing
                const clickedOnTransformer = event.target.getParent().className === 'Transformer';
                if (clickedOnTransformer) {
                    return;
                }

                // find clicked rect by its name
                const name = event.target.name();
                const rect = this.recs.find((r) => r.name === name);
                if (rect) {
                    this.selectedShapeName = name;
                } else {
                    this.selectedShapeName = '';
                }
                this.updateTransformer();
                return;
            }

            // draw rect
            this.isDrawing = true;
            this.isNamingOk = false;
            const pos = this.$refs.stage.getNode().getPointerPosition();
            this.setRecs([...this.recs, { startPointX: pos.x, startPointY: pos.y, endPointX: pos.x, endPointY: pos.y, scaleX: 1, scaleY: 1, width: 0, height: 0, canDelete: false, canEdit: false, canSave: false }]);
            this.$store.state[this.Boxes[0].name] = this.recs;
            //this.$store.commit('recsUpdate', this.recs);
            this.isInputing = false;
        },
        updateTransformer() {
            // here we need to manually attach or detach Transformer node
            const transformerNode = this.$refs.transformer.getNode();
            const stage = transformerNode.getStage();
            const { selectedShapeName } = this;

            const selectedNode = stage.findOne('.' + selectedShapeName);
            // do nothing if selected node is already attached
            if (selectedNode === transformerNode.node()) {
                return;
            }

            if (selectedNode) {
                // attach to another node
                transformerNode.nodes([selectedNode]);
            } else {
                // remove transformer
                transformerNode.nodes([]);
            }
        },
        handleMouseUp() {
            if (!this.canDraw) return;
            if (!this.isDrawing) return;
            this.isDrawing = false;
            this.inputText();
        },
        inputText() {
            this.isInputing = true;
            this.$nextTick(() => {
                this.$refs.rec_name.focus();
            });
        },
        setRecName() {
            if (this.$refs.rec_name.value.length === 0) {
                this.isWarning = true;
            } else {
                this.isInputing = false;
                this.recs[this.recs.length - 1].name = this.$refs.rec_name.value;
                this.recs[this.recs.length - 1].canDelete = true;
                this.recs[this.recs.length - 1].canEdit = true;
                this.$refs.rec_name.value = '';
                // this.$store.state[this.boxName] = this.recs;
                this.$store.commit('recsUpdate', this.recs);
                this.isNamingOk = true;
                this.isWarning = false;
            }
        },
        setRecs(element) {
            this.recs = element;
        },
        handleMouseMove() {
            // no drawing - skipping
            if (!this.isDrawing) {
                return;
            }
            // console.log(event);
            const point = this.$refs.stage.getNode().getPointerPosition();
            // handle  rectangle part
            let curRec = this.recs[this.recs.length - 1];
            curRec.width = point.x - curRec.startPointX;
            curRec.height = point.y - curRec.startPointY;
            curRec.endPointX = point.x;
            curRec.endPointY = point.y;
        },
        photoPlus() {
            let i = 0.01;
            this.$refs.stage.getNode().scaleX(this.$refs.stage.getNode().scaleX() + i);
            this.$refs.stage.getNode().scaleY(this.$refs.stage.getNode().scaleY() + i);
        },
        photoMinus() {
            console.log(this.$refs.stage.getNode().scaleX());
            console.log(this.$refs.stage.getNode().scaleY());
            let i = 0.01;
            this.$refs.stage.getNode().scaleX(this.$refs.stage.getNode().scaleX() - i);
            this.$refs.stage.getNode().scaleY(this.$refs.stage.getNode().scaleY() - i);
        },
        resetSize() {
            let stage = this.$refs.stage.getStage();
            stage.position(this.stageConfig.x, this.stageConfig.y);
            stage.scale({ x: 1, y: 1 });
        },
        imgZoom(event) {
            var scaleBy = 1.001;
            let stage = event.target.getStage();
            stage.on('wheel', (e) => {
                // stop default scrolling
                e.evt.preventDefault();

                var oldScale = stage.scaleX();
                var pointer = stage.getPointerPosition();

                var mousePointTo = {
                    x: (pointer.x - stage.x()) / oldScale,
                    y: (pointer.y - stage.y()) / oldScale
                };

                // how to scale? Zoom in? Or zoom out?
                let direction = e.evt.deltaY > 0 ? 1 : -1;

                // when we zoom on trackpad, e.evt.ctrlKey is true
                // in that case lets revert direction
                if (e.evt.ctrlKey) {
                    direction = -direction;
                }

                var newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy;

                stage.scale({ x: newScale, y: newScale });

                var newPos = {
                    x: pointer.x - mousePointTo.x * newScale,
                    y: pointer.y - mousePointTo.y * newScale
                };
                stage.position(newPos);
            });
        }
    },
    props: {
        Boxes: {
            type: Array,
            required: false
        }
    }
};
</script>
