import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewChangesComponent } from './view-changes.component';

describe('ViewChangesComponent', () => {
  let component: ViewChangesComponent;
  let fixture: ComponentFixture<ViewChangesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ViewChangesComponent]
    });
    fixture = TestBed.createComponent(ViewChangesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
