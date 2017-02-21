<template>
  <div id="app">
    <nav>
      <router-link to="/" exact>
        Config
      </router-link>
      <router-link to="/channel" exact>Channel</router-link>
      <router-link to="/striplist" exact>Strips</router-link>
      <span v-on:click="demomode=toggleDemo()">Demo mode {{ demomode? 'Enabled':'Disabled' }}</span>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script src="http://127.0.0.1:8081/socket.io/socket.io.js"></script>

<script>
// var socket = require('http://127.0.0.1:8081/socket.io/socket.io.js')
// console.log(socket)
export default {
  name: 'app',
  data: function () {
    return {
      demomode: false,
      osc: null
    }
  },
  methods: {
    toggleDemo: function () {
      this.demomode = !this.demomode
      window.demomode = this.demomode
      return this.demomode
    },
    connectOSC: function () {
      this.osc = (function (my) {
        my.socket = typeof window.io !== 'undefined' ? window.io.connect('http://127.0.0.1', {port: 8081, rememberTransport: false}) : false
        if (my.socket) {
          my.on = my.socket.on
        } else {
          my.on = function () {
            console.error('Cannot handle', arguments[0], 'since the socket connection cannot be established')
          }
        }
        return my
      }(this.osc || {}))
    }
  }
}
</script>

<style>
  
  body {
    background-color: #181818;
    font-size: 100%;
    font-family: "Open Sans", sans-serif;
    color: #aaa;
    text-align: center;
    background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAgAElEQ…9fnwOAqVOnkndOnz5NeOXzfgmhdy2e0h1YALB48WKGz6/yf8RxFhxL0FjRAAAAAElFTkSuQmCC");
    margin:0px;
  }
 
  
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
  
  .red{
    color:#d32626;
  }
  .red-bg{
    background-color:#d32626;
  }
  .green{
    color:#7cc732;
  }
  .green-bg{
    background-color:#7cc732;
  }
  .blue{
    color:#327cc7;
  }
  .blue-bg{
    background-color:#327cc7;
  }

  nav .router-link{
    
  }
  

</style>
