import { Http, Response, Request, Headers, RequestOptions, RequestMethod, URLSearchParams } from "@angular/http";
import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class PropertyService {

  constructor(private http: Http) {
	};

  searchProperties(propertyType, searchQuery) {
    let params = new URLSearchParams();
    params.set('q', searchQuery);
    var requestoptions = new RequestOptions({
			method: RequestMethod.Get,
			url: '/api/v1/properties/' + propertyType + '/',
      params: params
		});
		return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

};
