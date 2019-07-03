
import { RouterModule }                  from '@angular/router';

import { HomeComponent }                 from './home/home.component';
import { SearchComponent }               from './search/search.component';
import { PropertyComponent }             from './property/property.component';
import { NotFoundComponent }             from './not-found/not-found.component';
import { ValuationComponent }            from './valuation/valuation.component';
import { EstateAgentFinderComponent }    from './estate_agent_finder/estate_agent_finder.component';


export const routing = RouterModule.forRoot([
	{ path: '', component: HomeComponent },
	{ path: 'search', component: SearchComponent },
	{ path: 'valuation', component: ValuationComponent },
	{ path: 'estate-agent-finder', component: EstateAgentFinderComponent },
	{ path: 'property/:id', component: PropertyComponent },
	{ path: 'not-found', component: NotFoundComponent },
	{ path: '**', redirectTo: 'not-found' }
]);
