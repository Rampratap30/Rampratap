import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewSyncupComponent } from './view-syncup.component';

describe('ViewSyncupComponent', () => {
  let component: ViewSyncupComponent;
  let fixture: ComponentFixture<ViewSyncupComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ViewSyncupComponent]
    });
    fixture = TestBed.createComponent(ViewSyncupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
