import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TmoMultipleShiptoComponent } from './tmo-multiple-shipto.component';

describe('TmoMultipleShiptoComponent', () => {
  let component: TmoMultipleShiptoComponent;
  let fixture: ComponentFixture<TmoMultipleShiptoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TmoMultipleShiptoComponent]
    });
    fixture = TestBed.createComponent(TmoMultipleShiptoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
