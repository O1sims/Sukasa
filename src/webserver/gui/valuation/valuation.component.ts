import { Component, OnInit } from '@angular/core';

import { ValuationService } from './valuation.service';
import { SharedService } from '../shared/shared.service';


@Component({
  templateUrl: './valuation/valuation.component.html',
  providers: [ValuationService, SharedService]
})

export class ValuationComponent implements OnInit {
  towns:string[];
  heatingChoices:string[];
  aggregateStyleChoices:string[];

  bedrooms:number = 1;
  estimatedValue:number;
  rawEstimation:number;

  garden:boolean = false;
  driveway:boolean = false;
  garage:boolean = false;
  bayWindow:boolean = false;
  parking:boolean = false;

  address:string;
  postcode:string;
  
  town:string;
  heating:string;
  aggregateStyle:string;

  propertySubmitted:boolean = false;
  propertyImage:any;

  constructor(
    private sharedService: SharedService,
    private valuationService: ValuationService) {};

  ngOnInit() {
    // The allocation of shared variables
    this.towns = this.sharedService.towns;
    this.heatingChoices = this.sharedService.heatingChoices;
    this.aggregateStyleChoices = this.sharedService.aggregateStyleChoices;

    this.town = this.towns[0];
    this.heating = this.heatingChoices[0];
    this.aggregateStyle = this.aggregateStyleChoices[0];

  };

  setFeature(event, feature) {
    if (feature=="heating") {
      this.heating = event['target']['value'];
    } else if (feature=="propertyStyle") {
      this.aggregateStyle = event['target']['value'];
    } else if (feature=="postcode") {
      this.postcode = this.sharedService.shortenPostcode(
        event['target']['value']);
    } else if (feature=="bedrooms") {
      this.bedrooms = event['target']['value'];
    } else if (feature=="address") {
      this.address = event['target']['value'];
    } else if (feature=="town") {
      this.town = event['target']['value'];
    };
  };

  setImage(event) {
    this.propertyImage = event.target.files[0];
  };

  setAmenityBool(amenity) {
    if (amenity=="garage") {
      this.garage = !this.garage;
    } else if (amenity=="driveway") {
      this.driveway = !this.driveway;
    } else if (amenity=="garden") {
      this.garden = !this.garden;
    } else if (amenity=="bayWindow") {
      this.bayWindow = !this.bayWindow;
    };
  };

  constructPropertyData(forSubmission=false) {
    var propertyData = {
      "postcode": this.postcode,
      "propertyImage": this.propertyImage,
      "details": {
        "bedrooms": Number(this.bedrooms),
        "style": this.aggregateStyle,
        "heating": this.heating,
        "amenities": {
          "garage": this.garage,
          "garden": this.garden,
          "driveway": this.driveway,
          "bayWindow": this.bayWindow,
          "parking": this.parking
        }
      }
    };
    if (forSubmission) {
      propertyData['propertyId'] = Math.floor(Math.random()*100000).toString();
      propertyData['address'] = this.address;
      propertyData['town'] = this.town;
      propertyData['priceInfo'] = {
        'price': this.rawEstimation,
        'currency': 'pound'
      };
      propertyData['estateAgent'] = {
        "name": "Self-sale",
        "branch": "Hestia"
      }
    };
    return propertyData;
  }

  estimatePropertyValue() {
    var propertyData = this.constructPropertyData();
    this.valuationService.propertyValuation(propertyData)
    .subscribe(valuation => {
      this.estimatedValue = this.sharedService.cleanPropertyPrice(
        'pound', valuation['estimatedPrice'].toFixed(2));
      this.rawEstimation =  Number(valuation['estimatedPrice'].toFixed(2));
    });
  };

  submitProperty() {
    var propertyData = this.constructPropertyData(true);
    this.valuationService.addProperty(propertyData)
    .subscribe(submitData => {
      this.propertySubmitted=true;
    });
  }
}
