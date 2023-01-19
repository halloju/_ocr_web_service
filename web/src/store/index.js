import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

const store = new Vuex.Store({
    plugins: [createPersistedState()],
    state: {
        // 自定義模板
        text: [],
        box: [],
        mask: [],
        // 通用辨識
        general_boxes: [],
        general_upload_image: [],
        general_upload_res: [],
        general_execute_time: 0
    },

    mutations: {
        recsUpdate: function (state, name, payload) {
            state.state[name] = payload;
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
