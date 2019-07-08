import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class SharedService {
  currencyChart:object = {
    'pound': '£',
    'euro': '€',
    'dollar': '$'
  };

  cleanPropertyPrice(currency, price) {
    let cleanPrice = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return(this.currencyChart[currency] + cleanPrice);
  };

  shortenPostcode(postcode:string) {
    let clean_postcode = postcode.replace(' ', '');
    if (clean_postcode.length > 6) {
      var region_code = clean_postcode.substring(0, 4);
    } else {
      var region_code = clean_postcode.substring(0, 3);
    };
    return region_code;
  };

  towns:string[] = [
    "belfast",
    "holywood",
    "dundonald"
  ];

  heatingChoices:string[] = [
    "economy 7",
    "gas",
    "oil"
  ];

  aggregateStyleChoices:string[] = [
    "apartment",
    "bungalow",
    "detached",
    "semi-detached",
    "terrace"
  ];

  public token:string;
};
