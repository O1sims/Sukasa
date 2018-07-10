import { Http, Response, Request, Headers, RequestOptions, RequestMethod, URLSearchParams } from "@angular/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class PropertyService {
  apiVerion:string = environment.API_VERSION;

  constructor(private http: Http) {
	};

  getPropertyDetails(propertyType, propertyId) {
    var requestoptions = new RequestOptions({
			method: RequestMethod.Get,
      url: '/api/v' + this.apiVerion + '/property/' + propertyType + '/' + propertyId + '/'
		});

    return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

};
