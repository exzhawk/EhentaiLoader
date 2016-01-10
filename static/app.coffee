ehentaiLoaderApp = angular.module 'ehentaiLoaderApp', []

ehentaiLoaderApp.controller 'NavBar', ['$http', ($http) ->
  this.queue_count = 233
  this.download_count = 233
  this.search_keyword = ''
  this.do_search = ->
    $http
    .post('/search', q: this.search_keyword)
    .success ->
      console.log(233)
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




