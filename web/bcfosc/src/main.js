// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import Knob from './components/audio/Knob'
import router from './router'

/* eslint-disable no-new */
window.bcfosc = new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App, Knob },
  data: {
    on: null,
    send: null
  },
  methods: {
    connectOSC: function (ip, port) {
      window.socket = typeof window.io !== 'undefined' ? window.io.connect(ip, {port: port, rememberTransport: false}) : false
      if (window.socket) {
        this.on = window.socket.on
        this.send = window.socket.emit
        return true
      } else {
        console.error('Cannot handle', arguments[0], 'since the socket connection cannot be established')
        return true
      }
    }
  }
})

var bcfosc = window.bcfosc
bcfosc.connectOSC('http://127.0.0.1', 8081)
bcfosc.on('connect', function () {
  // sends to socket.io server the host/port of oscServer
  // and oscClient
  bcfosc.send('config', {
    server: {
      port: 3333,
      host: '127.0.0.1'
    },
    client: {
      port: 3819,
      host: '127.0.0.1'
    }
  })
  bcfosc.send('message', '/set_surface/feedback 4087')
})

// Message handler
bcfosc.on('message', function (obj) {
  // console.log(obj)
  bcfosc.$emit('message', obj)
})
