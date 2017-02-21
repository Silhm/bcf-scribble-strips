<template>
  <div class="config">
    <h1>Config</h1>
    <ul>
      <li><input type="text" v-bind:value="ip" placeholder="OSC server address"></li>
      <li><input type="text" v-bind:value="port" placeholder="OSC server address"></li>
      <li><button>Update values</button></li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'config',
  data () {
    return {
      msg: 'Welcome to OSC',
      ip: '127.0.0.1',
      port: 3819
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
