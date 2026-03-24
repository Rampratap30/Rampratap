import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TmoCdnSingleShiptoComponent } from './tmo-cdn-single-shipto.component';

describe('TmoCdnSingleShiptoComponent', () => {
  let component: TmoCdnSingleShiptoComponent;
  let fixture: ComponentFixture<TmoCdnSingleShiptoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TmoCdnSingleShiptoComponent]
    });
    fixture = TestBed.createComponent(TmoCdnSingleShiptoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
