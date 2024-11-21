import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GeneratescheduleComponent } from './generateschedule.component';

describe('GeneratescheduleComponent', () => {
  let component: GeneratescheduleComponent;
  let fixture: ComponentFixture<GeneratescheduleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GeneratescheduleComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GeneratescheduleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
