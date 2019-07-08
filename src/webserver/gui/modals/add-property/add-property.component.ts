import { Component, OnInit } from '@angular/core';

import { PropertyService } from '../../property/property.service';
import { SharedService } from '../../shared/shared.service';
import { ValuationService } from '../../valuation/valuation.service';


@Component({
    selector: 'add-property',
    templateUrl: './modals/add-property/add-property.component.html',
    providers: [SharedService, PropertyService, ValuationService]
})

export class AddPropertyComponent implements OnInit { 
    towns:string[];
    heatingChoices:string[];
    aggregateStyleChoices:string[];

    town:string;
    heating:string;
    aggregateStyle:string;
    postcode:string;
    bedrooms:number;
    address:string;

    constructor(
        private sharedService: SharedService,
        private propertyService: PropertyService,
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
        this.postcode = event['target']['value'];
        } else if (feature=="bedrooms") {
        this.bedrooms = Number(event['target']['value']);
        } else if (feature=="address") {
        this.address = event['target']['value'];
        } else if (feature=="town") {
        this.town = event['target']['value'];
        };
    };

    constructPropertyData() {
        let propertyData = {
            "address": this.address,
            "town": this.town,
            "postcode": this.sharedService.shortenPostcode(
                this.postcode),
            "details": {
                "aggregateStyle": this.aggregateStyle,
                "bedrooms": this.bedrooms,
                "heating": this.heating,
                "longPostcode": this.postcode
            }
        };
        return propertyData;
    };

    constructValuationData() {
        let propertyData = {
        "postcode": this.sharedService.shortenPostcode(
            this.postcode),
        "details": {
            "bedrooms": this.bedrooms,
            "style": this.aggregateStyle,
            "heating": this.heating,
            "amenities": {
            "garage": false,
            "garden": true,
            "parking": false,
            "driveway": true,
            "bayWindow": false
            }
        }
        };
        return propertyData;
    };

    getValuation() {
        var propertyData = this.constructValuationData();
        this.valuationService.propertyValuation(
            propertyData).subscribe(
                data => {
                    console.log(data);
                }
            );

    };

    addProperty() {
        let propertyData = this.constructPropertyData();
        this.propertyService.postPropertyDetails(
            propertyData).subscribe(
                data => {

                }
            );
    };

}
