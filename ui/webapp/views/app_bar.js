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
        <diSv style="font-weight: 500; font-size: 40px; margin-left: 20px;">
            Decoupled Finance
        </diSv>  
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
  },
  computed: {
  }
}
