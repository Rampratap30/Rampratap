import { Component, OnInit, Input } from '@angular/core';
import * as $ from 'jquery';
import { environment } from './../../environments/environment';
import { CoreService } from 'src/app/service/core.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
})
export class HeaderComponent implements OnInit {
  constructor(private cs: CoreService) {}

  title: string = 'Tech Master';
  logout: string = environment.logout;
  menuItems: any[] = [];
  getUserInfo: any;
  public getRole: string | undefined;

  ngOnInit() {
    this.cs.obsGetUserInfo?.subscribe((data) => {
      this.getUserInfo = data;
      this.getRole = data?.data?.userRole;
    });

    this.menuItems = [
      { href: 'home', label: 'Home', role: 'ALL' },
      { href: 'changes', label: 'Changes', role: 'ALL' },
      { href: 'views', label: 'Views', role: 'ALL' },
      { href: 'reports', label: 'Reports', role: 'ALL' },
      { href: 'configuration', label: 'Configuration', role: 'ADMIN' },
      { href: 'logs', label: 'Logs', role: 'ADMIN' },
    ];

    $(document).ready(function () {
      $('#dismiss, .overlay').on('click', function () {
        $('#sidebar').removeClass('active');
        $('.overlay').removeClass('active');
      });
      $('#sidebarCollapse').on('click', function () {
        $('#sidebar').addClass('active');
        $('.overlay').addClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
      });
    });

    //DATA = this.menuItems;
    $(document).on('click', '.menu-item a', function (e) {
      e.preventDefault();
      $('.content').toggleClass('overlay');
      $('body').toggleClass('body-fixed');
      $('#sidebar').removeClass('active');
      $('.overlay').removeClass('active');
    });
  }
}
