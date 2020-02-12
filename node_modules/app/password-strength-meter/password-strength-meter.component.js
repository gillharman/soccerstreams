'use strict';

angular.module('passwordStrengthMeter').
    component('passwordStrengthMeter', {
        template: '<div class="password-strength">' +
                            '<span class="text-muted">Password strength: {{$ctrl.strength}}</span>' +
                            '<ul class="password-strength-indicator">' +
                                '<li ng-repeat="i in [0,1,2,3]" ng-class="{ \'s-b-active\': $ctrl.strength_bar[{{i}}].active }" class="strength-bar s-b-{{i}}"></li>' +
                            '</ul>' +
                        '</div>',
        controller: ('PasswordStrengthMeterController', ['$scope', function PasswordStrengthMeterController($scope) {
            var self = this;
            self.strength = "",
            self.strength_bar = {
                0: { active: false, type: "Poor" },
                1: { active: false, type: "Moderate" },
                2: { active: false, type: "Moderate" },
                3: { active: false, type: "Strong" }
            }

            $scope.$on("pwUpdated", function(event, value) {
                updateStrengthBar(value);
            });

            function updateStrengthBar(password) {
                if(password != "" && password != undefined) {
                    if(password.length > 0) {
                        self.strength_bar['0'].active = true;
                        self.strength = self.strength_bar['0'].type;
                    }
                    if(password.length > 3) {
                        self.strength_bar['1'].active = true;
                        self.strength = self.strength_bar['1'].type;
                    } else if(self.strength_bar['1'].active) {
                        self.strength_bar['1'].active = false;
                    }
                    if(password.length > 5) {
                        self.strength_bar['2'].active = true;
                        self.strength = self.strength_bar['2'].type;
                    } else if(self.strength_bar['2'].active) {
                        self.strength_bar['2'].active = false;
                    }
                    if(password.length > 8) {
                        self.strength_bar['3'].active = true;
                        self.strength = self.strength_bar['3'].type;
                    } else if(self.strength_bar['3'].active) {
                        self.strength_bar['3'].active = false;
                    }
                } else {
                    for(var key in self.strength_bar) {
                        self.strength_bar[key].active = false;
                    }
                    self.strength = "";
                }
            }
        }])
    });
