/// </// <reference path="angular.min.js" />
/// </// <reference path="markers.js" />
/// </// <reference path="js/markerclusterer.js" />
var app = angular.module('ngMap')
app.controller('MyController', function($http, $interval, NgMap) {
    var vm = this;
    vm.dynMarkers = [];
    NgMap.getMap().then(function(map) {
      for (var i=0; i<1000; i++) {
        var latLng = new google.maps.LatLng(markers[i].position[0], markers[i].position[1]);
        vm.dynMarkers.push(new google.maps.Marker({position:latLng}));
      }
      vm.markerClusterer = new MarkerClusterer(map, vm.dynMarkers, {});
    });
  });