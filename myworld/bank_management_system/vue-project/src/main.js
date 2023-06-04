import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import locale from 'element-plus/lib/locale/lang/zh-cn'
import router  from './router'

createApp(App).use(router).use(ElementPlus, {locale}).mount('#app')
