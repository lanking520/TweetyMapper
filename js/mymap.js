/// </// <reference path="markers.js" />
/// </// <reference path="js/markerclusterer.js" />
var preUrl = "http://lowcost-env.xjjzsdshyn.us-east-1.elasticbeanstalk.com"
var app = angular.module('myapp',['ngMap','ngAnimate', 'ngSanitize', 'ui.bootstrap'])
app.controller('MyController', MapCtrl);

function Markerer (latLng, mmmap, tweet, sentiment){
          var infoWin = new google.maps.InfoWindow();
          var marker = new google.maps.Marker({
            position:latLng,
            icon:'http://maps.google.com/mapfiles/ms/icons/'+sentiment+'-dot.png'
          });
          google.maps.event.addListener(marker,'click', function(){
            infoWin.setContent(tweet);
            infoWin.setPosition(latLng);
            infoWin.open(mmmap);
          });
          return marker;
}

function updater(vm, $scope, $http, filters = null){
  vm.updateClusterer.clearMarkers();
  vm.markerClusterer.clearMarkers();
  vm.dynMarkers = [];
  obj = {"keyword":Object.keys($scope.words),"filter":filters};
  $http({
            url: preUrl+"/search",
            method: "POST",
            data: obj
        }).then(function (success){
          markers = success["data"]["result"];
          for (var i=0; i<markers.length; i++) {
            var latLng = new google.maps.LatLng(markers[i].position[1], markers[i].position[0]);
            vm.dynMarkers.push(Markerer(latLng, vm.map, markers[i].text,$scope.sentimentlib[markers[i].sentiment]));
          }
          vm.markerClusterer = new MarkerClusterer(vm.map, vm.dynMarkers, {});
        },function (error){console.log(error)});
}

function MapCtrl($http, $scope, $interval, NgMap){
    var vm = this;
    var updatetweet =function(){
      if(vm.updateMarkers.length > 0){
        $scope.hideupdate = false;
        $scope.numofupdates = vm.updateMarkers.length;
      }
        console.log(vm.updateMarkers);
       $http({
            url: preUrl+"/updates",
            method: "GET"
        }).then(function(success){
          markers = success["data"]["result"];
          if(markers.length > 0){
            for (var i=0; i<markers.length; i++) {
            var latLng = new google.maps.LatLng(markers[i].coordinates[1], markers[i].coordinates[0]);
            vm.updateMarkers.push(Markerer(latLng, vm.map, markers[i].text,$scope.sentimentlib[markers[i].sentiment]));
            }
            //vm.markerClusterer = new MarkerClusterer(vm.map, vm.dynMarkers, {});
          };},function (error){console.log(error)});
      }
    $scope.init = function(){
      $scope.oldwords = ["music", "food", "sport", "show", "movie", "car", "commercial", "party", "war", "hello"];
      $scope.words = {};
      NgMap.getMap().then(function(map) {
        vm.map = map;
      });
      $scope.hideupdate = true;
      vm.markerClusterer = new MarkerClusterer(vm.map, [], {});
      vm.updateClusterer = new MarkerClusterer(vm.map, [], {});
      $scope.sentimentlib = {"positive":"green","neutral":"blue","negative":"red"};
      vm.updateMarkers = [];
      $interval(updatetweet, 2000);
    };
    $scope.searchword = function(){
      if($scope.word != ""){
        $scope.words[$scope.word] = true;
        console.log($scope.words);
        updater(vm, $scope, $http);
      }
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
      //console.log($scope.words);
      if(Object.keys($scope.words).length === 0){
        vm.markerClusterer.clearMarkers();
      }
      else{
        updater(vm, $scope, $http);
      }
    };

    $scope.getpos = function(event) {
      Latlgn = [event.latLng.lng(),event.latLng.lat()];
      if(Object.keys($scope.words).length != 0){
        updater(vm, $scope, $http, Latlgn);
      }
    };

    $scope.fetchupdate = function() {
      $scope.words = {};
      vm.updateClusterer.clearMarkers();
      vm.markerClusterer.clearMarkers();
      vm.updateClusterer = new MarkerClusterer(vm.map, vm.updateMarkers, {});
      $scope.hideupdate = true;
      $scope.numofupdates = 0;
      vm.updateMarkers = [];
    };

};



