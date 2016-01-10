app = new Vue({
  el: 'body'
  data:
    queueCount: 233
    downloadCount: 233
    searchKeyword: ''
    searchResult: []
    username: ''
    password: ''
    isLogin: false
  computed:
    noLogin: ->
      return !this.isLogin
  methods:
    init: ->
      this.checkLogin()
    doSearch: ->
      $.ajax
        url: '/search'
        data:
          q: this.searchKeyword
        method: "GET"
        dataType: "json"
        success: (data) ->
          this.searchResult = data['posts']
    checkLogin: ->
      $this = this
      $.ajax
        url: '/login'
        method: "GET"
        dataType: "json"
        success: (data) ->
          $this.isLogin = data['isLogin']
    doLogin: ->
      $this = this
      $.ajax
        url: '/login'
        data:
          username: this.username
          password: this.password
        method: "POST"
        dataType: "json"
        success: (data) ->
          $this.isLogin = data['isLogin']
})

app.init()