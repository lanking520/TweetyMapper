/// </// <reference path="angular.min.js" />
/// </// <reference path="markers.js" />
/// </// <reference path="js/markerclusterer.js" />
var app = angular.module('ngMap')
app.controller('MyController', function($http, $scope, $interval, NgMap) {
    var vm = this;
    $scope.init = function(){
      $scope.words = {}
      NgMap.getMap().then(function(map) {
        vm.map = map;
      });
      vm.markerClusterer = new MarkerClusterer(vm.map, [], {});
    };
    $scope.searchword = function(){
      $scope.words[$scope.word] = true;
      vm.markerClusterer.clearMarkers();
      vm.dynMarkers = [];
      // Implement a HTTP Getter in here namely markers
      // Sample data format see in markers.js
      for (var i=0; i<markers.length; i++) {
        var latLng = new google.maps.LatLng(markers[i].position[1], markers[i].position[0]);
        vm.dynMarkers.push(new google.maps.Marker({position:latLng}));
      }
      vm.markerClusterer = new MarkerClusterer(vm.map, vm.dynMarkers, {});
    };
    $scope.deleteword = function(word){
      delete $scope.words[word];
      };
});