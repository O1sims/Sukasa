import { Component, OnInit } from '@angular/core';

import { EstateAgentFinderService } from './estate_agent_finder.service';
import { SharedService } from '../shared/shared.service';


@Component({
  templateUrl: './estate_agent_finder/estate_agent_finder.component.html',
  providers: [EstateAgentFinderService, SharedService]
})

export class EstateAgentFinderComponent implements OnInit {
  
  towns:string[];
  heatingChoices:string[];
  aggregateStyleChoices:string[];

  town:string;
  heating:string;
  aggregateStyle:string;
  postcode:string;
  bedrooms:number;
  address:string;

  garden:boolean = false;
  driveway:boolean = false;
  garage:boolean = false;
  bayWindow:boolean = false;
  parking:boolean = false;

  recommendedEstateAgents:object[] = [];

  constructor(
    private sharedService: SharedService,
    private estateAgentFinderService: EstateAgentFinderService) {};
  
  ngOnInit() {
    // The allocation of shared variables
    this.towns = this.sharedService.towns;
    this.heatingChoices = this.sharedService.heatingChoices;
    this.aggregateStyleChoices = this.sharedService.aggregateStyleChoices;

    this.town = this.towns[0];
    this.heating = this.heatingChoices[0];
    this.aggregateStyle = this.aggregateStyleChoices[0];
  };
  
  setFeature(event, feature:string) {
    if (feature=="heating") {
      this.heating = event['target']['value'];
    } else if (feature=="propertyStyle") {
      this.aggregateStyle = event['target']['value'];
    } else if (feature=="postcode") {
      this.postcode = event['target']['value'];
    } else if (feature=="bedrooms") {
      this.bedrooms = Number(event['target']['value']);
    } else if (feature=="address") {
      this.address = event['target']['value'];
    } else if (feature=="town") {
      this.town = event['target']['value'];
    };
  };

  setAmenityBool(amenity:string) {
    if (amenity=="garage") {
      this.garage = !this.garage;
    } else if (amenity=="driveway") {
      this.driveway = !this.driveway;
    } else if (amenity=="garden") {
      this.garden = !this.garden;
    } else if (amenity=="bayWindow") {
      this.bayWindow = !this.bayWindow;
    } else if (amenity=="parking") {
      this.parking = !this.parking;
    };
  };
  
  constructPropertyData() {
    let propertyData = {
      "propertyData": {
        "address": this.address,
        "town": this.town,
        "postcode": this.postcode,
        "aggregateStyle": this.aggregateStyle,
        "details": {
          "bedrooms": this.bedrooms,
          "heating": this.heating,
          "amenities": {
            "garden": this.garden, 
            "garage": this.garage, 
            "driveway": this.driveway, 
            "parking": this.parking, 
            "bayWindow": this.bayWindow
          }
        }
      }
    };
    return propertyData;
  };

  recommendEstateAgent() {
    let propertyData = this.constructPropertyData();
    let estateAgentLogos = this.sharedService.estateAgentLogoLookup;
    this.estateAgentFinderService.estateAgentRecommender(propertyData)
    .subscribe(estateAgentFinder => {
      estateAgentFinder['recommendedAgents'].forEach(function(estateAgent:object) {
        if (Object.keys(estateAgentLogos).includes(estateAgent['name'])) {
          estateAgent['logo'] = estateAgentLogos[estateAgent['name']];
        } else {
          estateAgent['logo'] = "";
        };
      });
      this.recommendedEstateAgents = estateAgentFinder['recommendedAgents'].slice(0, 3);
    });
  };
}
