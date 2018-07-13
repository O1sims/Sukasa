import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'home',
  templateUrl: './home/home.component.html'
})

export class HomeComponent {

  constructor(
    private router: Router) {}

  searchQuery:string = "";

  prepareSearchQuery(event) {
    this.searchQuery = event['target']['value'];
  };

  propertySearch() {
    this.router.navigate(['/search'],
    { queryParams: { q: this.searchQuery } });
  };
}
