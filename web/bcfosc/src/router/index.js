import Vue from 'vue'
import Router from 'vue-router'
import Config from '../components/Config'
import Channel from '../components/Channel'
import Striplist from '../components/Striplist'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {path: '/', component: Config},
    {path: '/channel', component: Channel},
    {path: '/striplist', component: Striplist}
  ]
})
