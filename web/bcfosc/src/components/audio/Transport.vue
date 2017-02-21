<template>
  <div class="transport">
    <div class="bg">
      <div class="display">
        <div class="time">
          00:00:01:29
        </div>
        <div class="beat">
          <span class="beat-val">000|00|0000</span>
          <div class="beat-info">
            <span class="bpm">120</span>
            <span class="sig">4/4</span>
          </div>
          
        </div>
      </div>
      
      <div class="transport-control">
        <div class="control stop">S</div>
        <div class="control play active">P</div>
        <div class="control rewind">«</div>
        <div class="control forward">»</div>
      </div>
      
    </div>
    
  </div>
</template>

<script>

</script>
<style scoped>  
  @font-face {
	font-family: 'liquid_crystal';
	src: url('/static/liquid-crystal-bold.otf');
  }
  
  .transport{
    width: 720px;
    height: 150px;
    background: url(images/transport_bg.png) no-repeat;
  }
  
  .bg{
    /*position: absolute; */
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }
  .display{
    background: #392323;
    color: #ad2528;
    font-family: 'liquid_crystal'; /* no .ttf */
    position: relative;
    font-size: 1.5em;
    display: flex;
    justify-content: space-around;
    width: 370px;
    height: 50px;
    box-shadow: 1px 2px 9px 3px rgba(0, 0, 0, 0.24);
  }
  
  .beat{
    display: flex;
  }
  .bpm, .sig{
    display: block;
   font-size: 0.5em; 
  }
 
  .beat-info{
        margin-left: 5px;
  }
  
  .transport-control{
        display: flex;
  }
  .control{
    background: url(images/trans_button.png);
    width: 55px;
    height: 55px;
  }
  .control.active{
    background-position:  0 -62px;
  }
  
</style>
