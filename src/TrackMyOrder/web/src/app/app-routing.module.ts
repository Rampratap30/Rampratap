import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TmoMultipleShiptoComponent } from './pages/tmo-multiple-shipto/tmo-multiple-shipto.component';
import { TmoCdnMultipleShiptoComponent } from './pages/tmo-cdn-multiple-shipto/tmo-cdn-multiple-shipto.component';
import { TmoCdnSingleShiptoComponent } from './pages/tmo-cdn-single-shipto/tmo-cdn-single-shipto.component';
import { TmoPageNotFoundComponent } from './pages/tmo-page-not-found/tmo-page-not-found.component';
import { HomeComponent } from './pages/home/home.component';

const routes: Routes = [
  {
    path: 'home',
    component: HomeComponent,
  },
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full',
  },
  {
    path: 'cdnSingleShipto',
    component: TmoCdnSingleShiptoComponent,
  },
  {
    path: 'multipleShipto',
    component: TmoMultipleShiptoComponent,
  },
  {
    path: 'cdnMultipleShipto',
    component: TmoCdnMultipleShiptoComponent,
  },
  {
    path: 'PageNotFoundComponent',
    component: TmoPageNotFoundComponent,
  },
  {
    path: '**',
    component: TmoPageNotFoundComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
