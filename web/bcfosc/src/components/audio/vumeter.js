Vue.component('vu-meter', {
  template: '<span class="vu-meter"><canvas :width="width" :height="height" v-draw-meter="{ amp: dBVal, peak: dBPeakVal, clipSize: clipSize, showPeaks: showPeaks }"></canvas></span>',
  props: {
    val: {
      type: Number,
      default: 0
    },
    peakVal: {
      type: Number,
      default: 0
    },
    refreshRate: {
      type: Number,
      default: 100
    },
    clipSize: {
      type: Number,
      default: 10
    },
    width: {
      type: Number,
      default: 10
    },
    height: {
      type: Number,
      default: 150
    },
    showPeaks: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    dBVal: function() {
      return 20 * Math.log10(this.val);
    },
    dBPeakVal: function() {
      return 20 * Math.log10(this.peakVal);
    }
  },
  watch: {
    val: function(newVal, oldVal) {
      if (this.showPeaks) {
        var smoothingFactor = 50;
        if (newVal > this.peakVal) {
          this.peakVal = newVal;
        } else {
          this.peakVal = newVal * (1 / smoothingFactor) + this.peakVal * ((smoothingFactor - 1) / smoothingFactor);
        }
      }
    }
  },
  directives: {
    drawMeter: function(canvas, binding) {
      var clipSize = binding.value.clipSize;
      var showPeaks = binding.value.showPeaks;
      var amp = binding.value.amp / 76 + 1;
      var peak = binding.value.peak / 76 + 1;
      var w = canvas.width;
      var h = canvas.height;
      var hInRange = h - clipSize;
      var ctx = canvas.getContext("2d");
      var gradient = ctx.createLinearGradient(0, 0, 0, h);
      gradient.addColorStop(0, "red");
      gradient.addColorStop(clipSize / h, "orange");
      gradient.addColorStop(clipSize / h, "greenyellow");
      gradient.addColorStop(1, "lime");
      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = gradient;
      ctx.fillRect(0, h - hInRange * amp, w, hInRange * amp);
      if (showPeaks) {
        if (peak >= 1) {
          ctx.fillStyle = "red";
        } else {
          ctx.fillStyle = "greenyellow";
        }
        ctx.fillRect(0, Math.round(h - hInRange * peak), w, 1);
      }
      ctx.fillStyle = "white";
      ctx.fillRect(0, clipSize, w, 1);
    }
  }
});


// mock up some vaguely plausible fake audio signal
function fauxdio(f) {
  f ? f = f : f = 65;
  var now = Date.now();
  var lowwave = Math.sin(now / 1000 * Math.PI / 2 * f / 13.2);
  var basewave = Math.sin(now / 1000 * Math.PI / 2 * f) * 0.8;
  var midwave = Math.sin(now / 1000 * Math.PI / 2 * f * 5.73) * 0.6;
  var highwave = Math.sin(now / 1000 * Math.PI / 2 * f * 17) * 0.4;
  var lownoise = (Math.random() * 2 - 1) * 0.1;
  var peaks = Math.pow((Math.random() * 2 - 1), 4);
  return Math.abs((lowwave + basewave + midwave + highwave + lownoise + peaks) / 3);
}


setInterval(function() {
  vals = ["val0", "val1", "val2", "val3", "val4", "val5", "val6", "val7"];
  for (let i = 0; i < vals.length; i++) {
    var newVal = fauxdio(65 + i * i * 12);
    app[vals[i]] = newVal;
  }
}, 43);