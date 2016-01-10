ehentaiLoaderApp = angular.module 'ehentaiLoaderApp', []

ehentaiLoaderApp.controller 'NavBar', ['$http', ($http) ->
  this.queue_count = 0
  this.download_count = 0
  this.search_keyword = ''
  this.search_result = []
  search_result = this.search_result
  this.do_search = ->
    $http
    .post('/search', q: this.search_keyword)
    .success (data) ->
      search_result=data['posts']
  this
]

ehentaiLoaderApp.controller 'LoginModal', ['$http', ($http) ->
  this.username = ''
  this.password = ''
  $loginModal = $ '#loginModal'
  $loginModal.modal backdrop: 'static'
  this.do_login = ->
    console.log(this.username)
    if this.username.length == 0
      $http
      .get '/login'
      .success (data) ->
        if data['isLogin']
          $loginModal.modal 'hide'
        else
          console.log('notlogin')
    else
      $http
      .post '/login',
        username: this.username
        password: this.password
      .success (data) ->
        if data['isLogin']
          $loginModal.modal 'hide'
        else
          console.log('loginfail')
  this
]




