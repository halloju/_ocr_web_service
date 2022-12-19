import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

const store = new Vuex.Store({
    plugins: [createPersistedState()],
    state: {
        recs_text: [],
        general_upload_image: [],
        general_upload_res: [],
    },

    mutations: {
        recsUpdate: function (state, payload) {
            state.recs_text = payload;
        },
        generalImageUpdate: function (state, payload) {
            state.general_upload_image = payload;
        },
        generalImageResponse: function (state, payload){
            state.general_upload_res = payload;
        }
    }
});
export default store;
