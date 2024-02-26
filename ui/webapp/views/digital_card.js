export default {
  components: {
  },
   template : `   
    <div>Balance: 0 DC</div>   
    <qr-code 
    id="qr-code"
    contents="publicKey"
    position-ring-color="#13532d"
    position-center-color="#70c559"
    style="
    width: 600px;
    height: 600px;
    margin: 2em auto;
  "
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
      // todo: generate public and private keys via crypto library
      let publicKey = 'publicKey'
      let privateKey = 'privateKey'
      self.publicKey = publicKey

      // put new hash into db
      await this.db.hashes.put({
        public: publicKey,
        private: privateKey,
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
