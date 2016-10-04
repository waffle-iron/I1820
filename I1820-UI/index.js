/*
 * +===============================================
 * | Author:        Parham Alvani (parham.alvani@gmail.com)
 * | Author:        Iman Tabrizian (tabrizian@outlook.com)
 * |
 * | Creation Date: 09-09-2016
 * |
 * | File Name:     index.js
 * +===============================================
 */

/* global Vue : Vue.js */
/* global io  : socket.io */
/* global $   : JQuery */

var app = new Vue({
  el: '#app',
  data: {
    rpis: {},
    connection: {
      message: 'Connecting...',
      state: 'default'
    },
    states: {
    }

  },
  created: function () {
    this.refresh()
    $('time.timeago').timeago()
  },
  updated: function () {
    $('time.timeago').timeago()
  },
  methods: {
    refresh: function () {
      $.get('discovery', function (data, status) {
        app.rpis = JSON.parse(data)
      })
    },
    turn: function (command) {
      var payload = {
        type: 'lamp',
        rpi_id: '066156d8-df62-5894-809b-d51ec5a2ff3d',
        device_id: '\u0000\u0013\u00a2\u0000@\u00c1\u00a9o',
        settings: {
          on: command
        }
      }
      $.ajax({
        url: 'thing',
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(payload)
      })
    },
    checkData: function () {
      return Object.keys(this.states).length
    }
  }
})

$('document').ready(function () {
  var socket = io.connect('http://' + document.domain + ':' + location.port)
  socket.on('connect', function () {
    app.connection.message = 'Connected'
    app.connection.state = 'success'
  })
  socket.on('error', function () {
    app.connection.message = 'Error :('
    app.connection.state = 'danger'
  })
  socket.on('log', function (message) {
    message = JSON.parse(message)
    for (var key in message.states) {
      if (message.states.hasOwnProperty(key)) {
        Vue.set(app.states, key, message.states[key])
      }
    }
  })
})