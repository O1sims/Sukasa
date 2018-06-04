
import { NgModule }                  from '@angular/core';
import { BrowserModule }             from '@angular/platform-browser';

import { AppComponent }              from './app.component';

import { HomeComponent }             from './home/home.component';
import { SearchComponent }           from './search/search.component';
import { NotFoundComponent }         from './not-found/not-found.component';

import { routing }                   from './app.routing';


@NgModule({
    imports: [
      routing,
      BrowserModule
    ],
    declarations: [
      AppComponent,
      HomeComponent,
      SearchComponent,
      NotFoundComponent
    ],
    bootstrap: [
      AppComponent
    ],
    entryComponents: []
})


export class AppModule {
}
