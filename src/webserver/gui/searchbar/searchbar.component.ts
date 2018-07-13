import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';


@Component({
  selector: 'searchbar',
  templateUrl: './searchbar/searchbar.component.html'
})

export class SearchBarComponent implements OnInit {
  searchQuery:string = "";

  constructor(
    private route: ActivatedRoute,
    private router: Router) {}

  ngOnInit() {
    this.route.queryParams
    .subscribe(
      params => {
        this.searchQuery = params['q'] || '';
      });
  };

  prepareSearchQuery(event) {
    this.searchQuery = event['target']['value'];
  };

  propertySearch() {
    this.router.navigate(['/search'],
    { queryParams: { q: this.searchQuery } });
  };

}
