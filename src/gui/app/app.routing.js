System.register(["@angular/router", "./home/home.component", "./search/search.component", "./property/property.component", "./not-found/not-found.component"], function (exports_1, context_1) {
    "use strict";
    var __moduleName = context_1 && context_1.id;
    var router_1, home_component_1, search_component_1, property_component_1, not_found_component_1, routing;
    return {
        setters: [
            function (router_1_1) {
                router_1 = router_1_1;
            },
            function (home_component_1_1) {
                home_component_1 = home_component_1_1;
            },
            function (search_component_1_1) {
                search_component_1 = search_component_1_1;
            },
            function (property_component_1_1) {
                property_component_1 = property_component_1_1;
            },
            function (not_found_component_1_1) {
                not_found_component_1 = not_found_component_1_1;
            }
        ],
        execute: function () {
            exports_1("routing", routing = router_1.RouterModule.forRoot([
                { path: '', component: home_component_1.HomeComponent },
                { path: 'search', component: search_component_1.SearchComponent },
                { path: 'property/:id', component: property_component_1.PropertyComponent },
                { path: 'not-found', component: not_found_component_1.NotFoundComponent },
                { path: '**', redirectTo: 'not-found' }
            ]));
        }
    };
});
