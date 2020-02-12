'use strict';

angular.module('userRegistration').
    controller('UserRegistrationController', ["$scope", function($scope) {
        var self = this;
        self.firstName = "";
        self.lastName = "";
        self.username = "";
        self.password1 = "";
        self.password2 = "";

        $scope.$watch("password1", function(newValue, oldValue) {
            if(newValue === oldValue) {
                return;
            }
            $scope.$broadcast("pwUpdated", newValue);
        });
    }]);
