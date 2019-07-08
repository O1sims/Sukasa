import { Component, ViewChild, OnInit } from '@angular/core';

import { UserService } from '../user/user.service';


@Component({
    selector: 'navbar',
    templateUrl: './navbar/navbar.component.html',
    providers: [UserService]
})

export class NavBarComponent implements OnInit {
  pathName: string;
  selectedTab: string;

  username:string;
  password:string;
    
  email:string;
  firstName:string;
  lastName:string;
    
  section:string;
  modalTitle:string;
    
  user:object;
  loggedIn:boolean = false;
  loginWarning:boolean = false;

  @ViewChild("closeModal") closeModal:any;

  constructor(
    private userService: UserService) {};

  ngOnInit() {
    this.getPathname();
    if (sessionStorage.getItem("token") != null || sessionStorage.getItem("token") != "") {
      this.checkLogIn(sessionStorage.getItem("token"));
    };
  };

  checkLogIn(token:string) {
    this.userService.check(token).subscribe(
        userData => {
            if (userData['user'] != null) {
                this.user = userData['user'];
                this.loggedIn = true;
            } else {
                this.loggedIn = false;
            };
          }
        );
      };

setFeature(event:object, feature:string) {
    if (feature=="username") {
      this.username = event['target']['value'];
    } else if (feature=="password") {
      this.password = event['target']['value'];
    } else if (feature=="email") {
      this.email = event['target']['value'];
    } else if (feature=="firstName") {
      this.firstName = event['target']['value'];
    } else if (feature=="lastName") {
      this.lastName = event['target']['value'];
    };
  };

  logout() {
    this.userService.logoutUser(
      sessionStorage.getItem("token")).subscribe(
        data => {
          sessionStorage.removeItem("token");
          this.loggedIn = false;
          this.user = {};
        }
      );
  };

  moveToLogIn() {
    this.section = "login";
    this.modalTitle = "Log in";
  };

  moveToSignUp() {
    this.section = "signUp";
    this.modalTitle = "Sign up";
  };

  logIn() {
    var userData = {
      "username": this.username,
      "password": this.password
    };

    this.userService.logIn(userData).subscribe(
      data => {
        if (data['token'] == null) {
          this.loginWarning = true;
        } else {
          this.loginWarning = false;
          sessionStorage.setItem("token", data['token']);
          this.closeModal.nativeElement.click();
          this.loggedIn = true;
          this.user = data['user'][0];
        };
      }
    );
  };

  signUp() {
    var signUpData = {
      "username": this.username,
      "password": this.password,
      "first_name": this.firstName,
      "second_name": this.lastName,
      "email": this.email
    };
    this.userService.signUp(signUpData).subscribe(
      data => {
        if (data['token'] == null) {
          // TODO: Add sign up warning!

        } else {
          this.loginWarning = false;
          this.closeModal.nativeElement.click();
          sessionStorage.setItem("token", data['token']);
          this.user = data['user'];
          this.checkLogIn(data['token']);
        };
      }
    );
  };

  getPathname() {
    this.pathName = window.location.pathname;
    if (this.pathName == '' ||
          this.pathName == '/' ||
          this.pathName == '/search') {
      this.selectedTab = 'search';
    };
  };

  assignSelectedTab(tabString:string) {
    this.selectedTab = tabString;
  };
}
