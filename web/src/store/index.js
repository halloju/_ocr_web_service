import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

const store = new Vuex.Store({
    plugins: [createPersistedState()],
    state: {
        text: [],
        box: [],
        mask: [],
        general_upload_image: [],
        general_upload_res: []
    },

    mutations: {
        recsUpdate: function (state, payload) {
            state.text = payload;
        },
        generalImageUpdate: function (state, payload) {
            state.general_upload_image = payload;
        },
        generalImageResponse: function (state, payload) {
            state.general_upload_res = payload;
        }
    }
});
export default store;
