import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
    templateUrl: 'app/search/search.component.html'
})

export class SearchComponent implements OnInit {
  searchQuery: string;
  
  constructor(
    private route: ActivatedRoute,
    private router: Router) {}

  ngOnInit() {
    this.route.queryParams
    .subscribe(
      params => {
        this.searchQuery = params['q'] || ''
      });
  };
}
