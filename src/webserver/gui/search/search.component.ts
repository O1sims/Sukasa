import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { SearchService } from './search.service';
import { SharedService } from '../shared/shared.service';


@Component({
  selector: 'search',
  templateUrl: './search/search.component.html',
  providers: [SearchService, SharedService]
})

export class SearchComponent implements OnInit {
  groupSize:number = 2;

  maxPage:number;
  searchPage:number;
  searchQuery:string;
  searchResults:object[];

  allPropertiesFound:number;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private searchService: SearchService,
    private sharedService: SharedService) {};

  ngOnInit() {
    this.route.queryParams
    .subscribe(
      params => {
        this.searchQuery = params['q'] || '';
        this.searchPage = params['page'] || 1;
        this.propertySearch(this.searchQuery, this.searchPage);
      });
  };

  propertySearch(query:string, page:number) {
    this.searchService.searchProperties(query, page)
    .subscribe(
      propertyRequest => {
        this.allPropertiesFound = propertyRequest['propertiesLength'];
        this.maxPage = Math.ceil(this.allPropertiesFound/10);
        var propertyData = propertyRequest['data']
        for (let i = 0; i < propertyData.length; i++) {
          let priceInfo = propertyData[i].priceInfo;
          propertyData[i].price = this.sharedService.cleanPropertyPrice(
            priceInfo.currency,
            priceInfo.price)
        };
        this.searchResults = this.chuckSearchResults(propertyData);
      });
  };

  chuckSearchResults(results:any, groupSize = this.groupSize) {
    return(
      results.map(function(item:any, index) {
        return index % groupSize === 0 ?
        results.slice(index, index + groupSize) : null;
      }).filter(function(item:any){ return item; }));
  };

  traverseSearchPage(trav:string) {
    if (trav=='next') {
      var traversePage = Number(this.searchPage) + 1;
    } else if (trav=='previous') {
      var traversePage = Number(this.searchPage) - 1;
    };
    this.router.navigate(['/search'],
    { queryParams: { 
      q: this.searchQuery,
      page: traversePage } 
    });
    window.scrollTo(0, 0);
  };
  
}
