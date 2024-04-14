export default {
  components: {
  },
   template : `   
    <component is="style">
        #balance {
          font-size: 32px;
          font-weight: bold;
          margin-top: 20px;
          position: absolute;
          color: deeppink;        
        }
        #qr-code {
          width: 600px;
          height: 600px;
          margin: 3em auto;        
        }         
    </component>
    <div id="balance">Balance: {{$root.balance}} DC</div>      
    <qr-code 
    id="qr-code"
    contents="publicKey"
    position-ring-color="#13532d"
    position-center-color="#70c559"
    ></qr-code>
   `,
  data: () => ({
    db: null,
  }),
  methods:{

    initDB : async function() {
      // create DB with schema if it doesn't exist
      this.db = new Dexie("MyHashes");
      this.db.version(4).stores({
        hashes: null,
      })
      this.db.version(5).stores({
        hashes: `
        id++,
        public,
        private`,
      })
    },

    generateKeys : async function() {
      const rsa = new RSA()
      rsa.generateKeyPair(async function(keyPair) {

        // put new hash into db
        await self.db.hashes.put({
          public: keyPair.publicKey,
          private: keyPair.privateKey,
        })

      }, 4096)

    },
  },
  mounted: async function() {
    // initDB
    await this.initDB()
    self = this

    // get all hashes
    const hashes = await this.db.hashes.toArray()

    if (hashes.length === 0) {
      // create new public key and private key
      await this.generateKeys()
    } else {
      // use preexisting public key
      self.publicKey = hashes[0].public
    }
  },
}
