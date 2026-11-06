(function exposeCipher(root) {
  "use strict";
  const LFSR_PERIOD_BITS = 0xffff;

  function nextBit(state) {
    const outputBit = state & 1;

    const feedback =
      ((state >> 0) & 1) ^
      ((state >> 2) & 1) ^
      ((state >> 3) & 1) ^
      ((state >> 5) & 1);

    const nextState = (state >> 1) | (feedback << 15);

    return [outputBit, nextState];
 
  }

  function keystream(length, seed, offset = 0) {
    if (!Number.isInteger(seed) || seed < 1 || seed > 0xffff) throw new RangeError("invalid seed");
    if (!Number.isInteger(length) || length < 0 || !Number.isInteger(offset) || offset < 0) {
      throw new RangeError("invalid length or offset");
    }
    let state = seed;
    const output = new Uint8Array(length);

    const skipBits = (offset % LFSR_PERIOD_BITS) * 8;

    for (let k = 0; k < skipBits; k++) {
      state = nextBit(state)[1];
    }

    for (let i = 0; i < length; i++) {
      let byteValue = 0;

      for (let j = 0; j < 8; j++) {
        const [bit, next] = nextBit(state);
        state = next;
        byteValue = (byteValue << 1) | bit;
      }
      output[i] = byteValue;
    }
    return output;
  }




  function xorBytes(data, seed, offset = 0) {
    const key = keystream(data.length, seed, offset);
    const result = new Uint8Array(data.length);

    for (let i = 0; i < data.length; i++) {
      result[i] = data[i] ^ key[i];
   }
    return result;  
  }

  const cipher = { keystream, xorBytes };
  root.LfsrCipher = cipher;
  if (typeof module !== "undefined") module.exports = cipher;
}(typeof self !== "undefined" ? self : globalThis));
