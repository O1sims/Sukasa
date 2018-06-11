import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { SearchService } from './search.service';


@Component({
  templateUrl: 'app/search/search.component.html',
  providers: [SearchService]
})

export class SearchComponent implements OnInit {
  searchQuery:string = "";
  searchResults:object[] = [];

  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute,
    private router: Router) {}

  ngOnInit() {
    this.route.queryParams
    .subscribe(
      params => {
        this.searchQuery = params['q'] || '';
        this.propertySearch(this.searchQuery);
      });
  };

  propertySearch(query) {
    this.searchService.searchProperties('sale', query)
    .subscribe(
      propertyData => {
        for (let i = 0; i < propertyData.length; i++) {
          let priceInfo = propertyData[i].priceInfo;
          propertyData[i].price = this.cleanPropertyPrice(
            priceInfo.currency,
            priceInfo.price)
        };
        this.searchResults = propertyData;
        console.log(this.searchResults);
      });
  };

  cleanPropertyPrice(currency, price) {
    let cleanPrice = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    var currencies = {
      'pound': '£',
      'euro': '€',
      'dollar': '$'
    };
    return(currencies[currency] + cleanPrice);
  };

}
