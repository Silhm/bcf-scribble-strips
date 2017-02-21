<template>
    <div class="channel">
        <header class="channel-name">auie {{ strip.name }} ({{strip.id}}) </header>
        <content>
            <div class="section input">
                <div>Input</div>
                <!--vu-meter :val="strip.vumeter.in" show-peaks></vu-meter-->
                <knob :val="strip.gain" knobname="Gain" knobtype="trim"></knob> 
                <div class="gain">Gain {{ strip.gain }} </div>
                <div class="phase" v-bind:class="{ revert : strip.polarity }"> &oslash; </div>

            </div>
            <div class="section main-screen">Main screen</div>
            <div class="section output">
                <div>Output</div>
                <!--vu-meter :val="strip.vumeter.out" show-peaks></vu-meter-->
                <knob :val="strip.volume" knobname="Volume" knobtype="vol"></knob> 
                <div class="volume">Volume {{ strip.volume }}</div>
                <!--knob :val="strip.pan" knobname="Pan" knobType="panKnob"></knob--> 
                <knob :val="strip.pan" knobname="Pan" knobtype="pan"></knob> 
                <div class="pan">Pan {{ strip.pan }}</div>
            </div>
        </content>
        <footer> {{ strip.comment }} </footer>
    </div>
</template>

<script>
import Knob from './audio/Knob'

export default {
  name: 'channel',
  data () {
    return {
      strip: {
        id: 0,
        name: '-',
        comment: '-',
        status: {
          mute: false,
          solo: false,
          rec: false
        },
        gain: 0,
        volume: 0,
        pan: 0.5,
        polarity: 0,
        signal: 0,
        vumeter: {
          in: 0,
          out: 0
        }
      }
    }
  },
  components: {
    knob: Knob
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


.all-view{
    width:100%;
    height:30%;
}


header{
    text-align: left;
    padding-left: 15px;
    font-size: 1.7em;
}
content{
    background-color: #282828;
    color:#e9e9e9;
    display: flex;
    padding: 15px;
}
.section{
     background-color: #0a0a0a;
     text-align: center;
     margin:5px;
     padding: 3px;
}
.main-screen{
    flex: 1;
}

.input, .output{
    width: 100px;
}

.phase{
    font-size: 1.7em;
    font-weight: bold;
}
.phase.revert{
    text-shadow: 0px 0px 15px rgba(168, 216, 248, 1);
    color: rgb(168, 216, 248);
}

  
  
  
  
  
</style>
