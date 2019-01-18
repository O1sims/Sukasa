import { Http, Response, Request, Headers, RequestOptions, RequestMethod, URLSearchParams } from "@angular/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class ValuationService {
  api:string = environment.API_HOST + ":" +
  environment.API_PORT + "/api/v" +
  environment.API_VERSION;

  constructor(
    private http: Http) {
	};

  propertyValuation(propertyData) {
    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: this.api + '/property_valuation/estimation/',
      body: propertyData
		});
		return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

  addProperty(submitPropertyData) {
    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: this.api + '/properties/',
      body: submitPropertyData
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
