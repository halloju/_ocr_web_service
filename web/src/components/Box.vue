<script>
import Rect from '@/components/Rect.vue';
import { mapState } from 'vuex';

export default {
    name: 'Box',
    mounted() {
        this.image = new window.Image();
        this.image.src = sessionStorage.imageSource;
        this.image.onload = () => {
            this.imageConfig = {
                x: 0,
                y: 0,
                width: this.image.width,
                height: this.image.height
            };
        };
        this.canDraw = this.Boxes.length <= 1;
        this.$nextTick(() => {
            this.updateStageConfig();
        });
        console.log(this.recs);
    },
    components: {
        Rect
    },
    data() {
        return {
            image: null,
            stageConfig: {
                x: 0,
                y: 0,
                width: 800,
                height: 800
            },
            imageConfig: {
                width: 800,
                height: 800,
                x: 0,
                y: 0
            },
            isDrawing: false,
            isInputing: false,
            isNamingOk: true,
            isTransforming: false,
            isWarning: false,
            canDraw: true,
            isActive: false
        };
    },
    watch: {
        $route() {
            this.recs = [];
        }
    },
    computed: {
        ...mapState(['selfDefinedRecs']),
        recs() {
            return this.selfDefinedRecs[this.Boxes[0].name] || [];
        }
    },
    methods: {
        handleMouseDown(event) {
            if (!this.isNamingOk) return;
            if (!this.canDraw) return;
            if (this.isActive) return;
            if (event.target === event.target.getStage()) return;
            if (this.isTransforming & (event.target.className === 'Image')) {
                this.selectedShapeName = '';
                this.updateTransformer();
                this.isTransforming = false;
                return;
            }
            // transform rect
            if (event.target.className === 'Rect' || event.target.className === 'Text') {
                this.isTransforming = true;
                console.log('transforming');
                // // clicked on transformer - do nothing
                const clickedOnTransformer = event.target.getParent().className === 'Transformer';
                if (clickedOnTransformer) {
                    return;
                }

                // find clicked rect by its name
                const name = event.target.name();
                console.log(this.recs);
                const rect = this.recs.find((r) => r.name === name);
                console.log(rect);
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
            const pos = this.$refs.image.getNode().getRelativePointerPosition();
            this.$store.commit('recsUpdate', {
                type: this.Boxes[0].name,
                data: {
                    startPointX: pos.x,
                    startPointY: pos.y,
                    endPointX: pos.x,
                    endPointY: pos.y,
                    scaleX: 1,
                    scaleY: 1,
                    width: 0,
                    height: 0,
                    canDelete: false,
                    canEdit: false,
                    canSave: false
                }
            });
            console.log(this.Boxes[0].name);
            this.isInputing = false;
        },
        updateTransformer() {
            // here we need to manually attach or detach Transformer node
            const transformerNode = this.$refs.transformer.getNode();
            transformerNode.anchorDragBoundFunc(this.transformerBoundBoxFunc);
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
                this.$store.commit('recsNameUpdate', {
                    type: this.Boxes[0].name,
                    name: this.$refs.rec_name.value,
                    canEdit: true,
                    canDelete: true
                });
                this.isNamingOk = true;
                this.isWarning = false;
                this.$refs.rec_name.value = '';
            }
        },
        setRecs(element) {
            this.recs = element;
            console.log(this.recs);
        },
        handleMouseMove() {
            // no drawing - skipping
            if (!this.isDrawing) {
                return;
            }
            // console.log(event);
            const point = this.$refs.image.getNode().getRelativePointerPosition();
            if (point.x < 0) {
                point.x = 0;
            }
            if (point.y < 0) {
                point.y = 0;
            }
            if (point.x > this.imageConfig.width) {
                point.x = this.imageConfig.width;
            }
            if (point.y > this.imageConfig.height) {
                point.y = this.imageConfig.height;
            }
            // handle  rectangle part
            let curRec = this.recs[this.recs.length - 1];
            curRec.width = point.x - curRec.startPointX;
            curRec.height = point.y - curRec.startPointY;
            curRec.endPointX = point.x;
            curRec.endPointY = point.y;
            this.$store.commit('recsSizeUpdate', {
                type: this.Boxes[0].name,
                data: curRec
            });
        },
        photoZoom(i) {
            if (!this.isActive) {
                this.$message({
                    message: '請進入可移動圖片模式',
                    type: 'warning'
                });
                return;
            }
            this.$refs.stage.getNode().scaleX(this.$refs.stage.getNode().scaleX() + i);
            this.$refs.stage.getNode().scaleY(this.$refs.stage.getNode().scaleY() + i);
        },
        resetSize() {
            this.updateStageConfig();
            let stage = this.$refs.stage.getStage();
            stage.scale({ x: 1, y: 1 });
            stage.x(this.stageConfig.x);
            stage.y(this.stageConfig.y);
            stage.on('wheel', (e) => {
                // stop default scrolling
                e.evt.preventDefault();
                if (!this.isActive) {
                    console.log('not wheel');
                    return;
                }
            });
        },
        imgZoom(event) {
            var scaleBy = 1.001;
            let stage = event.target.getStage();
            stage.on('wheel', (e) => {
                // stop default scrolling
                e.evt.preventDefault();
                if (!this.isActive) {
                    console.log('not wheel');
                    return;
                }
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
        },
        toggle() {
            const stage = this.$refs.stage.getNode();
            stage.draggable(this.isActive);
            this.selectedShapeName = '';
            this.updateTransformer();
            this.isTransforming = false;
            let Recs = this.$refs.image
                .getNode()
                .getParent()
                .getChildren(function (node) {
                    return node.getClassName() === 'Rect';
                });
            Recs.forEach((rec) => {
                rec.draggable(!this.isActive);
            });
        },
        handleImageDragEnd(e) {
            if (e.target !== this.$refs.stage.getNode()) {
                return;
            }
            const pos = e.target.getPosition();
            this.stageConfig.x = pos.x;
            this.stageConfig.y = pos.y;
        },
        updateStageConfig() {
            this.stageConfig = {
                x: (this.$refs.img_block.clientWidth - this.image.width) / 2,
                y: (this.$refs.img_block.clientHeight - this.image.height) / 2,
                width: this.$refs.img_block.clientWidth,
                height: this.$refs.img_block.clientHeight
            };
        },
        transformerBoundBoxFunc(oldAbsPos, newAbsPos) {
            const div = this.$refs.img_block.getBoundingClientRect();
            const AbsPos = {
                x: div.left + this.stageConfig.x,
                y: div.top + this.stageConfig.y
            };
            let x = newAbsPos.x;
            let y = newAbsPos.y;
            if (newAbsPos.x < AbsPos.x) {
                x = AbsPos.x;
            }
            if (newAbsPos.y < AbsPos.y) {
                y = AbsPos.y;
            }
            if (newAbsPos.x > AbsPos.x + this.image.width) {
                x = this.image.width - this.selectedShape.width;
            }
            return {
                x: x,
                y: y
            };
        }
    },
    props: {
        Boxes: {
            type: Array,
            required: false
        },
        isShapesVisible: {
            type: Object,
            default: () => {
                return {
                    text: true,
                    box: true,
                    mask: true
                };
            }
        }
    }
};
</script>
<template>
    <div class="card">
        <div class="card-container overflow-hidden" ref="img_block">
            <v-stage ref="stage" :config="stageConfig" @mousemove="handleMouseMove" @mouseDown="handleMouseDown" @mouseUp="handleMouseUp" @wheel="imgZoom" @dragend="handleImageDragEnd">
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
                    <Rect v-for="box in this.Boxes" :key="box.name" :boxName="box.name" :fillColor="box.fillColor" :imageAttrs="{ width: this.imageConfig.width, height: this.imageConfig.height }" :isShapesVisible="this.isShapesVisible[box.name]" />
                    <v-transformer ref="transformer" :rotateEnabled="false" :keepRatio="false" :enabledAnchors="['top-left', 'top-right', 'bottom-left', 'bottom-right']" />
                </v-layer>
            </v-stage>
        </div>
        <div class="flex align-items-stretch flex-wrap card-container blue-container overflow-hidden" style="min-height: 70px">
            <div class="flex align-items-center justify-content-center font-bold text-white border-round m-4" style="min-width: 200px; min-height: 50px">
                <Button icon="pi pi-search-plus" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'放大圖片'" @click="photoZoom(0.01)" />
                <Button icon="pi pi-search-minus" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'縮小圖片'" @click="photoZoom(-0.01)" />
                <Button icon="pi pi-undo" class="p-button-rounded p-button-info mr-2 mb-2" v-tooltip="'還原圖片大小'" @click="resetSize" />
            </div>
            <div class="flex align-items-center justify-content-center font-bold text-white border-round m-4" style="min-width: 200px; min-height: 50px">
                <ToggleButton v-model="isActive" onLabel="可移動圖片" offLabel="編輯模式" onIcon="pi pi-check" offIcon="pi pi-times" @change="toggle" />
            </div>
            <div class="flex align-items-center justify-content-center font-bold text-white border-round m-4" style="min-width: 200px; min-height: 50px">
                <div v-if="isInputing" class="p-inputgroup">
                    <input class="form-control" type="text" placeholder="請輸入 Label 名稱(不可重複)" ref="rec_name" :disabled="!isInputing" />
                    <Button label="GO! 命名" @click="setRecName" v-tooltip="'請先框好圖片再點擊'" style="width: 250px" :disabled="!isInputing"></Button>
                </div>
            </div>
            <div class="align-items-center justify-content-center font-bold text-white border-round m-4" style="min-width: 200px; min-height: 50px">
                <InlineMessage v-if="isWarning">請至少輸入一個文字，謝謝配合。</InlineMessage>
            </div>
        </div>
    </div>
</template>
