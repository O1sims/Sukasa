import { Http, Response, Request, Headers, RequestOptions, RequestMethod, URLSearchParams } from "@angular/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class SearchService {
  api:string = environment.API_HOST + ":" +
  environment.API_PORT + "/api/v" +
  environment.API_VERSION;

  constructor(
    private http: Http) {
	};

  searchProperties(searchQuery) {
    let params = new URLSearchParams();
    params.set('q', searchQuery);
    var requestoptions = new RequestOptions({
			method: RequestMethod.Get,
			url: this.api + '/properties/',
      params: params
		});
		return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

};
