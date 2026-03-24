import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TmoPageNotFoundComponent } from './tmo-page-not-found.component';

describe('TmoPageNotFoundComponent', () => {
  let component: TmoPageNotFoundComponent;
  let fixture: ComponentFixture<TmoPageNotFoundComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TmoPageNotFoundComponent]
    });
    fixture = TestBed.createComponent(TmoPageNotFoundComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
