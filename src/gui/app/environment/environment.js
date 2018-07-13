System.register([], function (exports_1, context_1) {
    "use strict";
    var __moduleName = context_1 && context_1.id;
    var environment;
    return {
        setters: [],
        execute: function () {
            exports_1("environment", environment = {
                API_HOST: "http://localhost",
                API_PORT: 5000,
                API_VERSION: "1.0.0"
            });
        }
    };
});
