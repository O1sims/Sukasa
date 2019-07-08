import { Http, Response, Request, RequestOptions, RequestMethod } from "@angular/http";
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
  
  estateAgentRecommender(propertyData:object) {
    var requestoptions = new RequestOptions({
			method: RequestMethod.Post,
			url: this.api + '/estate_agent_recommender/',
      body: propertyData
		});
		return this.http.request(
      new Request(requestoptions))
		.map(res => res.json());
  };

};
