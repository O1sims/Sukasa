import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { PropertyService } from './property.service';
import { SharedService } from '../shared/shared.service';


@Component({
  templateUrl: './property/property.component.html',
  providers: [PropertyService, SharedService]
})

export class PropertyComponent implements OnInit {
  propertyDetail:object;
  valuationLabel:string;
  differential:string = "";
  differentialClass:string = "alert alert-info";

  constructor(
    private route: ActivatedRoute,
    private sharedService: SharedService,
    private propertyService: PropertyService) {};

  ngOnInit() {
    var propertyData = this.route.params.subscribe(params => {
       this.propertyService.getPropertyDetails(params['id'])
       .subscribe(
         propertyDetail => {
           propertyDetail['price'] = this.sharedService.cleanPropertyPrice(
             propertyDetail['priceInfo']['currency'],
             propertyDetail['priceInfo']['price'])
           this.propertyDetail = propertyDetail;
           this.checkPriceImperfection(propertyDetail);
         }
       );
    });
  };

  sanityCheckFeature(feature, data) {
    if (data==undefined) {
      var replacement;
      if (feature=="heating") {
        replacement = "gas";
      } else if (feature=="bedrooms") {
        replacement = 2;
      }
      return replacement;
    } else {
      return data;
    }
  };

  checkPriceImperfection(propertyData) {
    var formattedPropertyData = {
      "givenPrice": propertyData['priceInfo']['price'],
      "propertyInfo": {
        "postcode": propertyData["postcode"],
        "details": {
          "bedrooms": this.sanityCheckFeature(
            "bedrooms", Number(propertyData["details"]["bedrooms"])),
          "style": propertyData["details"]["style"],
          "heating": this.sanityCheckFeature(
            "heating", propertyData["details"]["heating"]),
          "amenities": {
            "garage": propertyData["details"]["amenities"]["garage"],
            "garden": propertyData["details"]["amenities"]["garden"],
            "driveway": propertyData["details"]["amenities"]["driveway"],
            "bayWindow": propertyData["details"]["amenities"]["bayWindow"]
          }
        }
      }
    };
    this.propertyService.priceImperfection(formattedPropertyData)
    .subscribe(
      priceImperfectionCheck => {
        this.valuationLabel = priceImperfectionCheck['differential']['label'];
        var priceDifference = Math.abs(
          Number(priceImperfectionCheck['differential']['difference']));
        if (this.valuationLabel == "overvalued") {
          this.differentialClass = "alert alert-danger";
          this.differential = " by " + this.sharedService.cleanPropertyPrice(
            this.propertyDetail['priceInfo']['currency'],
            priceDifference.toFixed(2));
        } else if (this.valuationLabel == "undervalued") {
          this.differentialClass = "alert alert-success";
          this.differential = " by " + this.sharedService.cleanPropertyPrice(
            this.propertyDetail['priceInfo']['currency'],
            priceDifference.toFixed(2));
        }
      }
    );
  };

}
