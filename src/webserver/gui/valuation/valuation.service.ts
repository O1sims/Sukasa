import { Http, Response, Request, Headers, RequestOptions, RequestMethod, URLSearchParams } from "@angular/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class ValuationService {
  api:string = environment.API_HOST + "/api/v" +
    environment.API_VERSION;

  constructor(
    private http: Http) {
	};

  propertyValuation(propertyData) {
    let headers = new Headers();
    headers.set("Token", sessionStorage.getItem("token"));

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: this.api + '/property_valuation/estimation/',
      body: propertyData,
      headers: headers
		});
		return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

  addProperty(submitPropertyData) {
    let headers = new Headers();
    headers.set("Token", sessionStorage.getItem("token"));

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: this.api + '/properties/',
      body: submitPropertyData,
      headers: headers
		});
		return this.http.request(
      new Request(requestoptions))
      .map((res: Response) => {
  			if (res) {
          return {status: res.status};
  			};
      });
  };

};
