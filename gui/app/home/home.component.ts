import { Component } from '@angular/core';

@Component({
    templateUrl: 'app/home/home.component.html'
})

export class HomeComponent {

  searchQuery:string = "";

  prepareSearchQuery(event) {
    this.searchQuery = event['target']['value'];
  };
}
