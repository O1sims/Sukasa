System.register(["@angular/core", "@angular/http", "@angular/platform-browser", "./app.component", "./navbar/navbar.component", "./searchbar/searchbar.component", "./home/home.component", "./search/search.component", "./property/property.component", "./not-found/not-found.component", "./app.routing"], function (exports_1, context_1) {
    "use strict";
    var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
        var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
        if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
        else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
        return c > 3 && r && Object.defineProperty(target, key, r), r;
    };
    var __moduleName = context_1 && context_1.id;
    var core_1, http_1, platform_browser_1, app_component_1, navbar_component_1, searchbar_component_1, home_component_1, search_component_1, property_component_1, not_found_component_1, app_routing_1, AppModule;
    return {
        setters: [
            function (core_1_1) {
                core_1 = core_1_1;
            },
            function (http_1_1) {
                http_1 = http_1_1;
            },
            function (platform_browser_1_1) {
                platform_browser_1 = platform_browser_1_1;
            },
            function (app_component_1_1) {
                app_component_1 = app_component_1_1;
            },
            function (navbar_component_1_1) {
                navbar_component_1 = navbar_component_1_1;
            },
            function (searchbar_component_1_1) {
                searchbar_component_1 = searchbar_component_1_1;
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
            },
            function (app_routing_1_1) {
                app_routing_1 = app_routing_1_1;
            }
        ],
        execute: function () {
            AppModule = class AppModule {
            };
            AppModule = __decorate([
                core_1.NgModule({
                    imports: [
                        app_routing_1.routing,
                        platform_browser_1.BrowserModule,
                        http_1.HttpModule
                    ],
                    declarations: [
                        app_component_1.AppComponent,
                        home_component_1.HomeComponent,
                        search_component_1.SearchComponent,
                        navbar_component_1.NavBarComponent,
                        property_component_1.PropertyComponent,
                        not_found_component_1.NotFoundComponent,
                        searchbar_component_1.SearchBarComponent
                    ],
                    bootstrap: [
                        app_component_1.AppComponent
                    ],
                    entryComponents: []
                })
            ], AppModule);
            exports_1("AppModule", AppModule);
        }
    };
});
