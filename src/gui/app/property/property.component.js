System.register(["@angular/core", "@angular/router", "./property.service", "../shared/shared.service"], function (exports_1, context_1) {
    "use strict";
    var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
        var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
        if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
        else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
        return c > 3 && r && Object.defineProperty(target, key, r), r;
    };
    var __metadata = (this && this.__metadata) || function (k, v) {
        if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
    };
    var __moduleName = context_1 && context_1.id;
    var core_1, router_1, property_service_1, shared_service_1, PropertyComponent;
    return {
        setters: [
            function (core_1_1) {
                core_1 = core_1_1;
            },
            function (router_1_1) {
                router_1 = router_1_1;
            },
            function (property_service_1_1) {
                property_service_1 = property_service_1_1;
            },
            function (shared_service_1_1) {
                shared_service_1 = shared_service_1_1;
            }
        ],
        execute: function () {
            PropertyComponent = class PropertyComponent {
                constructor(propertyService, route, sharedService) {
                    this.propertyService = propertyService;
                    this.route = route;
                    this.sharedService = sharedService;
                    this.propertyDetail = {
                        "priceInfo": {
                            "offer": undefined,
                            "price": undefined
                        },
                        "details": {
                            "style": undefined,
                            "bedrooms": undefined,
                            "bathrooms": undefined
                        }
                    };
                }
                ;
                ngOnInit() {
                    var propertyData = this.route.params.subscribe(params => {
                        this.propertyService.getPropertyDetails('sale', params['id'])
                            .subscribe(propertyDetail => {
                            propertyDetail[0].price = this.sharedService.cleanPropertyPrice(propertyDetail[0].priceInfo.currency, propertyDetail[0].priceInfo.price);
                            this.propertyDetail = propertyDetail[0];
                        });
                    });
                }
                ;
            };
            PropertyComponent = __decorate([
                core_1.Component({
                    templateUrl: './property/property.component.html',
                    providers: [property_service_1.PropertyService, shared_service_1.SharedService]
                }),
                __metadata("design:paramtypes", [property_service_1.PropertyService,
                    router_1.ActivatedRoute,
                    shared_service_1.SharedService])
            ], PropertyComponent);
            exports_1("PropertyComponent", PropertyComponent);
        }
    };
});
