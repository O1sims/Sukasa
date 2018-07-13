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
    if (this.pathName == '/' || this.pathName == '/sale') {
      this.selectedTab = 'sale';
    } else if (this.pathName == '/rent' || this.pathName == '/rent/') {
      this.selectedTab = 'rent';
    };
  };

  assignSelectedTab(tabString) {
    this.selectedTab = tabString;
  };
}
