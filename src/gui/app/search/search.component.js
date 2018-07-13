System.register(["@angular/core", "@angular/router", "./search.service", "../shared/shared.service"], function (exports_1, context_1) {
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
    var core_1, router_1, search_service_1, shared_service_1, SearchComponent;
    return {
        setters: [
            function (core_1_1) {
                core_1 = core_1_1;
            },
            function (router_1_1) {
                router_1 = router_1_1;
            },
            function (search_service_1_1) {
                search_service_1 = search_service_1_1;
            },
            function (shared_service_1_1) {
                shared_service_1 = shared_service_1_1;
            }
        ],
        execute: function () {
            SearchComponent = class SearchComponent {
                constructor(searchService, route, sharedService) {
                    this.searchService = searchService;
                    this.route = route;
                    this.sharedService = sharedService;
                    this.groupSize = 2;
                    this.searchQuery = "";
                    this.searchResults = [];
                }
                ;
                ngOnInit() {
                    this.route.queryParams
                        .subscribe(params => {
                        this.searchQuery = params['q'] || '';
                        this.propertySearch(this.searchQuery);
                    });
                }
                ;
                propertySearch(query) {
                    this.searchService.searchProperties('sale', query)
                        .subscribe(propertyData => {
                        for (let i = 0; i < propertyData.length; i++) {
                            let priceInfo = propertyData[i].priceInfo;
                            propertyData[i].price = this.sharedService.cleanPropertyPrice(priceInfo.currency, priceInfo.price);
                        }
                        ;
                        console.log(propertyData);
                        this.searchResults = this.chuckSearchResults(propertyData);
                    });
                }
                ;
                chuckSearchResults(results, groupSize = this.groupSize) {
                    return (results.map(function (item, index) {
                        return index % groupSize === 0 ?
                            results.slice(index, index + groupSize) : null;
                    }).filter(function (item) { return item; }));
                }
                ;
            };
            SearchComponent = __decorate([
                core_1.Component({
                    templateUrl: './search/search.component.html',
                    providers: [search_service_1.SearchService, shared_service_1.SharedService]
                }),
                __metadata("design:paramtypes", [search_service_1.SearchService,
                    router_1.ActivatedRoute,
                    shared_service_1.SharedService])
            ], SearchComponent);
            exports_1("SearchComponent", SearchComponent);
        }
    };
});
