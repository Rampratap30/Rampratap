import { Component, OnInit } from '@angular/core';
import { CoreService } from './services/core.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  constructor(
    public cs: CoreService,
    private router: Router,
    private route: ActivatedRoute
  ) {}
  title = 'track-my-order';
}
