import { Http, Request, RequestOptions, RequestMethod } from "@angular/http";
import { environment } from '../environment/environment';
import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';


@Injectable()
export class UserService {
  api:string = environment.API_HOST + "/api/v" +
    environment.API_VERSION;
  
    constructor(
      private http: Http) {
    };
  
    logIn(userData:object) {
      var requestoptions = new RequestOptions({
        method: RequestMethod.Post,
        url: this.api + '/user/login/',
        body: userData
      });
      
      return this.http.request(
        new Request(requestoptions))
      .map(res => res.json());
    };
  
    signUp(signUpData:object) {
      var requestoptions = new RequestOptions({
        method: RequestMethod.Post,
        url: this.api + '/user/',
        body: signUpData
      });
      
      return this.http.request(
        new Request(requestoptions))
      .map(res => res.json());
    };
  
    check(token:string) {
      var requestoptions = new RequestOptions({
        method: RequestMethod.Post,
        url: this.api + '/user/check/',
        body: {"token": token}
      });
      
      return this.http.request(
        new Request(requestoptions))
      .map(res => res.json());
    };
  
    logoutUser(token:string) {
      var requestoptions = new RequestOptions({
        method: RequestMethod.Post,
        url: this.api + '/user/logout/',
        body: {"token": token}
      });
      
      return this.http.request(
        new Request(requestoptions))
      .map(res => res.json());
    };
  
  };