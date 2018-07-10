import { Http, Response, Request, Headers, RequestOptions, RequestMethod, URLSearchParams } from "@angular/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class SearchService {
  apiVerion:string = environment.API_VERSION;

  constructor(
    private http: Http) {
	};

  searchProperties(propertyType, searchQuery) {
    let params = new URLSearchParams();
    params.set('q', searchQuery);
    var requestoptions = new RequestOptions({
			method: RequestMethod.Get,
			url: '/api/v' + this.apiVerion + '/properties/' + propertyType + '/',
      params: params
		});
		return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

};
