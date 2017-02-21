<template>
  <div class="wrapper" v-draw-pan="{ width : width, height: height, position: position}" >
    <canvas v-bind:width="width" v-bind:height="height"></canvas>
    <div>{{ lrPos }}</div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      position: 20,
      posLR: 'L50R50',
      percent: 0,
      ticks: new Array(28),
      minangle: 0,
      maxangle: 270,
      minvol: -200,
      maxvol: 6,
      mingain: -20,
      maxgain: 20
    }
  },
  props: {
    knobname: String,
    knobtype: {
      type: String,
      default: 'standard'
    },
    val: {
      type: Number,
      default: 0
    },
    width: {
      type: Number,
      default: 70
    },
    height: {
      type: Number,
      default: 25
    }
  },
  computed: {
    lrPos: function () {
      var lPos = 50 - this.position
      var rPos = 50 + this.position
      return 'L' + lPos + 'R' + rPos
    }
  },
  watch: {

  },
  directives: {
    drawPan: function (elem, binding) {
      var c = elem.querySelector('canvas')
      var ctx = c.getContext('2d')
      var middle = binding.value.width / 2
      var width = binding.value.width
      var height = binding.value.height
      var pos = ((binding.value.position + 50) * width / 100)

      // Initial display
      ctx.beginPath()
      ctx.moveTo(middle, 0)
      ctx.lineTo(middle, height)
      ctx.closePath()
      ctx.strokeStyle = 'green'
      ctx.stroke()

      ctx.beginPath()
      ctx.moveTo(middle, height / 2)
      ctx.lineTo(middle, height)
      ctx.lineTo(binding.value.position >= 0 ? width : 0, height)
      ctx.lineTo(binding.value.position >= 0 ? width : 0, 0)
      ctx.closePath()
      ctx.strokeStyle = 'green'
      ctx.fillStyle = 'green'
      ctx.fill()

      ctx.beginPath()
      ctx.moveTo(binding.value.position >= 0 ? pos : 0, 0)
      ctx.lineTo(binding.value.position >= 0 ? width : pos, 0)
      ctx.lineTo(binding.value.position >= 0 ? width : pos, height)
      ctx.lineTo(binding.value.position >= 0 ? pos : 0, height)
      ctx.moveTo(width, 0)
      ctx.closePath()
      ctx.fillStyle = 'black'
      ctx.fill()
    }
  },
  methods: {

  }
}
</script>
<style scoped>  
  
  
</style>
