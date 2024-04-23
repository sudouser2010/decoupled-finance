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
       balance: ' ',
       sendTokenModalActive: false,
      }
   },
  methods:{
   setBalance : async function() {
     const url = `${BLOCK_CHAIN_SERVER_URL}/state?address=placeholder`;
     let response

     try {
       response = await fetch(url);
     } catch (e) {
       alert('ERROR: COULD NOT CONNECT TO API')
       return
     }
     if (response.status >= 200 && response.status <= 204) {
       let data = await response.json()
       this.balance = data?.data?.amount || 0
     }
   }
  },
  mounted: async function() {
    await this.setBalance()
  }

}).use(router).use(vuetify).mount('#app')
