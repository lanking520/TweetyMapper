/// </// <reference path="markers.js" />
/// </// <reference path="js/markerclusterer.js" />
var preUrl = "http://127.0.0.1:5000"
var app = angular.module('myapp',['ngMap','ngAnimate', 'ngSanitize', 'ui.bootstrap'])
app.controller('MyController', MapCtrl);

function Markerer (latLng, mmmap, tweet){
          var infoWin = new google.maps.InfoWindow();
          var marker = new google.maps.Marker({position:latLng});
          google.maps.event.addListener(marker,'click', function(){
            infoWin.setContent(tweet);
            infoWin.setPosition(latLng);
            infoWin.open(mmmap);
          });
          return marker;
}

function updater(vm, $scope, $http){
  vm.markerClusterer.clearMarkers();
  vm.dynMarkers = [];
  $http({
            url: "/search",
            method: "POST",
            data: {"keyword":Object.keys($scope.words)}
        }).then(function (success){
          markers = success["data"]["result"];
          for (var i=0; i<markers.length; i++) {
            var latLng = new google.maps.LatLng(markers[i].position[1], markers[i].position[0]);
            vm.dynMarkers.push(Markerer(latLng, vm.map, markers[i].text));
          }
          vm.markerClusterer = new MarkerClusterer(vm.map, vm.dynMarkers, {});
        },function (error){console.log(error)});
}

function MapCtrl($http, $scope, NgMap){
    var vm = this;
    $scope.init = function(){
      $scope.oldwords = ["music", "food", "sport", "show", "movie", "car", "commercial", "party", "war", "hello"];
      $scope.words = {};
      NgMap.getMap().then(function(map) {
        vm.map = map;
      });
      vm.markerClusterer = new MarkerClusterer(vm.map, [], {});
    };
    $scope.searchword = function(){
      $scope.words[$scope.word] = true;
      console.log($scope.word);
      console.log($scope.words);
      updater(vm, $scope, $http);
    };
      // Implement a HTTP Getter in here namely markers
      // Sample data format see in markers.js

    $scope.searchold = function(oldword){
      $scope.words = {};
      $scope.words[oldword] = true;
      updater(vm, $scope, $http);
    }

    $scope.deleteword = function(word){
      delete $scope.words[word];
      console.log($scope.words);
      if(Object.keys($scope.words).length === 0){
        return;
      }
      else{
        updater(vm, $scope, $http);
      }
    };
};



