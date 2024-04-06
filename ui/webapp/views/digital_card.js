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
ab2str: function (buf) {
  return String.fromCharCode.apply(null, new Uint8Array(buf));
},

/*
Export the given key and write it into the "exported-key" space.
*/
exportCryptoKey: async function(key) {
  const exported = await window.crypto.subtle.exportKey("spki", key);
  const exportedAsString = this.ab2str(exported);
  const exportedAsBase64 = window.btoa(exportedAsString);
  const pemExported = `-----BEGIN PUBLIC KEY-----\n${exportedAsBase64}\n-----END PUBLIC KEY-----`;

 return pemExported
},

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

    // ab2b64: function(arrayBuffer) {
    //     return window.btoa(String.fromCharCode.apply(null, new Uint8Array(arrayBuffer)))
    // },
    generateKeys : async function() {


// const keyPairaa = await window.crypto.subtle.generateKey(
//     {
//       name: "RSA-OAEP",
//       // Consider using a 4096-bit key for systems that require long-term security
//       modulusLength: 2048,
//       publicExponent: new Uint8Array([1, 0, 1]),
//       hash: "SHA-256",
//     },
//     true,
//     ["encrypt", "decrypt"],
//   )
//       debugger
//           const foo = await this.exportCryptoKey(keyPairaa.privateKey);
//     console.log(foo)
//     alert(foo)


const aa = await window.crypto.subtle
  .generateKey(
    {
      name: "ECDSA",
      namedCurve: "P-384",
    },
    true,
    ["sign", "verify"],
  )
      const aa1 = await this.exportCryptoKey(aa.privateKey);
      console.log(aa1)
    alert(aa1)

  // Generate key pair
      const keypair = await window.crypto.subtle.generateKey(
          {
              name: "ECDSA",
              namedCurve: "P-256", // secp256r1
          },
          true,
          ["sign", "verify"]
      )
      debugger
      // convert public key from object to array buffer
      let publicKey = await window.crypto.subtle.exportKey(
        "spki",
        keypair.publicKey
      )
      // convert public key from arraybuffer to string
      publicKey = this.ab2b64(publicKey)


      // let privateKey2 = await window.crypto.subtle.exportKey(
      //   "spki",
      //   keypair.privateKey
      // )
      // debugger
      // let publicKey = keypair.publicKey
      let privateKey = keypair.privateKey

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
