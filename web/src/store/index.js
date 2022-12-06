import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate'

const store = new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    recs_text: [],
  },

  mutations: {
    recsUpdate:function (state, payload) {
        state.recs_text = payload;
    },
  },
})
export default store;
