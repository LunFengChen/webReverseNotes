r = {
	    randomBytes: function(t) {
                for (var e = []; t > 0; t--)
                    e.push(Math.floor(256 * Math.random()));
                return e
            },
            bytesToWords: function(t) {
                for (var e = [], n = 0, r = 0; n < t.length; n++,
                r += 8)
                    e[r >>> 5] |= t[n] << 24 - r % 32;
                return e
            },
            wordsToBytes: function(t) {
                for (var e = [], n = 0; n < 32 * t.length; n += 8)
                    e.push(t[n >>> 5] >>> 24 - n % 32 & 255);
                return e
            },
            bytesToHex: function(t) {
                for (var e = [], n = 0; n < t.length; n++)
                    e.push((t[n] >>> 4).toString(16)),
                    e.push((15 & t[n]).toString(16));
                return e.join("")
            },
            hexToBytes: function(t) {
                for (var e = [], n = 0; n < t.length; n += 2)
                    e.push(parseInt(t.substr(n, 2), 16));
                return e
            },
            bytesToBase64: function(t) {
                for (var n = [], r = 0; r < t.length; r += 3)
                    for (var o = t[r] << 16 | t[r + 1] << 8 | t[r + 2], i = 0; i < 4; i++)
                        8 * r + 6 * i <= 8 * t.length ? n.push(e.charAt(o >>> 6 * (3 - i) & 63)) : n.push("=");
                return n.join("")
            },
            base64ToBytes: function(t) {
                t = t.replace(/[^A-Z0-9+\/]/ig, "");
                for (var n = [], r = 0, o = 0; r < t.length; o = ++r % 4)
                    0 != o && n.push((e.indexOf(t.charAt(r - 1)) & Math.pow(2, -2 * o + 8) - 1) << 2 * o | e.indexOf(t.charAt(r)) >>> 6 - 2 * o);
                return n
            }
}