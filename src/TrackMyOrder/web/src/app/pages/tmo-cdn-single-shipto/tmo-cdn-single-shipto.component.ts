import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-tmo-cdn-single-shipto',
  templateUrl: './tmo-cdn-single-shipto.component.html',
  styleUrls: ['./tmo-cdn-single-shipto.component.css'],
})
export class TmoCdnSingleShiptoComponent {
  order_status = {
    '1': 'Order Received',
    '2': 'In Process',
    '3': 'Scheduling',
    '4': 'Scheduled for Delivery',
    '5': 'Out for Delivery',
    '6': 'Delivered',
  };

  orders: any;
  orderId: any;
  ordernumber: any;
  orderstatus: any;
  ricoh_sp_name: any;
  ricoh_sp_email: any;
  line_details: any;
  item_details: any;
  small_parcel: any;
  small: any;
  estimated_delivery_date: any;
  date_label: any;
  additionaldetails: any;
  adddetails: any;
  siteitem: any;
  additional_details: any;
  ship_to_location: any;
  ricoh_contact_name: any;
  ricoh_contact_email: any;
  pendingTrack: any;
  ship_to_city: any;
  ship_to_state: any;
  ship_to_zip: any;
  NAME: any;
  trackorder: any;
  site_reference: any;
  installation: any;
  EQUIPMENT_REMOVAL: any;
  HARD_DRIVE_SURRENDER: any;
  displaypage: string = '';
  ricoh_order_status: any;
  data: any;
  equip_removal_det: any;
  hd_surrender_det: any;
  installation_details: any;


  constructor(private route: ActivatedRoute) {}
  ngOnInit() {
    this.route.queryParams.subscribe((params) => {
      if (params['filter']) {
        const response: any = JSON.parse(params['filter']);
        console.log(response);
        this.displaypage = response['data'].display_page.toString();
        this.ordernumber = response['data'].order_number;
        this.orderstatus = response['data'].order_status;
        this.ricoh_sp_name = response['data'].ricoh_sp_name;
        this.ricoh_sp_email = response['data'].ricoh_sp_email;
        this.line_details = response['data']['line_details'];
        this.item_details = response['data']['item_details'];
        this.small_parcel = response['data']['small_parcel'];
        this.additional_details = response['data']['additional_details'];
        this.site_reference =
          response['data']['additional_details']['site_reference'];
        this.installation_details =
          response['data']['additional_details']['installation_details'];
        this.estimated_delivery_date = response['data'].estimated_delivery_date;
        this.date_label = response['data'].date_label;
        this.equip_removal_det = response['data']['equip_removal_det'];
        this.hd_surrender_det = response['data']['hd_surrender_det'];
        if (this.line_details && this.line_details.length > 0) {
          this.ricoh_order_status = this.line_details[0].order_status;
        }
      }
    });
  }
  getCurrentStatusText(): string {
    if (this.ricoh_order_status) {
      switch (this.ricoh_order_status) {
        case '1':
          return 'Order Received';
        case '2':
          return 'In Process';
        case '3':
          return 'Scheduling';
        case '4':
          return 'Scheduled for Delivery';
        case '5':
          return 'Out for Delivery';
        case '6':
          return 'Delivered';
        default:
          return 'Unknown Status';
      }
    }
    return 'Loading...';
  }
  isAllNAForSection(section: any[]): boolean {
    return section.every(item =>
      Object.values(item).every(value => value === "N/A")
    );
  }
}
