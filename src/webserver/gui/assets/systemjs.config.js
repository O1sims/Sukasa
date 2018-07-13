(function(global) {

  var config = {
    map: map,
    baseURL: '/gui/',
    packages: packages
  };

  var map = {
    'app': '.',
    '@angular': './node_modules/@angular',
    'rxjs': './node_modules/rxjs'
  };

  var packages = {
    'app' : {
      main: 'main.js',
      defaultExtension: 'js'
    },
    'rxjs' : {
      defaultExtension: 'js'
    }
  };

  var ngPackageNames = [
    'common',
    'compiler',
    'core',
    'forms',
    'http',
    'platform-browser',
    'platform-browser-dynamic',
    'router',
    'router-deprecated',
    'upgrade'
  ];

  ngPackageNames.forEach(function (pkgName) {
      packages['@angular/'+pkgName] = {
        main: 'index.js',
        defaultExtension: 'js'
      };
  });

  function packUmd(pkgName) {
    packages['@angular/'+pkgName] = {
      main: '/bundles/' + pkgName + '.umd.js',
      defaultExtension: 'js'
    };
  }

  var setPackageConfig = System.packageWithIndex ? packIndex : packUmd;

  ngPackageNames.forEach(setPackageConfig);

  var config = {
    map: map,
    packages: packages
  };

  System.config(config);
})(this);
