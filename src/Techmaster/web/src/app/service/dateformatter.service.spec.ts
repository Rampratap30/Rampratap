import { TestBed } from '@angular/core/testing';

import { DateformatterService } from './dateformatter.service';

describe('DateformatterService', () => {
  let service: DateformatterService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DateformatterService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
