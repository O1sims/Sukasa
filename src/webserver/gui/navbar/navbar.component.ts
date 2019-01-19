import { Component, OnInit } from '@angular/core';

@Component({
    selector: 'navbar',
    templateUrl: './navbar/navbar.component.html'
})

export class NavBarComponent implements OnInit {
  pathName: string;
  selectedTab: string;

  ngOnInit() {
    this.getPathname();
  };

  getPathname() {
    this.pathName = window.location.pathname;
    if (this.pathName == '' ||
          this.pathName == '/' ||
          this.pathName == '/search') {
      this.selectedTab = 'search';
    };
  };

  assignSelectedTab(tabString) {
    this.selectedTab = tabString;
  };
}
