import { Http, Headers, Request, RequestOptions, RequestMethod } from "@angular/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class EstateAgentFinderService {
  api:string = environment.API_HOST + "/api/v" +
    environment.API_VERSION;

  constructor(
    private http: Http) {
	};

  estateAgentRecommender(propertyData) {
    let headers = new Headers();
    headers.set("Token", sessionStorage.getItem("token"));

    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: this.api + '/estate_agent_recommender/',
      body: propertyData,
      headers: headers
		});
		return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

};
