import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import es from 'vuetify/es5/locale/es';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#BE0707',
        secondary: '#424242',
        accent: '#0A4A73',
        error: '#FF5252',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FFC107'
      },
    },
  },
  iconfont: 'md',
    lang: {
      locales: { es },
      current: 'es',
    },
});
