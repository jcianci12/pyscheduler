import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnavailabilityComponent } from './unavailability.component';

describe('UnavailabilityComponent', () => {
  let component: UnavailabilityComponent;
  let fixture: ComponentFixture<UnavailabilityComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UnavailabilityComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnavailabilityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
