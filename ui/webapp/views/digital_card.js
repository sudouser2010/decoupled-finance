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

    createRandomString: function(length=10) {
      const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
      let result = ""
      const randomArray = new Uint8Array(length)
      crypto.getRandomValues(randomArray)

      randomArray.forEach((number) => {
        result += chars[number % chars.length];
      })
      return result
    },


    generateKeys : async function() {
      const name = `${self.createRandomString()} ${self.createRandomString()}`
      const email = `${self.createRandomString()}@${self.createRandomString()}`
      const passphrase = self.createRandomString(20)

      const { privateKey, publicKey, revocationCertificate } = await openpgp.generateKey({
          type: 'ecc', // Type of the key, defaults to ECC
          curve: 'curve25519', // ECC curve name, defaults to curve25519
          userIDs: [{ name, email }], // you can pass multiple user IDs
          passphrase: passphrase, // protects the private key
          format: 'armored' // output key format, defaults to 'armored' (other options: 'binary' or 'object')
      })

      // put new hash into db
      await this.db.hashes.put({
        public: publicKey,
        private: privateKey,
        passphrase: passphrase,
      })
    },
  },
  mounted: async function() {
    // initDB
    await this.initDB()

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
