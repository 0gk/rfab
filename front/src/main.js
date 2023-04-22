import { createApp } from 'vue'

import axios from 'axios'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import './style.css'
import App from './App.vue'
import GlobalMixin from './globalmixin.js'

const app = createApp(App);

app.use(ElementPlus);

app.mixin(GlobalMixin)

// app.config.globalProperties.$plid = null; 

app.mount('#app');
