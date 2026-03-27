import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ViewEmployeeComponent } from './pages/view-employee/view-employee.component';
import { EditEmployeeComponent } from './pages/edit-employee/edit-employee.component';
import { ConfigurationComponent } from './pages/configuration/configuration.component';
import { ViewsComponent } from './pages/views/views.component';
import { ChangesComponent } from './pages/changes/changes.component';
import { LogsComponent } from './pages/logs/logs.component';
import { ReportsComponent } from './pages/reports/reports.component';
import { ViewChangesComponent } from './pages/view-changes/view-changes.component';
import { PageNotFoundComponent } from './pages/page-not-found/page-not-found.component';
import { ViewSyncupComponent } from './pages/view-syncup/view-syncup.component';
import { AddEmployeeComponent } from './pages/add-employee/add-employee.component';

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
    path: 'sso',
    redirectTo: '/home',
    pathMatch: 'prefix',
  },
  {
    path: 'viewEmployee/:id',
    component: ViewEmployeeComponent,
  },
  {
    path: 'addEmployee',
    component: AddEmployeeComponent,
  },
  {
    path: 'editEmployee/:id',
    component: EditEmployeeComponent,
  },
  {
    path: 'configuration',
    component: ConfigurationComponent,
  },
  {
    path: 'views',
    component: ViewsComponent,
  },
  {
    path: 'changes',
    component: ChangesComponent,
  },
  {
    path: 'reports',
    component: ReportsComponent,
  },
  {
    path: 'logs',
    component: LogsComponent,
  },
  {
    path: 'viewChanges/:changeId/:employeeId',
    component: ViewChangesComponent,
  },
  {
    path: 'viewSyncup/:changeId/:employeeId',
    component: ViewSyncupComponent,
  },
  {
    path: 'page-not-found',
    component: PageNotFoundComponent,
  },
  {
    path: '**',
    component: PageNotFoundComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }
