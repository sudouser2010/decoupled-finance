import app_bar from './app_bar.js'

export default {
  components: {
    app_bar,
  },
   template : `
   <app_bar></app_bar>
   <router-view></router-view>
   `,
}
