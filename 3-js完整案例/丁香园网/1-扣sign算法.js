a = function (t) {
  o = {
    stringToBytes: function (t) {
      e = {
        bin: {
          stringToBytes: function (t) {
            for (var e = [], n = 0; n < t.length; n++) e.push(255 & t.charCodeAt(n));
            return e;
          }
        }
      };
      return e.bin.stringToBytes(unescape(encodeURIComponent(t)));
    }
  };
  r = {
    bytesToWords: function (t) {
      for (var e = [], n = 0, r = 0; n < t.length; n++, r += 8) e[r >>> 5] |= t[n] << (24 - (r % 32));
      return e;
    }
  };
  t.constructor == String
    ? (t = o.stringToBytes(t))
    : void 0 !== u && "function" == typeof u.isBuffer && u.isBuffer(t)
    ? (t = Array.prototype.slice.call(t, 0))
    : Array.isArray(t) || (t = t.toString());
  var e = r.bytesToWords(t),
    n = 8 * t.length,
    i = [],
    a = 1732584193,
    c = -271733879,
    s = -1732584194,
    f = 271733878,
    l = -1009589776;
  (e[n >> 5] |= 128 << (24 - (n % 32))), (e[(((n + 64) >>> 9) << 4) + 15] = n);
  for (var p = 0; p < e.length; p += 16) {
    for (var h = a, y = c, d = s, g = f, v = l, m = 0; m < 80; m++) {
      if (m < 16) i[m] = e[p + m];
      else {
        var b = i[m - 3] ^ i[m - 8] ^ i[m - 14] ^ i[m - 16];
        i[m] = (b << 1) | (b >>> 31);
      }
      var E =
        ((a << 5) | (a >>> 27)) +
        l +
        (i[m] >>> 0) +
        (m < 20 ? ((c & s) | (~c & f)) + 1518500249 : m < 40 ? (c ^ s ^ f) + 1859775393 : m < 60 ? ((c & s) | (c & f) | (s & f)) - 1894007588 : (c ^ s ^ f) - 899497514);
      (l = f), (f = s), (s = (c << 30) | (c >>> 2)), (c = a), (a = E);
    }
    (a += h), (c += y), (s += d), (f += g), (l += v);
  }
  return [a, c, s, f, l];
};

s = function (t, e) {
  var r = {
    wordsToBytes: function (t) {
      for (var e = [], n = 0; n < 32 * t.length; n += 8) e.push((t[n >>> 5] >>> (24 - (n % 32))) & 255);
      return e;
    }
  };

  var n = r.wordsToBytes(a(t));
  r = {
    bytesToHex: function (t) {
      for (var e = [], n = 0; n < t.length; n++) e.push((t[n] >>> 4).toString(16)), e.push((15 & t[n]).toString(16));
      return e.join("");
    }
  };

  return e && e.asBytes ? n : e && e.asString ? i.bytesToString(n) : r.bytesToHex(n);
};

function calc_sign(str) {
  return s(str);
}

var str = "1";
var res = calc_sign("1");
console.log(`[*] calc_sign: ${str} -> ${res}`);
