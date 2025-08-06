const sm2 = require('sm-crypto').sm2
const sm4 = require('sm-crypto').sm4

function encrypt(pageIndex, nonceStr) {
  info = `param=&page=${pageIndex}&size=10`
  sm4EncryptKey = 'dbb78b8b64d640bb130255c69e959973'
  timestamp = Date.now()
  queryContent = sm4.encrypt(info, sm4EncryptKey)
  params = `appId=27IGtFrNFDc&encryptType=SM4&nonceStr=${nonceStr}&queryContent=${queryContent}&signType=SM2&timestamp=${timestamp}&version=1.0`
  privateKey = '7faa61bb9051707ad9d9d2c417d61e038a3af871a61c8da534a9061ac1e51c32'
  publicKey = '040f5940c99c46ee9e438487c6a41d880b93f0804ea0e5ef53a062bb08203fc2a675b3d2b7a9aeb1862bb1b8fa5d17a40e300cbbe9a470ee3bf89b4ccb1c899719'
  id = '27IGtFrNFDc'
  mode = {
    hash: !0,
    publicKey: publicKey,
    userId: id
  }
  return {
    'queryContent': queryContent,
    'timestamp': timestamp,
    'nonce': nonceStr,
    'sign': sm2.doSignature(params, privateKey, mode)
  }
}


var res = encrypt("appId=27IGtFrNFDc&encryptType=SM4&nonceStr=8b444fe706d546a79e5150d4b90f2d66&queryContent=f8e3735a2bc6b0b110636dbca6f6059631244ee277cc8ef5d7df2e4ad5afd7b9&signType=SM2&timestamp=1753879324035&version=1.0")
console.warn(res)