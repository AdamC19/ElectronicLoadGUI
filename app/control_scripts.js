var app = angular.module('loadApp', []);

app.controller('loadAppCtl', function($scope) {
    $scope.socket = io();

    $scope.load = {
        connected: true,
        voltage: 0.0,
        current: 0.0,
        resistance: 0.0,
        power: 0.0
    };

    $scope.socket.on('update', function(data){
        $scope.$apply(function(){
            $scope.load.voltage = data.voltage;
            $scope.load.current = data.current;
            $scope.load.resistance = data.resistance;
            $scope.load.power = data.power;
        });
    });

    $scope.setCurrent = function() {
        config = {current: parseFloat($scope.load.current_setpt)};
        $scope.socket.emit('configure', config);
    };
});