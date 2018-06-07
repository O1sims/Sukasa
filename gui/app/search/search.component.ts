import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { SearchService } from './search.service';


@Component({
    templateUrl: 'app/search/search.component.html',
    providers: [SearchService]
})

export class SearchComponent implements OnInit {
  searchResults:object[] = [];

  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute,
    private router: Router) {}

  ngOnInit() {
    this.route.queryParams
    .subscribe(
      params => {
        let searchQuery = params['q'] || '';
        this.propertySearch(searchQuery);
      }
    );
  };

  propertySearch(query) {
    this.searchService.searchProperties('sale', query)
    .subscribe(
      propertyData => {
        this.searchResults = propertyData;
        console.log(this.searchResults);
      }
    );
  };
}
