import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class SharedService {
  cleanPropertyPrice(currency, price) {
    let cleanPrice = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return(this.currencyChart[currency] + cleanPrice);
  };
  
  currencyChart:object = {
    'pound': '£',
    'euro': '€',
    'dollar': '$'
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

  estateAgentLogoLookup:object = {
    "Stewart & Company": "https://img2.propertypal.com/logo/160816205354/400x400/ST0709218/master.png",
    "John Minnis Estate Agents": "https://img2.propertypal.com/logo/190410161629/400x400/ST0213205/master.png",
    "Ulster Property Sales": "https://img2.propertypal.com/logo/160816205354/400x400/ST1208213/master.png",
    "Reeds Rains": "https://img2.propertypal.com/logo/170126124650/400x400/ST0409251/master.png",
    "Rodgers & Finney": "https://img2.propertypal.com/logo/170801084334/400x400/ST0817201/master.png",
    "GOC Estate Agents Ltd": "https://img2.propertypal.com/logo/160816205354/400x400/ST0209202/master.png",
    "Armstrong Anderson": "https://img2.propertypal.com/logo/170120153025/400x400/ST0814202/master.png",
    "Simon Brien Residential": "https://img2.propertypal.com/logo/160816205354/400x400/ST0509207/master.png",
    "Templeton Robinson": "https://img2.propertypal.com/logo/160816205354/400x400/ST0409210/master.png",
    "PurpleBricks Group PLC": "https://img2.propertypal.com/logo/190107145048/400x400/ST0515201/master.png",
    "Henry Graham Estate Agents": "https://img2.propertypal.com/logo/180710080745/400x400/ST0807212/forSale.png",
    "Fetherston Clements": "https://img2.propertypal.com/logo/160816205354/400x400/ST0111211/master.png",
    "McClearys Property Sales": "https://img2.propertypal.com/logo/171208152049/400x400/ST1107208/master.png",
    "Michael Chandler Estate Agents": "https://img2.propertypal.com/logo/180928095842/400x400/ST0609216/master.png",
  };
};
