import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { PropertyService } from './property.service';


@Component({
  templateUrl: 'app/property/property.component.html',
  providers: [PropertyService]
})

export class PropertyComponent implements OnInit {
  propertyId:string = "";

  constructor(
    private propertyService: PropertyService,
    private route: ActivatedRoute) {};

  ngOnInit() {
    var propertyData = this.route.params.subscribe(params => {
       this.propertyId = params['id'];
       this.propertyService.getPropertyDetails('sale', params['id'])
       .subscribe(
         propertyDetail => {
           console.log(propertyDetail[0]);
         });
    });
  };

}
