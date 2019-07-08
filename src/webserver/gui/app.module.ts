
import { NgModule }                      from '@angular/core';
import { HttpModule }                    from '@angular/http';
import { FormsModule }                   from '@angular/forms';
import { BrowserModule }                 from '@angular/platform-browser';

import { AppComponent }                  from './app.component';

import { NavBarComponent }               from './navbar/navbar.component';
import { SearchBarComponent }            from './searchbar/searchbar.component';

import { HomeComponent }                 from './home/home.component';
import { SearchComponent }               from './search/search.component';
import { PropertyComponent }             from './property/property.component';
import { NotFoundComponent }             from './not-found/not-found.component';

import { ValuationComponent }            from './valuation/valuation.component';
import { EstateAgentFinderComponent }    from './estate_agent_finder/estate_agent_finder.component';

import { AddPropertyComponent }          from './modals/add-property/add-property.component';

import { UserService }                   from './user/user.service';

import { routing }                       from './app.routing';
 

@NgModule({
    imports: [
      routing,
      BrowserModule,
      HttpModule,
      FormsModule
    ],
    declarations: [
      AppComponent,
      HomeComponent,
      SearchComponent,
      NavBarComponent,
      PropertyComponent,
      NotFoundComponent,
      SearchBarComponent,
      ValuationComponent,
      AddPropertyComponent,
      EstateAgentFinderComponent
    ],
    providers: [
      UserService
    ],
    bootstrap: [
      AppComponent
    ],
    entryComponents: []
})


export class AppModule {
}
