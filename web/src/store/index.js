import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

const store = new Vuex.Store({
    plugins: [createPersistedState()],
    state: {
        // 自定義模板
        selfDefinedRecs: { text: [], box: [], mask: [] },
        // 通用辨識
        general_boxes: [],
        general_upload_image: [],
        general_upload_res: [],
        general_execute_time: 0
    },

    mutations: {
        recsUpdate: function (state, payload) {
            state.selfDefinedRecs[payload.type].push(payload.data);
        },
        recsNameUpdate: function (state, payload) {
            let index = state.selfDefinedRecs[payload.type].length - 1;
            state.selfDefinedRecs[payload.type][index].name = payload.name;
            state.selfDefinedRecs[payload.type][index].canDelete = payload.canDelete;
            state.selfDefinedRecs[payload.type][index].canEdit = payload.canEdit;
        },
        recsSizeUpdate: function (state, payload) {
            let index = state.selfDefinedRecs[payload.type].length - 1;
            state.selfDefinedRecs[payload.type][index].width = payload.data.width;
            state.selfDefinedRecs[payload.type][index].height = payload.data.height;
            state.selfDefinedRecs[payload.type][index].endPointX = payload.data.endPointX;
            state.selfDefinedRecs[payload.type][index].endPointY = payload.data.endPointY;
        },
        recsDelete: function (state, payload) {
            state.selfDefinedRecs[payload.type].splice(payload.index, 1);
        },
        recsNameEdit: function (state, payload) {
            state.selfDefinedRecs[payload.type][payload.index].canSave = payload.canSave;
            state.selfDefinedRecs[payload.type][payload.index].canEdit = payload.canEdit;
        },
        recsNameSave: function (state, payload) {
            state.selfDefinedRecs[payload.type][payload.index].name = payload.name;
            state.selfDefinedRecs[payload.type][payload.index].canSave = payload.canSave;
            state.selfDefinedRecs[payload.type][payload.index].canEdit = payload.canEdit;
        },
        recsClear: function (state) {
            Object.keys(state.selfDefinedRecs).forEach((key) => {
                state.selfDefinedRecs[key] = [];
            });
        },
        generalBoxesUpdate: function (state, payload) {
            state.general_boxes = payload;
        },
        generalImageUpdate: function (state, payload) {
            state.general_upload_image = payload;
        },
        generalImageResponse: function (state, payload) {
            state.general_upload_res = payload;
        },
        generalExecuteTime: function (state, payload) {
            state.general_execute_time = payload;
        }
    }
});
export default store;
