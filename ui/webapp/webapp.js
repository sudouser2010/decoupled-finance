const { createApp } = Vue
import base_view from './views/base_view.js'
import main_view from './views/main.js'


//-------------------------------------------router stuff
const routes = [
  { path: '/', component: base_view,
    children: [
      { name:'digital-card', path: '', component: main_view },
      { name:'default', path: '', redirect: { name: 'digital-card' }},
    ]
  },
]
const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes,
})
//-------------------------------------------router stuff



// ------------ Vuetify
const { createVuetify } = Vuetify
const vuetify = createVuetify()
// ------------ Vuetify

createApp({
  data: function() {
   return {
      router: router,
      }
   },
  methods:{
  },
  mounted: async function() {
  }

}).use(router).use(vuetify).mount('#app')
