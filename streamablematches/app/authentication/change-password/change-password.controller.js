'use strict';

angular.
    module('changePassword').
    controller('ChangePasswordController', ['$scope', function($scope) {
        var self = this;
        self.old_password = "";
        self.new_password1 = "";
        self.new_password2 = "";

        $scope.$watch("new_password1", function(newValue, oldValue) {
            if(newValue === oldValue) {
                return;
            }
            $scope.$broadcast("pwUpdated", newValue);
        });
    }]);
