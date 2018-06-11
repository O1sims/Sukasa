import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { SearchService } from './search.service';


@Component({
  templateUrl: 'app/search/search.component.html',
  providers: [SearchService]
})

export class SearchComponent implements OnInit {
  groupSize:number = 2;

  searchQuery:string = "";
  searchResults:object[] = [];

  currencyChart:object = {
    'pound': '£',
    'euro': '€',
    'dollar': '$'
  };

  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute) {};

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
        console.log(propertyData);
        this.searchResults = this.chuckSearchResults(propertyData)
      });
  };

  chuckSearchResults(results, groupSize = this.groupSize) {
    return(
      results.map(function(item, index) {
        return index % groupSize === 0 ?
        results.slice(index, index + groupSize) : null;
      }).filter(function(item){ return item; }));
  };

  cleanPropertyPrice(currency, price) {
    let cleanPrice = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return(this.currencyChart[currency] + cleanPrice);
  };

}
