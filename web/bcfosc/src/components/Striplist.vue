<template>
    <div class="striplist">
      <transport></transport>
      <div v-for="strip in stripList" class="strip">
        <vumeter :meterval="strip.meter" :clip="strip.clip"></vumeter>
        <div class="top">
          <div class="strip-name">
            <span class="id">{{ strip.id }}</span>
              {{ strip.name }}
          </div>
          <div class="strip-display">
            <pan>L50R50</pan>
          </div>
          &nbsp;
        </div>
        <div class="bottom">
            <div class="strip-status">
                <div class="status rec" v-bind:class="{ active: strip.status.rec }"></div>
                <hr/>
                <div class="status solo" v-bind:class="{ active: strip.status.solo }"></div>
            </div>
           <div class="strip-status">
            <div class="status phase" v-bind:class="{ active: strip.phase }"></div>
            <div class="status mute" v-bind:class="{ active: strip.status.mute }"></div>
          </div>
             
        </div>
      </div>
    </div>
</template>

<script>
import Pan from './audio/Pan'
import Vumeter2 from './audio/Vumeter2'

export default {
  name: 'striplist',
  data () {
    return {
      msg: 'hello',
      stripList: {
        '1': {
          id: 1,
          name: 'Kick',
          meter: Math.floor(Math.random() * 65536),
          phase: false,
          clip: false,
          status: {
            mute: false,
            solo: true,
            rec: true
          }
        },
        '2': {
          id: 2,
          name: '-',
          meter: Math.floor(Math.random() * 65536),
          phase: true,
          clip: true,
          status: {
            mute: true,
            solo: false,
            rec: false
          }
        },
        '3': {
          id: 3,
          name: '-',
          meter: Math.floor(Math.random() * 65536),
          phase: false,
          clip: false,
          status: {
            mute: false,
            solo: false,
            rec: false
          }
        },
        '4': {
          id: 4,
          name: '-',
          meter: Math.floor(Math.random() * 65536),
          phase: false,
          clip: false,
          status: {
            mute: false,
            solo: false,
            rec: false
          }
        },
        '5': {
          id: 5,
          name: '-',
          meter: Math.floor(Math.random() * 65536),
          phase: false,
          clip: false,
          status: {
            mute: false,
            solo: false,
            rec: false
          }
        },
        '6': {
          id: 6,
          name: '-',
          meter: Math.floor(Math.random() * 65536),
          phase: false,
          clip: false,
          status: {
            mute: false,
            solo: false,
            rec: false
          }
        },
        '7': {
          id: 7,
          name: '-',
          meter: Math.floor(Math.random() * 65536),
          phase: false,
          clip: false,
          status: {
            mute: false,
            solo: false,
            rec: false
          }
        },
        '8': {
          id: 8,
          name: '-',
          meter: Math.floor(Math.random() * 65536),
          phase: false,
          clip: false,
          status: {
            mute: false,
            solo: false,
            rec: false
          }
        }
      }
    }
  },
  created: function () {
    this.$root.$on('message', function (message) {
      this.stripList[1].name = message
    }.bind(this))
  },
  components: {
    pan: Pan,
    vumeter: Vumeter2
  },
  methods: {
    handleMessage: function (obj) {
      var query = obj[0]
      var value = obj[1]

      if (query.indexOf('/strip/name/') >= 0) {
        var chId = parseInt(query.replace('/strip/name/', ''))
        this.stripList[chId] = {
          name: value,
          id: chId
        }
        this.stripList[chId].name = value
      } else if (query.indexOf('/strip/mute/') >= 0) {
        var muteId = parseInt(query.replace('/strip/mute/', ''))
        this.stripList[muteId].status.mute = value === 1
      } else if (query.indexOf('/strip/solo/') >= 0) {
        var soloId = parseInt(query.replace('/strip/solo/', ''))
        this.stripList[soloId].status.solo = value === 1
      } else if (query.indexOf('/strip/recenable/') >= 0) {
        var recId = parseInt(query.replace('/strip/recenable/', ''))
        this.stripList[recId].status.rec = value === 1
      }
    }
  }
}
fauxdio(3)
// mock up some vaguely plausible fake audio signal
function fauxdio (f) {
  if (!f) {
    f = 65
  }
  var now = Date.now()
  var lowwave = Math.sin(now / 1000 * Math.PI / 2 * f / 13.2)
  var basewave = Math.sin(now / 1000 * Math.PI / 2 * f) * 0.8
  var midwave = Math.sin(now / 1000 * Math.PI / 2 * f * 5.73) * 0.6
  var highwave = Math.sin(now / 1000 * Math.PI / 2 * f * 17) * 0.4
  var lownoise = (Math.random() * 2 - 1) * 0.1
  var peaks = Math.pow((Math.random() * 2 - 1), 4)
  return Math.abs((lowwave + basewave + midwave + highwave + lownoise + peaks) / 3)
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .strip{
    text-align:left;

    float: left;
    margin:2px;
  }

  .top{
     background: url(./images/strips/mcp_bg_top.png) no-repeat;
  }
  .bottom{
    padding: 15px 0;
     background: url(./images/strips/mcp_bg_bottom.png) no-repeat;
  }


  .strip-display{
      background:#000000;   
      padding: 3px;
      overflow:hidden;
      color: white;
      opacity: 0.8;
      padding-top: 17px;
      padding-bottom: 17px;
      text-align: center;
  }
  .strip-name{
      font-size: 1.2em;
      color: #f4f4f4;
      padding: 0;

  }
  .strip-name .id{
      background: #181818;
      color: #f4f4f4;
      position: relative;
      padding: 0 3px;
      left: 0;
      top: 1px;
      border-bottom-right-radius: 7px;
      border-top-right-radius: 7px;
    }


  .strip-status{
    text-align: center;
    margin: 2px;
    font-size:0.8em;
    color: black;
    opacity: 0.8;
  }
  .status{
      /*border: 1px solid rgba(128, 128, 128, 0.5);*/
      padding:1px;
      border-radius:2px;
  }


  .status.active{
     /* border: 1px solid #ffffff;*/
  }
  .status.active .fa{
      color:#ff0000;
  }



  .status.solo{
    display: inline-block;
    background: url(images/strips/solo.png);
    width: 34px;
    height: 32px;
  }
  .status.solo.active{
    background-position: 0 -36px;
  }

  .status.mute{
    display: inline-block;
    background: url(images/strips/mute.png);
    width: 26px;
    height: 30px;
  }
  .status.mute.active{
    background-position: 0 -34px;
  }
  
  .status.rec{
        margin: 0 auto;
    background: url(images/strips/arm.png);
    width: 32px;
    height: 20px;
  }
  .status.rec.active{
    background-position: 0 -22px;
  }
  
  .status.phase{
    display: inline-block;
    background: url(images/strips/phase.png);
    width: 26px;
    height: 32px;
  }
  .status.phase.active{
    background-position: 0 -36px;
  }
  
  
</style>
