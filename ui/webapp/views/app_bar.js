export default {
  template: `
  <component is="style">
  .v-toolbar__content {
    height: 100px !important;
    background: black;
  }
  </component>
  <v-app-bar 
      color="deep-purple accent-4"
      dense
      dark  
  :elevation="4"
  style="position: relative !important; height: 100px"
  >
    <div style="width: 70%">
        <div style="font-weight: 500; font-size: 40px; margin-left: 20px;">
            Decoupled Finance
        </div>  
    </div>
                         

    <div style="width: 30%; text-align: right">
      <v-btn  @click="goToScan()" variant="outlined" size="small"
        style="margin-right: 20px;"
      >
        Send Token
      </v-btn>      
    </div>      
  
    

  </v-app-bar>
  `,
  data: () => ({
    defaultColor: 'grey',
    activeColor: 'white',
  }),
  methods: {
    goToScan() {
      this.$root.router.replace({ name: 'scan' })
    },
    goToSearch() {
      this.$root.router.replace({ name: 'search' })
    }
  },
  computed: {
    scanIconColor() {
      if (this.$root.router.currentRoute.name === 'scan') {
        return this.activeColor
      }
      return this.defaultColor
    },
    searchIconColor() {
      if (this.$root.router.currentRoute.name === 'search') {
        return this.activeColor
      }
      return this.defaultColor
    },
    donateUrl() {
      return `${this.$root.apiResource}/donate`
    },
  }
}
