export default {
   template : `  
<component is="style">
    .send_token_container {
        padding: 30px;
    }
</component>  
<v-dialog
  v-model="$root.sendTokenModalActive"
  width="400"
  eager
  v-if="$root.sendTokenModalActive"
>

  <v-card
    max-width="400"
    class="mx-auto send_token_modal"
  >
    <v-card-title style="font-size:30px; text-align: center; width: 300px">Send Token</v-card-title> 
    <v-container  class="send_token_container">
      <v-text-field 
      v-model="amount"    
      variant="outlined"          
      placeholder="Amount"
      type="number"
      ></v-text-field>  
       
      <v-text-field 
      v-model="address"    
      variant="outlined"          
      placeholder="Address"
      ></v-text-field>     
       
      <v-btn  
      :loading="loading"
      :disabled="loading"
      @click="submit"
      
      color="rgb(15 181 82)"
      rounded="pill"  
      style="height: 50px; color:white; width: 100%"
      id="send-token"
      >
        Submit
      </v-btn>                   
    </v-container>
    
    <v-divider></v-divider>
    <v-card-actions>
      <v-btn color="primary" block @click="$root.sendTokenModalActive = false" height="50px">Close</v-btn>
    </v-card-actions>    
  </v-card>


</v-dialog>
   `,
  data: () => ({
    amount: '',
    address: '',
    loading: false,
  }),
}
