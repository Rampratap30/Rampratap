import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { TmoMultipleShiptoComponent } from './pages/tmo-multiple-shipto/tmo-multiple-shipto.component';
import { TmoCdnMultipleShiptoComponent } from './pages/tmo-cdn-multiple-shipto/tmo-cdn-multiple-shipto.component';
import { TmoCdnSingleShiptoComponent } from './pages/tmo-cdn-single-shipto/tmo-cdn-single-shipto.component';
import { TmoPageNotFoundComponent } from './pages/tmo-page-not-found/tmo-page-not-found.component';
import { HttpClientModule } from '@angular/common/http';
import { HomeComponent } from './pages/home/home.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    TmoMultipleShiptoComponent,
    TmoCdnMultipleShiptoComponent,
    TmoCdnSingleShiptoComponent,
    TmoPageNotFoundComponent,
    HomeComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
