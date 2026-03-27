import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { HomeComponent } from './pages/home/home.component';
import { ConfigurationComponent } from './pages/configuration/configuration.component';
import { EditEmployeeComponent } from './pages/edit-employee/edit-employee.component';
import { ViewEmployeeComponent } from './pages/view-employee/view-employee.component';
import { NgbDateParserFormatter, NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AgGridModule } from 'ag-grid-angular';
import { NgxSelectModule } from 'ngx-select-ex';
import { ReactiveFormsModule } from '@angular/forms';
import { ToastrModule } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgxSpinnerModule } from 'ngx-spinner';
import { ViewsComponent } from './pages/views/views.component';
import { ScrollableTabsComponent } from './pages/views/scrollable-tabs/scrollable-tabs.component';
import { ChangesComponent } from './pages/changes/changes.component';
import { LogsComponent } from './pages/logs/logs.component';
import { ReportsComponent } from './pages/reports/reports.component';
import { ViewChangesComponent } from './pages/view-changes/view-changes.component';
import { PageNotFoundComponent } from './pages/page-not-found/page-not-found.component';
import { DateformatterService } from './service/dateformatter.service';
import { ViewSyncupComponent } from './pages/view-syncup/view-syncup.component';
import { AddEmployeeComponent } from './pages/add-employee/add-employee.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    HomeComponent,
    ConfigurationComponent,
    EditEmployeeComponent,
    ViewEmployeeComponent,
    ViewsComponent,
    ScrollableTabsComponent,
    ChangesComponent,
    LogsComponent,
    ReportsComponent,
    ViewChangesComponent,
    PageNotFoundComponent,
    ViewSyncupComponent,
    AddEmployeeComponent

  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgbModule,
    AgGridModule,
    NgxSelectModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    NgxSpinnerModule,
    ToastrModule.forRoot(),
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  providers: [
    { provide: NgbDateParserFormatter, useClass: DateformatterService }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {


}
