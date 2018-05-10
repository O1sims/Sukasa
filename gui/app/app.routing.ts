
import { RouterModule }                  from '@angular/router';

import { NotFoundComponent }             from './not-found/not-found.component';


export const routing = RouterModule.forRoot([
	{ path: '', component: NotFoundComponent },
	{ path: 'not-found', component: NotFoundComponent },
	{ path: '**', redirectTo: 'not-found' }
]);
