import { Http, Request, Headers, RequestOptions, RequestMethod } from "@angular/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class PropertyService {
  api:string = environment.API_HOST + "/api/v" +
    environment.API_VERSION;

  constructor(private http: Http) {
	};

  getPropertyDetails(propertyId) {
    let headers = new Headers();
    headers.set("Token", sessionStorage.getItem("token"));

    var requestoptions = new RequestOptions({
			method: RequestMethod.Get,
      url: this.api + '/properties/' + propertyId + '/',
      headers: headers
		});

    return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

  postPropertyDetails(propertyData:object) {
    let headers = new Headers();
    headers.set("Token", sessionStorage.getItem("token"));

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
      url: this.api + '/properties/',
      headers: headers,
      body: propertyData
		});

    return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

  priceImperfection(propertyData) {
    let headers = new Headers();
    headers.set("Token", sessionStorage.getItem("token"));

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
      url: this.api + '/property_valuation/differential/',
      body: propertyData,
      headers: headers
		});

    return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

};
