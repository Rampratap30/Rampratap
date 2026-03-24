import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TmoCdnMultipleShiptoComponent } from './tmo-cdn-multiple-shipto.component';

describe('TmoCdnMultipleShiptoComponent', () => {
  let component: TmoCdnMultipleShiptoComponent;
  let fixture: ComponentFixture<TmoCdnMultipleShiptoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TmoCdnMultipleShiptoComponent]
    });
    fixture = TestBed.createComponent(TmoCdnMultipleShiptoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
