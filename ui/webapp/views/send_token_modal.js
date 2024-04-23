export default {
   template : `  
<v-dialog
  v-model="$root.sendTokenModalActive"
  width="300"
  eager
  v-if="$root.sendTokenModalActive"
>

  <v-card
    max-width="300"
    class="mx-auto send_token_modal"
  >
    <v-card-title style="font-size:30px; text-align: center; width: 300px">Send Token</v-card-title> 
    <v-container >
        Place Holder
    </v-container>
    
    <v-divider></v-divider>
    <v-card-actions>
      <v-btn color="primary" block @click="$root.sendTokenModalActive = false" height="50px">Close</v-btn>
    </v-card-actions>    
  </v-card>


</v-dialog>
   `
}
