import { Http, Response, Request, Headers, RequestOptions, RequestMethod, URLSearchParams } from "@angular/http";
import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class PropertyService {

  constructor(private http: Http) {
	};

  getPropertyDetails(propertyType, propertyId) {
    var headers = new Headers();
		headers.append("Content-Type", 'application/json');

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: 'api/v1/properties/' + propertyType + '/',
      headers: headers,
      body: JSON.stringify({'_id': propertyId})
		});

    return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

};
