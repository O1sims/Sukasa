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
};
