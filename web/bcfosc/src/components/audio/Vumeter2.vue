<template>
  <div v-draw-meter="{ width : width, height: height, meterval:meterval, maxmeterval:maxmeterval, clip:clip}" class="meter-wrapper">
    <canvas v-bind:width="width" v-bind:height="height"></canvas>
    <div class="val-display">{{ dbVal }}dB</div>
</template>

<script>
export default {
  data () {
    return {
      dbVal: -42
    }
  },
  props: {
    meterval: {
      type: Number,
      default: 0
    },
    maxmeterval: {
      type: Number,
      default: 65535
    },
    clip: false,
    width: {
      type: Number,
      default: 17
    },
    height: {
      type: Number,
      default: 173
    }
  },
  watch: {
    meterval: function (newVal, oldVal) {
      console.log(oldVal)
    }
  },
  directives: {
    drawMeter: function (elem, binding) {
      var width = binding.value.width
      var height = binding.value.height
      var crop = binding.value.meterval * height / binding.value.maxmeterval
      var c = elem.querySelector('canvas')
      var ctx = c.getContext('2d')
      // Load both BG and Meter
      var bgImg = new Image()
      bgImg.onload = function () {
        ctx.drawImage(bgImg, 0, 0, width, height, 0, 0, width, height)
        // (img,sx,sy,swidth,sheight,x,y,width,height);
      }
      if (binding.value.clip) {
        bgImg.src = '/static/meter_bg_clip.png'
      } else {
        bgImg.src = '/static/meter_bg.png'
      }
      var meterImg = new Image()
      meterImg.onload = function () {
        ctx.drawImage(meterImg, 0, height - crop, width, height, 0, height - crop, width, height)
      }
      meterImg.src = '/static/meter_strip.png'
    }
  }
}
</script>
<style scoped>
  .meter-wrapper{
    margin: 10px auto;
    text-align: center;
  }
  
  .val-display{
    background: url("../images/strips/db_display.png") no-repeat;
    color: rgba(255, 255, 255, 0.77);
    font-size: 0.8em;
    height: 18px;
    width: 57px;
    text-align: center;
    margin: 0 auto;
    padding-top: 7px;
  }
   
  
</style>
