import digital_card from './digital_card.js'


export default {
  components: {
    digital_card,
  },
  template : `
<v-container class="fill-height" fluid>
  <v-row align="center" class="fill-height" justify="center">  
      
    <div style="max-width: 500px; width: 90%; height: 100%">
                               
      <v-row justify="center" style="margin-bottom: 120px; position: relative">
        <digital_card></digital_card>   
      </v-row> 
       
    </div>      
   
  </v-row>
</v-container>
 `,
  computed: {
  },
}
