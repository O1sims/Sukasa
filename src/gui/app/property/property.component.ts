import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { PropertyService } from './property.service';
import { SharedService } from '../shared/shared.service';


@Component({
  templateUrl: './property/property.component.html',
  providers: [PropertyService, SharedService]
})

export class PropertyComponent implements OnInit {
  propertyDetail:object = {
    "priceInfo": {
      "offer": undefined,
      "price": undefined
    },
    "details": {
      "style": undefined,
      "bedrooms": undefined,
      "bathrooms": undefined
    }
  };

  constructor(
    private propertyService: PropertyService,
    private route: ActivatedRoute,
    private sharedService: SharedService) {};

  ngOnInit() {
    var propertyData = this.route.params.subscribe(params => {
       this.propertyService.getPropertyDetails('sale', params['id'])
       .subscribe(
         propertyDetail => {
           propertyDetail[0].price = this.sharedService.cleanPropertyPrice(
             propertyDetail[0].priceInfo.currency,
             propertyDetail[0].priceInfo.price)
           this.propertyDetail = propertyDetail[0];
         });
    });
  };

}
