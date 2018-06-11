import { Component, OnInit } from '@angular/core';

@Component({
    selector: 'navbar',
    templateUrl: 'app/navbar/navbar.component.html'
})

export class NavBarComponent implements OnInit {
  pathName: string;
  selectedTab: string;

  ngOnInit() {
    this.getPathname();
  };

  getPathname() {
    this.pathName = window.location.pathname;
    if (this.pathName == '/' || this.pathName == '/risk-graph') {
      this.selectedTab = 'riskNetwork';
    } else if (this.pathName == '/cvi' || this.pathName == '/cvi/') {
      this.selectedTab = 'cvi';
    } else if (this.pathName == '/risk-appetite' || this.pathName == '/risk-appetite/') {
      this.selectedTab = 'riskAppetite';
    } else if (this.pathName == '/actions' || this.pathName == '/actions/') {
      this.selectedTab = 'actions';
    };
  };

  assignSelectedTab(tabString) {
    this.selectedTab = tabString;
  };
}
